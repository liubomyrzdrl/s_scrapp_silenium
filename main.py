from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


def main():
    options = Options()
    options.add_argument("--headless")  # Запуск без UI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    # You can replace the URL with the one you want to scrape
    driver.get("https://yabloki.ua/mac/macbook-air/?header=22")

    time.sleep(2)  # We are waiting for the page to load

    product_title = driver.find_elements(By.CLASS_NAME, "title")
    prices = driver.find_elements(By.CLASS_NAME, "product-card-catalog-info-price")

    data = []

    for title, price in zip(product_title, prices):
        try:
            title_text = title.text.strip()
            price_text = price.text.strip()
            data.append({
                "title": str(title_text),
                "price": str(price_text)
            })
        except Exception as e:
            print(f"Error extracting data: {e}")

    for i, item in enumerate(data[:5]):
        print(f"Item {i}:")
        for key, value in item.items():
            print(f"  {key}: {value} (type: {type(value)})")

    # Change price format if necessary
    # This part ensures that the price is a string and replaces new lines with a slash
    for item in data:
        if isinstance(item["price"], str):
            item["price"] = item["price"].replace("\n", " / ").strip()
        else:
            item["price"] = str(item["price"])

    try:
        df = pd.DataFrame(data)
        print("DataFrame created successfully.")
    except Exception as e:
        print(f"Error creating DataFrame: {e}")
        for i, item in enumerate(data):
            print(f"Item {i}:")
            for k, v in item.items():
                print(f"  {k}: {v} ({type(v)})")
        driver.quit()
        return

    # Write DataFrame to Excel
    try:
        with pd.ExcelWriter("data.xlsx", engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Macbook Prices')
    except Exception as e:
        print(f"Error saving data to Excel: {e}")

    driver.quit()


if __name__ == "__main__":
    main()
