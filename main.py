import undetected_chromedriver
from bs4 import BeautifulSoup
from os import system

attributes = ['rating', 'name', 'price'] #attributes of the product class

class product:
    def __init__(self, item) -> None:
        name_container = item.find("div", {'data-cy': 'title-recipe'})
        self.name = name_container.find('span').text[:25]   
        
        rating_container = item.find("i", {'data-cy': 'reviews-ratings-slot'})
        self.rating = rating_container.find("span").text[:3] #Rating cannot be bigger than 3 characters

        self.link = 'https://www.amazon.co.uk/dp/'+item['data-asin']
        
        price_container = item.find("div", {'data-cy': 'price-recipe'})
        if len(price_container.find_all("span")) < 2:
            return
        
        self.price = price_container.find("span", {'class': 'a-offscreen'}).text

def get_url(search_string) -> str: #transforms the users search query into an amazon compatible search query
    url = search_string.replace(" ", "+")
    return url

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
        
        if getattr(productVar, "price", None) == None:
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
    

def search(driver, search_query):#takes the processed user query and gets every search result on the first page, then lists every item found
    url = f'https://www.amazon.co.uk/s?k={search_query}'
    
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all("div", {'data-component-type': 's-search-result'})
    
    products = []
    
    process_products(products, results)
        
    sort_check(products)
            
    system("clear||cls")
    
    for item in products:
       print(f"Name: {item.name} \nPrice: {item.price} \nRating: {item.rating}/5 \nLink: {item.link} \n ")
    
    return products

def compare_products(products) -> None:
    
    
    return

def main():
    products = []
    driver = undetected_chromedriver.Chrome(headless = True)
    
    while True:
        user_input = input("What would you like to do? \n| Search | Compare | Exit |\n")
        
        if user_input.lower() == "exit":#Simply close the program
            break
        
        if user_input.lower() == "search":#Search for a producut
            search_string = input("What would you like to search for? \n").lower()
            products = search(driver, get_url(search_string), products)
        
        if user_input.lower() == "compare":
            if len(products) == 0:
                print("You haven't searched for any products yet, so nothing to compare.")
                continue
            
            compare_products(products)
            
    driver.close() #close the headless browser
    
main()