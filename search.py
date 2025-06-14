from bs4 import BeautifulSoup
from product import product
from os import system

attributes = ['rating', 'name', 'price'] #attributes of the product class
link_end = 'co.uk'

def swap(products, j) -> None:#simple swap of two elements in a list
    temp = products[j + 1]
    products[j + 1] = products[j]
    products[j] = temp

def sort_products(products: list[product], sortingType: str) -> None:#sorts the products in the order of the selected attribute
    for i in range(len(products) - 1):
        for j in range(len(products) - 1 - i):
            
            if sortingType == 'name' and getattr(products[j], sortingType) >= getattr(products[j + 1], sortingType):
                swap(products, j)
            
            if sortingType == 'price' and float(getattr(products[j], sortingType)[1:]) >= float(getattr(products[j + 1], sortingType)[1:]) :
                swap(products, j)
                
            if sortingType == 'rating' and float(getattr(products[j], sortingType)) <= float(getattr(products[j + 1], sortingType)):
                swap(products, j)
                
def process_products(products, results) -> None: #Processes the HTML returned and created product objects using the product class
    count = 0
    
    for item in results:
        
        if count >= 10:
            break
        
        productVar = product(item)
        
        if getattr(productVar, "listable", None) == None:
            continue
        
        count += 1
        
        products.append(productVar)
        
def sort_check(products) -> None:
    while True: 
        sortingType = input("How would you like to sort it? \n| Rating | Name | Price\n").lower()
                
        if not sortingType in attributes:
            print("Not a valid attribute!") 
        
        sort_products(products, sortingType)    
        
        break
    

def search_products(driver, search_query):#takes the processed user query and gets every search result on the first page, then lists every item found
    url = f'https://www.amazon.{link_end}/s?k={search_query}'
    
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("div", {'data-component-type': 's-search-result'})
    
    products = []
    
    process_products(products, results)
        
    sort_check(products)
            
    system("clear||cls")
    
    for i in range(len(products)):
        item = products[i]
        print(f"{i+1}. Name: {item.name} \nPrice: {item.price} \nRating: {item.rating}/5 \nLink: {item.link} \n ")
    
    return products