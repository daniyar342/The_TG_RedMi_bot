import requests
from bs4 import BeautifulSoup

url = "https://mi-shop.kg/product-category/smartphones/"
response = requests.get(url)
html = response.text
soup = BeautifulSoup(html, "html.parser")

body = soup.find("div", class_="box_content")
products = body.find("div", class_="products").find_all("div", class_="product_item_inner")


def parse_product(products):
    product_links = {}
    for product in products:
        link = product.find("a").get("href")
        price_element = product.find("span", class_="price")
        if price_element:
            price = price_element.find("span", class_="woocommerce-Price-amount amount").text.strip()
            product_links[link] = price
        else:
            product_links[link] = "Price not available"
    return product_links


def parse_page(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    body = soup.find("div", class_="box_content")
    products = body.find("div", class_="products").find_all("div", class_="product_item_inner")
    product_links = parse_product(products)
    return product_links


n = parse_page("https://mi-shop.kg/product-category/smartphones/")
product_links = [{f"{link}" : f"{price}" } for link, price in n.items()]
