import undetected_chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time

attributes = ['rating', 'name', 'price']

class product:
    def __init__(self, item) -> None:
        title_container = item.find("div", {'data-cy': 'title-recipe'})
        self.title = title_container.find('span').text[:25]   
        
        rating_container = item.find("i", {'data-cy': 'reviews-ratings-slot'})
        self.rating = rating_container.find("span").text[:3] #Rating cannot be bigger than 3 characters

        self.link = 'https://www.amazon.co.uk/dp/'+item['data-asin']
        
        price_container = item.find("div", {'data-cy': 'price-recipe'})
        if len(price_container.find_all("span")) < 2:
            return
        self.price = price_container.find("span", {'class': 'a-offscreen'}).text

def get_url(search_string) -> str:
    url = search_string.replace(" ", "+")
    return url

def swap(products, j) -> None:
    temp = products[j + 1]
    products[j + 1] = products[j]
    products[j] = temp

def sort_products(products: list[product], sortingType: str) -> None:
    for i in range(len(products) - 1):
        for j in range(len(products) - 1 - i):
            
            if sortingType == 'name' and getattr(products[j], sortingType) <= getattr(products[j + 1], sortingType):
                swap(products, j)
            
            if sortingType == 'price' and float(getattr(products[j], sortingType)[1:]) <= float(getattr(products[j + 1], sortingType)[1:]) :
                swap(products, j)
                
            
            if sortingType == 'rating' and float(getattr(products[j], sortingType)) <= float(getattr(products[j + 1], sortingType)):
                swap(products, j)

def search(driver, search_query):
    url = f'https://www.amazon.co.uk/s?k={search_query}'
    
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("div", {'data-component-type': 's-search-result'})
    
    products = []
    item_count = 0
    
    for item in results:
        if item_count == 10:
            break
        
        productVar = product(item)
        
        if getattr(productVar, "price", None) == None:
            continue
        
        products.append(productVar)
        item_count += 1
        
    while True: 
        sortingType = input("How would you like to sort it? \n| Rating | Name | Price\n").lower()
                
        if not sortingType in attributes:
            print("Not a valid attribute!") 
        
        sort_products(products, sortingType)    
        break
            
    
    for item in products:
       print(f"Name: {item.title} \nPrice: {item.price} \nRating: {item.rating} /5 \nLink: {item.link}")
    
    return products

def main():
    products = []
    driver = undetected_chromedriver.Chrome(headless = True)
    
    while True:
        user_input = input("What would you like to do? \n| Search | Compare | EXIT |\n")
        
        if user_input.lower() == "exit":
            break
        
        if user_input.lower() == "search":
            search_string = input("What would you like to search for? \n").lower()
            url = get_url(search_string)
            products = search(driver, url)
        
        if user_input.lower() == "compare":
            if len(products) == 0:
                print("You haven't searched for any products yet, so nothing to compare.")
                continue
            
            print("Logic Incoming")
            
    driver.close()
    
main()