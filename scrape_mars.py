from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit web page
    url_mars = 'https://mars.nasa.gov/news/'
    browser.visit(url_mars)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    slide_element = soup.select_one("ul.item_list li.slide")
    latest_news_title = slide_element.find("div", class_="content_title").get_text()
    latest_news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
  # Close the browser after scraping
    browser.quit()



    
    
    browser = init_browser()
    url_JPL_Mars = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    img_base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url_JPL_Mars)
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.select('a',class_="button fancybox")
    link_list=[]
    for result in results:
    # Error handling
      try:
        img_list = result.get('data-fancybox-href')
               
        if img_list:
          link_list.append(img_list)
           
         
      except Exception as e:
        print(e)
    featured_image_url = img_base_url + link_list[0]
    
    browser.quit()


    browser = init_browser() 
    tweet_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(tweet_url)
    time.sleep(3)
    html = browser.html
    soup = bs(html, 'html.parser')
    mars_weather_tweet = soup.find("div", attrs={"class": "tweet", "data-name": "Mars Weather"})
    try:
      mars_weather = mars_weather_tweet.find("p", "tweet-text").get_text()
    except AttributeError:
      pattern = re.compile(r'sol')
      mars_weather = soup.find('span', text=pattern).text
    
 



    
    url_pandas ="https://space-facts.com/mars/"
    tables = pd.read_html(url_pandas)
    df = tables[0]
    df.columns = ['Description', 'Value']
    df = df.set_index('Description') 
    result = df.to_html(header="true", table_id="table")

    browser = init_browser()
    
    
    usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(usgs_url)
    soup = bs(browser.html, 'html.parser')
    hemispheres = soup.select('div.item')  
    List=[]
    hemisphere_title=[]
    for x in range (4):
        xpath = '//div//a[@class="itemLink product-item"]/img'
        results = browser.find_by_xpath(xpath)
        img = results[x]
        img.click()
        #make new soup of that page
        soup1 = bs(browser.html, 'html.parser')
        #find the full image
        full = soup1.find('a', text='Sample')
        #get the img url
        img_url = full['href']
        hemisphere_title.append(hemispheres[x].h3.text)
        List.append(img_url)
        browser.back()   
    lista=[]
    for x in range(4):
    	prueba= {}   
    	prueba['foto']= List[x] 
    	prueba['titulo']= hemisphere_title[x]
    	lista.append(prueba)    


	




      # Store data in a dictionary
    mars_data = {
        "news_title": latest_news_title,
        "news_text": latest_news_paragraph,
        "img_link": featured_image_url,
        "weather": mars_weather,
        "tabla":result,
		"hem":lista 
        }
    
    
    
    # Return results
    return mars_data








