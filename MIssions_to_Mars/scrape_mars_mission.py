# Dependencies
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


def scrape():
    
    mars_data = {}
    
    # Url of website to be scraped
    url = 'https://mars.nasa.gov/news/'
    response = requests.get(url)
    soup =  BeautifulSoup(response.text, 'html.parser')

    # get the latest news title
    news_title = soup.find('div', class_="content_title").text.strip()

    # Get latest news paragraph text
    news_p = soup.find('div', class_="rollover_description").text.strip()


    # Url of JPL Featured Space Image to scrape
    url = 'https://www.jpl.nasa.gov'
    query = '/spaceimages/?search=&category=Mars'
    response = requests.get(url+query)
    soup =  BeautifulSoup(response.text, 'html.parser')

    # Get image url
    image = soup.find('div', class_="carousel_items") 
    featured_image_url = url+image.a['data-fancybox-href']


    # Trick Twitter to bypass Javascript check to get Mars Weather
    user_agent_old_phone = 'Nokia5310XpressMusic_CMCC/2.0 (10.10) Profile/MIDP-2.1 '\
    'Configuration/CLDC-1.1 UCWEB/2.0 (Java; U; MIDP-2.0; en-US; '\
    'Nokia5310XpressMusic) U2/1.0.0 UCBrowser/9.5.0.449 U2/1.0.0 Mobile'

    headers = { 'User-Agent': user_agent_old_phone}

    # Scrape twitter for Mars Weather
    url_twitter = 'https://twitter.com/marswxreport?lang=en'
    resp = requests.get(url_twitter, headers=headers)  # Send request

    code = resp.status_code  # HTTP response code
    if code == 200:
        soup = BeautifulSoup(resp.text, 'lxml')  # Parsing the HTML
        #print(soup.prettify())
    else:
        print(f'Error to load Twitter: {code}')
      
        
    # Get Mars weather
    mars_weather = soup.find(text=re.compile("InSight"));

    # Get Mars facts data from webpage
    url = 'https://space-facts.com/mars/'
    response = requests.get(url)
    soup =  BeautifulSoup(response.text, 'html.parser')

    # Get table data 
    #table = soup.find_all('tr')
    table = soup.find(id="tablepress-p-mars-no-2")



    # Get Mars facts data from webpage and convert to html table string
    url = 'https://space-facts.com/mars/'

    # Scrape using pandas
    tables = pd.read_html(url)
    mars_facts = tables[2]
    

    mars_facts.columns = ['Description', 'Value']
    mars_facts.set_index('Description', inplace=True)

    # Convert to html string
    mars_facts_html = mars_facts.to_html()


    # Url for main page 
    url_main ='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Python dictionary with urls for pictures of each of Mars' Hemispheres
    hemisphere_image_urls = [
        {"title": "Cerberus Hemisphere Enhanced", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere Enhanced", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis_Major Hemisphere Enhanced", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"},
        {"title": "Valles_Marineris Hemisphere Enhanced", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"}
    ]
    
    mars_data["news_title"] = news_title
    mars_data["news_p"] = news_p
    mars_data["featured_image_url"] =  featured_image_url
    mars_data["mars_weather"] = mars_weather
    #mars_data["mars_facts"] = mars_facts
    mars_data["mars_facts_html"] = mars_facts_html
    mars_data["hemisphere_image_urls"] = hemisphere_image_urls
        
    # Return Results
    return mars_data

