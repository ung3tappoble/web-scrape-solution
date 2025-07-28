# 🛍 Product Scraper

This is a Python script that scrapes product data from the H&M website — including product name, price, current color, available colors, review count, and review score — and saves the results as a JSON file.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ung3tappoble/web-scrape-solution.git
cd your-repo-name
```


### 2. Install dependencies
Make sure you have Python 3 installed.
```bash
pip install -r requirements.txt
```

### 3. Run the script
To run the scraper with Firefox (default):
```bash
python main.py
```
To run the scraper with Chrome:
```bash
python main.py chrome
```

## 📦 Output
```json
{
    "name": String,
    "price": Double,
    "current_color": String,
    "available_colors": Array,
    "reviews_count": Int,
    "reviews_score": Double,
}
```

## 🛠 Technologies Used
* Python 3
* Selenium WebDriver
* WebDriver Manager
* Regular Expressions
* JSON