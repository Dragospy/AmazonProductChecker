from bs4 import BeautifulSoup
from config import *

def compare_products(driver, products) -> None:
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

    
    for i in [product_1_index, product_2_index]:
        driver.get(products[i].link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find("table", {'id': 'productDetails_techSpec_section_1'})
        
        brand_name = results.find_all('tr')[0].find('th').text
        brand__name_text = results.find_all('tr')[0].find('td').text
        print(brand_name.strip(), brand__name_text.strip())
    
    
    return