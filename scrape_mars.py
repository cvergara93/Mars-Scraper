import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import time

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def scrape():
    final_data = {}
    output = MarsNews()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars__featured_image"] = MarsFeaturedImage()
    final_data["mars_weather"] = MarsWeather()
    final_data["mars_facts"] = MarsFacts()
    final_data["mars_hemisphere_imgs"] = MarsHems()
    return final_data

def MarsNews():
    n_url = "https://mars.nasa.gov/news/"
    browser.visit(n_url)
    time.sleep(1)
    n_html = browser.html
    n_soup = BeautifulSoup(n_html, "html.parser")
    article = n_soup.find("div", class_='list_text')
    n_title = article.find("div", class_="content_title").text
    n_par = article.find("div", class_ ="article_teaser_body").text
    output = [n_title, n_par]
    return output

def MarsFeaturedImage():
    i_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(i_url)
    time.sleep(3)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    i_html = browser.html
    i_soup = BeautifulSoup(i_html, "html.parser")
    extension = i_soup.find("img", class_="main_image")["src"]
    featured_image_url = f"https://www.jpl.nasa.gov{extension}"
    return featured_image_url

def MarsWeather():
    w_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(w_url)
    w_html = browser.html
    w_soup = BeautifulSoup(w_html, "html.parser")
    tweets = w_soup.find_all('div', class_="js-tweet-text-container")
    mars_weather = tweets[0].text.split('pic.twitter', 1)[0]
    return mars_weather

def MarsFacts():
    f_url = "https://space-facts.com/mars/"
    tables = pd.read_html(f_url)
    facts_df = tables[0]
    facts_df.columns = ["Parameter", "Value"]
    facts_df.set_index("Parameter", inplace=True)
    mars_facts = facts_df.to_html(index = True, header =True)
    return mars_facts

def MarsHems():
    h_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(h_url)
    hemisphere_image_urls = []
    for x in range (0,4):
        time.sleep(2)
        images = browser.find_by_tag('h3')
        images[x].click()
        new_html = browser.html
        new_soup = BeautifulSoup(new_html, 'html.parser')
        partial = new_soup.find("img", class_="wide-image")["src"]
        img_title = new_soup.find("h2",class_="title").text.replace("Enhanced", "").strip()
        img_url = 'https://astrogeology.usgs.gov'+ partial
        dictionary = {"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
        browser.back()
    return hemisphere_image_urls