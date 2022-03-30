import re
import requests
from bs4 import BeautifulSoup


#Used headers/agent because the request was timed out and asking for an agent. 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
response = requests.get("https://www.foodpanda.in/restaurants",headers=headers)

content = response.content
soup = BeautifulSoup(content,"html.parser")

#print soup 

details = soup.find_all("section", attrs={"class": "js-infscroll-load-more-here"})
#print res_name

res_details = details[0].find_all("article", attrs={"class": "vendor list js-vendor-list-vendor-panel"})


res_dict = {}
for res in res_details:
    name_list = [] 
    res_link = []
    #cuisine_dict = {}
    res_info = res.find_all("a", attrs={"class": "vendor__inner js-fire-click-tracking-event"})
    #print res_info[0]['href'] 
    res_link.append(res_info[0]['href'])
    vendor_info = res_info[0].find_all("div", attrs={"class":"vendor__details"})
    # Name 
    name = vendor_info[0].find_all("div", attrs={"class":"vendor__title"})[0].find('span').text.replace(" ", "")
    name_list.append(name) 
    i = 0
     
    vendor_cuisine = vendor_info[0].find_all("ul", attrs={"class": "vendor__cuisines"})
    for cuisine in vendor_cuisine: 
        cuisine_dict = {} 
        for l in cuisine.contents:
            cuisine_dict[l.string] = {} 
            #cuisine_list.append(l.string)
        res_dict[name_list[i]] = {'cuisine': cuisine_dict, 'link': res_link[i]}
        i = i + 1
print res_dict

#for k in res_dict.keys():
#res_link = "https://www.foodpanda.in/restaurant/r3cf/new-punjabi-food-corner?vendorId=28569"# + res_dict[k]['link']
res_link = "https://www.foodpanda.in/restaurant/n8qp/new-andhra-house-vbg?vendorId=4637"
#res_link = "https://www.foodpanda.in" + res_dict[k]['link']
response = requests.get(res_link, headers=headers) 
content = response.content
soup = BeautifulSoup(content,"html.parser")

#print res_dict
for k in res_dict.keys():
    if res_dict[k]['link'] == res_link.replace('https://www.foodpanda.in', ''):
        cuisine = res_dict[k]['cuisine']
        if 'North Indian' in cuisine:
            nort_indian_dict = {}
            bread_dict = {}
            rice_dict = {}
            curry_dict = {}

            # Get Bread item
            bread_parent = soup.find_all("div", attrs={"id": "menu_delivery-menu_category_breads"})[0].parent.parent
            #print bread_parent
            for child in bread_parent: 
                bread = child.find("article")
                if bread and bread != -1:
                    bread_name = bread['data-clicked_product_name']
                    bread_price = bread.find('div', attrs={'class': 'menu-item__variation__price'}).string.replace(' ', '')
                    bread_dict[bread_name] = bread_price
            #print bread_dict 
            nort_indian_dict['Bread'] = bread_dict
            
            # Get Rice item
            rice_parent =  soup.find_all("div", attrs={"id": re.compile("menu_delivery-menu_category_*rice*")})[0].parent.parent
            for child in rice_parent:
                rice = child.find("article")
                if rice and rice != -1:
                    rice_name = rice['data-clicked_product_name']
                    rice_price = rice.find('div', attrs={'class': 'menu-item__variation__price'}).string.replace(' ', '')
                    rice_dict[rice_name] = rice_price
            #print rice_dict
            nort_indian_dict['Rice'] = rice_dict
            
            # Get Curry item
            # Need to make iteartive 
            curry_parent = soup.find_all("div", attrs={"id": re.compile("menu_delivery-menu_category.*main-course*")})[0].parent.parent
            #print curry_parent
            for child in curry_parent:
                curry = child.find("article")
                #print curry
                if curry and curry != -1:
                    curry_name = curry['data-clicked_product_name'] 
                    curry_price = curry.find('div', attrs={'class': 'menu-item__variation__price'}).string.replace(' ', '')
                    curry_dict[curry_name] = curry_price
            print curry_dict
            nort_indian_dict['Curry'] = curry_dict
            res_dict[k]['cuisine']['North Indian'].update(nort_indian_dict)
print res_dict
#print soup



