import json
import sys
import re

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

URL = "https://www2.hm.com/bg_bg/productpage.1274171042.html"

def init_driver(browser="firefox"):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        return webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    else:
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1200")
        options.add_argument("--height=800")
        return webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

def wait_text(driver, by, identifier, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, identifier))
    ).text.strip()

def extract_review_count(text):
    match = re.search(r"Коментари\s*\[(\d+)\]", text, flags=re.IGNORECASE)
    if match:
        return int(match.group(1))
    return 0

def extract_review_score(text):
    match = re.search(r"(\d{1}.\d{1}).*", text)
    if match:
        return float(match.group(1))
    return 0

def get_product_data(browser="firefox"):
    driver = init_driver(browser)
    driver.get(URL)

    try:
        data = {}
        #Product name
        name_element = driver.find_elements(By.XPATH, "//h1[contains(text(),'Тениска с принт')]")
        if name_element:
            data["name"] = name_element[0].text
        else:
            data["name"] = None

        #Price
        price_element = driver.find_elements(By.XPATH, "//*[contains(text(),'Тениска с принт')]//following::*[contains(text(),'лв')]")
        if price_element:
            price_text_el = price_element[0].text
            price = price_text_el.replace("лв.", "").replace(",", ".").strip()
            data["price"] = float(''.join(c for c in price if c.isdigit() or c == '.'))
        else:
            data['price'] = None

        #Current Color
        current_color_element = driver.find_elements(By.XPATH, "(//*[contains(text(),'Цвят:')]//following::p)[1]")
        if current_color_element:
            current_color_text = current_color_element[0].text
            current_color = current_color_text
            data["current_color"] = current_color
        else:
            data['current_color'] = None

        #Available Colors
        try:
            show_all_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@data-testid, 'grid')]//button"))
            )
            show_all_button.click()
        except Exception as e:
            print("Button not found", e)

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@data-testid, 'grid')]//a"))
        )

        color_links = driver.find_elements(By.XPATH, "//div[contains(@data-testid, 'grid')]//a")
        available_colors = [el.get_attribute("title") or el.text.strip() for el in color_links]

        data["available_colors"] = available_colors

        #Reviews Count
        reviews_count_element = driver.find_elements(By.XPATH, "//button[contains(text(),'Коментари')]")
        if reviews_count_element:
            reviews_count_text = reviews_count_element[0].text
            data["reviews_count"] = extract_review_count(reviews_count_text)
        else:
            data["reviews_count"] = 0


        # Reviews Score
        reviews_score_element = driver.find_elements(By.XPATH, "//*[contains(@aria-label, 'out of 5')]")
        if reviews_score_element:
            reviews_score_text = reviews_score_element[0].text
            data["reviews_score"] = extract_review_score(reviews_score_text)
        else:
            data["reviews_score"] = 0

        # JSON save
        with open("product_data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("Data saved successfully to product_data.json:")
        print(json.dumps(data, indent=4, ensure_ascii=False))

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    browser = sys.argv[1] if len(sys.argv) > 1 else "firefox"
    get_product_data(browser)
