from config import *

class product:
    def __init__(self, item) -> None:
        name_container = item.find("div", {'data-cy': 'title-recipe'})
        self.name = name_container.find('span').text[:25]   
        
        rating_container = item.find("i", {'data-cy': 'reviews-ratings-slot'})
        if not rating_container:
            return
        self.rating = rating_container.find("span").text[:3] #Rating cannot be bigger than 3 characters

        self.link = f'https://www.amazon.{link_end}/dp/{item['data-asin']}'
        
        price_container = item.find("div", {'data-cy': 'price-recipe'})
        if len(price_container.find_all("span")) < 2:
            return
        self.price = price_container.find("span", {'class': 'a-offscreen'}).text
        
        self.listable = True
