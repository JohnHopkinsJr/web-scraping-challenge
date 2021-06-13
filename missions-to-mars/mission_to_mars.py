#!/usr/bin/env python
# coding: utf-8
# *************************************
# *************************************
# John Hopkins 5/24/2021
# *************************************
# *************************************

# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import os
import pandas as pd
import time
 
# *************************************
# *************************************

def scrape():
    try:
        # Start with an empty dict
        mars_info = {}
    
        # ChromeDriver Needed to Open Browser
        executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        browser = Browser('chrome', **executable_path, headless=False)

        ## Begin Scraping 

        # NASA News Title
        news_url = 'https://mars.nasa.gov/news/'
        browser.visit(news_url)

        time.sleep(3)

        # Create a Beautiful Soup object
        news_html = browser.html
        news_para = bs(news_html,'html.parser')

        # NASA Mars News Extracted Title and Paragraph Text
        #news_title = news_title.soup.find("div",class_="content_title").text
        #news_paragraph = news_paragraph.soup.find("div", class_="rollover_description_inner").text

        news_title = news_para.find("div",class_="content_title").text
        news_para = news_para.find("div", class_="rollover_description_inner").text
        print(f"Title: {news_title}")
        print(f"Paragraph: {news_para}")

        # Dictionary entry from MARS NEWS
        mars_info['news_title'] = news_title
        mars_info['news_para'] = news_para

        # browser.quit()
        # *************************************

        # JPL Mars Space Images - Featured Image
        jpl_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
        browser.visit(jpl_url)

        time.sleep(2)

        # Create a Beautiful Soup HTML Object
        html_image = browser.html
        soup = bs(html_image, "html.parser")
        imgs = soup.find("a", "fancybox-thumbs")
        print(imgs)
        # For each item iterate through the list and append featured_image_url 
        feat_img = []
        featured_image_url =''
        for img in imgs:
            pic = imgs['href']
            print(pic)
            feat_img.append(pic)
            featured_image_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/' + pic
            print(featured_image_url)
        # Dictionary entry from FEATURED IMAGE
        mars_info['featured_image_url'] = featured_image_url
        # mars_info['featured_image_url'] = featured_image_url

        # browser.quit()
        # *************************************

        # Mars Facts
        # Visit the Mars Facts webpage [here](https://space-facts.com/mars/) and use Pandas to scrape the table containing 
        # facts about the planet including Diameter, Mass, etc.
        # U se Pandas to convert the data to a HTML table string.

        url = 'https://space-facts.com/mars/'
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')

        # Clean Data
        tables = pd.read_html(url)
        marsdf = tables[0]
        marsdf.columns = ['Stat', 'Measurement']
        s = pd.Series(marsdf['Stat'])
        marsdf['Stat'] = s.str.strip(':')
        marsdf = marsdf.set_index('Stat')

        #Use to_html method to generate HTML tables from df
        html_table = marsdf.to_html()
        
        # data = marsdf.to_html('mars_table.html')
        # data=html_table
        
        # print(data)
        # Dictionary entry from MARS FACTS
        mars_info['mars_facts'] = html_table

        # browser.quit()
        # *************************************

        # Mars Hemispheres
        # Visit the USGS Astrogeology site [here]
        # (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution 
        # images for each of Mar's hemispheres.

        # ChromeDriver Needed to Open Browser
        # executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
        # browser = Browser('chrome', **executable_path, headless=False)

        # Setting url for alternate browser
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        #browser.get(url)
        browser.visit(url)

        nextpage_urls = []
        imgtitles = []
        base_url = 'https://astrogeology.usgs.gov'

        # HTML object
        html = browser.html
        # Parse HTML with Beautiful Soup
        soup = bs(html, 'html.parser')
        # Retrieve all elements that contain hemisphere photo info
        divs = soup.find_all('div', class_='description')

        # Iterate through each div to pull titles and make list of hrefs to iterate through
        counter = 0
        for div in divs:
            # Use Beautiful Soup's find() method to navigate and retrieve attributes
            link = div.find('a')
            href=link['href']
            img_title = div.a.find('h3')
            img_title = img_title.text
            imgtitles.append(img_title)
            next_page = base_url + href
            nextpage_urls.append(next_page)
            counter = counter+1
            if (counter == 4):
                break

        # Use Beautiful Soup's find() method to navigate and retrieve attributes
        my_images=[]
        for nextpage_url in nextpage_urls:
            url = nextpage_url
            browser.visit(url)
            html = browser.html
            soup = bs(html, 'html.parser')
            link2 = soup.find('img', class_="wide-image")
            forfinal = link2['src']
            full_img = base_url + forfinal
            my_images.append(full_img)
            nextpage_urls = []
            my_images

        # Creating final list of dictionaries imgtitles and my_images
        hemisphere_image_urls = []

        cerberus = {'title':imgtitles[0], 'img_url': my_images[0]}
        schiaparelli = {'title':imgtitles[1], 'img_url': my_images[1]}
        syrtis = {'title':imgtitles[2], 'img_url': my_images[2]}
        valles = {'title':imgtitles[3], 'img_url': my_images[3]}

        hemisphere_image_urls = [cerberus, schiaparelli, syrtis, valles]

        mars_info['hemi_img_url'] = hemisphere_image_urls
        print('************START************')
        print(mars_info)
        print('************END************')
        return mars_info

    finally:

        browser.quit()

# *************************************
# *************************************
     
# johnhopkins@Batman-13609:~/Code!/web-scraping-challenge$ jupyter nbconvert --to script mission_to_mars.ipynb
# [NbConvertApp] Converting notebook mission_to_mars.ipynb to script
# [NbConvertApp] Writing 5406 bytes to mission_to_mars.py

# *************************************
# *************************************