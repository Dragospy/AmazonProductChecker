import undetected_chromedriver
from search import search_products
from compare import compare_products

def get_url(search_string) -> str: #transforms the users search query into an amazon compatible search query
    url = search_string.replace(" ", "+")
    return url

def main():
    products = []
    driver = undetected_chromedriver.Chrome(headless = True)
    
    while True:
        user_input = input("What would you like to do? \n| Search | Compare | Exit |\n")
        
        if user_input.lower() == "exit":#Simply close the program
            break
        
        if user_input.lower() == "search":#Search for a producut
            search_string = input("What would you like to search for? \n").lower()
            products = search_products(driver, get_url(search_string))
        
        if user_input.lower() == "compare":
            if len(products) == 0:
                print("You haven't searched for any products yet, so nothing to compare.")
                continue
            
            compare_products(driver, products)
            
    driver.close() #close the headless browser
    
main()