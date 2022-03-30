import re
import json
import redis
import requests
from bs4 import BeautifulSoup


#Used headers/agent because the request was timed out and asking for an agent. 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

# The resultant dictionary
res_dict = {}
# To scroll one by one pages
page_index = 0
for page_index in range(1, 5):
    page_url = "https://www.foodpanda.in/restaurants?page={}".format(page_index)
    response = requests.get(page_url,headers=headers)
    content = response.content
    soup = BeautifulSoup(content,"html.parser")

    # Get the page restuartant list
    details = soup.find_all("section", attrs={"class": "js-infscroll-load-more-here"})
    res_details = details[0].find_all("article", attrs={"class": "vendor list js-vendor-list-vendor-panel"})

    # Per resturant flow
    for res in res_details:
        name_list = [] 
        res_link = []
        # Resturant Info 
        res_info = res.find_all("a", attrs={"class": "vendor__inner js-fire-click-tracking-event"})
        res_link.append(res_info[0]['href'])
        vendor_info = res_info[0].find_all("div", attrs={"class":"vendor__details"})
        # Get the name of resturant 
        name = vendor_info[0].find_all("div", attrs={"class":"vendor__title"})[0].find('span').text.replace(" ", "").replace("\n", "")
        name_list.append(name) 

        # Get the cuisine list
        i = 0
        vendor_cuisine = vendor_info[0].find_all("ul", attrs={"class": "vendor__cuisines"})
        for cuisine in vendor_cuisine: 
            cuisine_dict = {} 
            for l in cuisine.contents:
                cuisine_dict[l.string] = {} 
            res_dict[name_list[i]] = {'cuisine': cuisine_dict, 'link': res_link[i]}
            i = i + 1
    #print res_dict

    # Fill the Cuisine for each resturant
    for k in res_dict.keys():
        res_link = "https://www.foodpanda.in" + res_dict[k]['link']
        response = requests.get(res_link, headers=headers) 
        content = response.content
        soup = BeautifulSoup(content,"html.parser")

        cuisine = res_dict[k]['cuisine']
        # North Indian Cuisine
        if 'North Indian' in cuisine:
            nort_indian_dict = {}
            bread_dict = {}
            rice_dict = {}
            curry_dict = {}

            # Get Bread item
            bread_parent = soup.find_all("div", attrs={"id": "menu_delivery-menu_category_breads"})#[0].parent.parent
            if bread_parent:
                bread_parent = bread_parent[0].parent.parent
                for child in bread_parent: 
                    bread = child.find("article")
                    if bread and bread != -1:
                        bread_name = bread['data-clicked_product_name']
                        bread_price = bread.find('div', attrs={'class': 'menu-item__variation__price'}).string
                        if bread_price:
                            bread_price = bread_price.replace(' ', '').replace('\n', '')
                        bread_dict[bread_name] = bread_price
            print bread_dict 
            nort_indian_dict['Bread'] = bread_dict
            
            # Get Rice item
            rice_parent =  soup.find_all("div", attrs={"id": re.compile("menu_delivery-menu_category_*rice*")})
            if rice_parent:
                rice_parent = rice_parent[0].parent.parent
                for child in rice_parent:
                    rice = child.find("article")
                    if rice and rice != -1:
                        rice_name = rice['data-clicked_product_name']
                        rice_price = rice.find('div', attrs={'class': 'menu-item__variation__price'}).string
                        if rice_price:
                            rice_price = rice_price.replace(' ', '').replace('\n', '')
                        rice_dict[rice_name] = rice_price
            print rice_dict
            nort_indian_dict['Rice'] = rice_dict
          
            # Get Curry item
            # Need to make iteartive 
            curry_parent = soup.find_all("div", attrs={"id": re.compile("menu_delivery-menu_category.*main-course*")})
            if curry_parent:
                curry_parent = curry_parent[0].parent.parent
                for child in curry_parent:
                    curry = child.find("article")
                    if curry and curry != -1:
                        curry_name = curry['data-clicked_product_name'] 
                        curry_price = curry.find('div', attrs={'class': 'menu-item__variation__price'}).string
                        if curry_price:
                            curry_price = curry_price.replace(' ', '').replace('\n', '')
                        curry_dict[curry_name] = curry_price
            print curry_dict
            nort_indian_dict['Curry'] = curry_dict
            print nort_indian_dict
            res_dict[k]['cuisine']['North Indian'].update(nort_indian_dict)

    print "Dic \n\n\n"
    print res_dict


# Publish resturant details on the redis
conn = redis.Redis('localhost', port=6379)
resturant_data = {"value": json.dumps(res_dict), "version": "0"}
conn.hmset("/Butler/FoodPanda", resturant_data)

#print conn.hgetall("/Butler/FoodPanda")
