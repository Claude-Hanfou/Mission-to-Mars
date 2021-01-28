# Dependencies
from bs4 import BeautifulSoup
import requests
import time
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    mars= {}



    #Start with the paragraph and the title_container
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
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

    #Store in main dictionary
    mars['news_title'] = news_title
    mars['news_paragraph'] = news_p
    

    
    #get the table information
    url2= 'https://space-facts.com/mars/'
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
   
    grab=pd.read_html(url2)
    mars_data=pd.DataFrame(grab[0])
    mars_data.columns=['Mars','Data']
    mars_table=mars_data.set_index("Mars")
    marsdata = mars_table.to_html(classes='marsdata')
    marsdata=marsdata.replace('\n', ' ')
    marsdata
    #store in main dictionary
    mars['marsdata'] = marsdata



    #get the image
    url3 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Retrieve page with the requests module
    browser.visit(url3)
    html = browser.html

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html, 'html.parser')

    hemisphere_image_urls = []
    #Create forloop for image and title
    for i in range (4):
        time.sleep(5)
        header=browser.find_by_tag('h3')
        header[i].click()
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        link= soup.find('img', class_ ='wide-image')['src']
        title=soup.find('h2', class_='title').text
        image= 'https://astrogeology.usgs.gov/' + link
        dictionary={"title": title , "img_url":image}
        hemisphere_image_urls.append(dictionary)
        browser.back()
    #store in main dictionary
    mars['hemispher_image_urls'] = hemisphere_image_urls


    # Close the browser after scraping
    browser.quit()

    #return mars
    return mars