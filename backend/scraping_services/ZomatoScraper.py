import scrapy
from scrapy.crawler import CrawlerProcess
import re
import os
import requests
import bs4 as bs
from bs4 import BeautifulSoup
from selenium import webdriver

from selenium import webdriver 
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException

if __name__=="__main__":
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
    os.environ["webdriver.chrome.driver"] =  "C:\\Software"
    browser = webdriver.Chrome()
    timeout=200
    i=0
    # Wait for the page to load
    for i in range(1, 10):
        page_url = "https://www.zomato.com/bangalore/delivery?page={}".format(i)
        browser.get(page_url)
        try:
            WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CSS_SELECTOR,
            'div.col-s-16.search_results.mbot')))
        except TimeoutException:
            print('Timed out waiting for delivery page to load:{}'.format(page_url))
            browser.quit()

        # Get the list of each restaurant
        restaurant_list_level_1 = browser.find_elements_by_xpath('.//*[@id="orig-search-list"]')
        for restaurant_level_1 in restaurant_list_level_1:
            restaurant_list_level_2 = restaurant_level_1.find_elements_by_css_selector('.a[data-result-type]')[0]
            print(restaurant_list_level_2)
            # for restaurant_level_2 in restaurant_list_level_2:
            #     restaurant_name_attributes = restaurant_level_2.find_elements_by_css_selector('a.result-title.hover_feedback.zred.bold.ln24.fontsize0')
            #     restaurant_name = restaurant_name_attributes.find_elements_by_css_selector('title').text
            #     restaurant_link = restaurant_name_attributes.find_elements_by_css_selector('href').text
            #     print(restaurant_name)

        # browser.get("https://www.zomato.com/bangalore/eat-fit-hsr-bangalore/order")
        # try:
        #     WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="menu-container"]')))
        # except TimeoutException:
        #     print('Timed out waiting for page to load')
        #     browser.quit()
        # menu_items_holder = browser.find_elements_by_xpath('//*[@class="menu-container"]')
        # menu_items = menu_items_holder[0].find_elements_by_xpath('//*[@id="menu_0"]')
        # # use list comprehension to get the actual repo titles and not the selenium objects.
        # items = [item.text for item in menu_items]
        # # print out all the titles.
        # print('items:')
        # print(items, '\n')