import os
import urllib
import urllib2
import requests
from bs4 import BeautifulSoup


#Used headers/agent because the request was timed out and asking for an agent. 
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
response = requests.get("https://www.zomato.com/bangalore/restaurants/north-indian",headers=headers)

content = response.content
soup = BeautifulSoup(content,"html.parser")

#print soup 

#North Indian Cuisines
nort_indian_res = soup.find_all("div", attrs={"class": "col-s-16 search_results mbot"})
first_page_all_info = nort_indian_res[0].find_all("div", attrs={"class": "orig-search-list-container"})
first_page_res = first_page_all_info[0].find_all("div", attrs={"id": "orig-search-list"})
#print first_page_res

rest_dict = {}
info =  first_page_res[0].find_all("div", attrs={"class": "card search-snippet-card search-card" or "card search-snippet-card all_web_jumbo_impr_track all_web_jumbo_click_track search-card"})

for info1 in info:
    rest_info = info1.find("div", attrs={"class": "content"}).find("div").find("article").find("div", attrs={"class": "pos-relative clearfix"}).find("div").find("div", attrs={"class":"col-s-16 col-m-12 pl0"}) 
    # Right Now just sending the location, so using find instaed of find_all
    result = rest_info.find("div", attrs={"class":"row"}).find_all("div", attrs={"class":"col-s-12"})
    for r in result:
        temp = {}
        details = r.find("a", attrs={"class": "result-title hover_feedback zred bold ln24 fontsize0"})
        temp[details.text.split('\n')[0]] = {'address': details["title"].split(', ')[1], 'link': details["href"]}
        rest_dict.update(temp)  

#print rest_dict

# Get the menu    
res_menu = "https://www.zomato.com/bangalore/sultans-of-spice-koramangala-5th-block"
response1 = requests.get("https://www.zomato.com/bangalore/midnight-bites-marathahalli-bangalore/order", headers=headers)
content1 = response1.content
soup_menu = BeautifulSoup(content1,"html.parser")
print soup_menu





'''
# Collections
collection = soup.find_all("div", attrs={"class": "collections-grid row"})
c = collection[0].find_all("div", attrs={"class": "col-l-8 col-s-16 mbot"})
for t in c:
    print (t.find("div", attrs={"class": "heading bold ln20"})).text
    #print t

# top resturant 
top_rest = soup.find_all("div",attrs={"class": "bb0 collections-grid col-l-16"})
list_tr = top_rest[0].find_all("div",attrs={"class": "col-s-8 col-l-1by3"})

#print top_rest 


list_rest =[]
for tr in list_tr:
    dataframe ={}
    dataframe["rest_name"] = (tr.find("div",attrs={"class": "res_title zblack bold nowrap"})).text.replace('\n', ' ')
    dataframe["rest_address"] = (tr.find("div",attrs={"class": "nowrap grey-text fontsize5 ttupper"})).text.replace('\n', ' ')
    dataframe["cuisine_type"] = (tr.find("div",attrs={"class":"nowrap grey-text"})).text.replace('\n', ' ')
    list_rest.append(dataframe)
print list_rest 
'''
