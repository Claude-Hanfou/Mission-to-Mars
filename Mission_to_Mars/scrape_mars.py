# Dependencies
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars_info= {}



    #Start with the paragraph and the title_container
    url = "https://raleigh.craigslist.org/search/hhh?max_price=1500&availabilityMode=0"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #news title
    news_title = soup.find('ul', class_='item_list')
    title = news_title.find('li', class_='slide') 
    bottom= title.find('div', class_='bottom_gradient')
    news_title = bottom.find('h3').text   

    #get the paragraph info
    news_p = title.find('div', class_='rollover_description_inner').text

    #Store in main dict
    mars_info['news_title'] = news_title
    mars_info['news_paragraph'] = news_p
    
    return mars_info

    
    #get the table ingormation
    url = "https://space-facts.com/mars/'
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
   

    tables = pd.read_html(url2)
    df = tables[0]