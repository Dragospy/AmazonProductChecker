from bs4 import BeautifulSoup
from config import *
import time
from os import system
from product import list_products

def compare_products(driver, products) -> None:
    system("clear||cls")
    
    list_products(products)
    
    product_1_index = ""
    
    while not product_1_index.isdigit():
        product_1_index = input("Choose a product (number before the name of the product)\n").lower()
    
    product_2_index = ""
    while not product_2_index.isdigit() and product_2_index != product_1_index:
        product_2_index = input("Choose a product to compare it with (number before the name of the product)\n").lower()
        
        if product_2_index == product_1_index:
            print("Can't compare an item with itself!")
            product_2_index = ""
            
    product_1_index, product_2_index = int(product_1_index), int(product_2_index)
    
    product_specs = [{}, {}]
    index_tracker = 0
    
    
    print("\nFetching products (Fetching is delayed to prevent Amazon bot detection)")

    for i in [product_1_index, product_2_index]:
        print(f"Fetching product {i}")
        
        time.sleep(2)
        
        driver.get(products[i].link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        results = soup.find("table", {'id': 'productDetails_techSpec_section_1'})
        
        if not results:
            print("Failed to fetch product details, please try again later.")
            return
        
        specifications = results.find_all('tr')
        for spec in specifications:
            spec_name = (spec.find('th').text).strip()
            spec_data = (spec.find('td').text).strip()
            
            product_specs[index_tracker][spec_name] = spec_data
        
        index_tracker += 1
    
    system("clear||cls")
    
    print(f"Product {product_1_index} link: {products[product_1_index].link} \nProduct {product_2_index} link: {products[product_2_index].link} \n")
    
    for index, (key, value) in enumerate(product_specs[0].items()):
        print(f'{key}:\n {product_1_index} -> {value}\n {product_2_index} -> {"No Comparable Data Listed" if (key not in product_specs[1]) else product_specs[1][key]}')
        print("")
    
    
    return