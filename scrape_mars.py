from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def Scrape_All():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scrape News Title data
    news_title = scrape_news_title(browser)

    # Scrape News Description data
    news_p = scrape_news_paragraph(browser)

    # Scrape Featured Image URL
    featured_image_url = scrape_featured_img_url(browser)

    # Scrape facts page HTML 
    facts = scrape_facts_page(browser)

    # Iterate and scrape hemisphere image URLs
    hemisphere_image_urls = scrape_facts_hemis_url(browser)

    # Store results in Dictionary 
    result = {
            "news_title": news_title,
            "news_summary": news_p,
            "featured_image_url": featured_image_url,
            "facts_table_html": facts,
            "hemisphere_image_urls": hemisphere_image_urls
        }

    # Close browser
    browser.quit()

    # Return results
    return result

def scrape_news_title(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    html1 = browser.html
    soup = bs(html1, "html.parser")

     ## Set news paragraph by using beautiful soup to scrape first index of div & class name
    news_title = [i.text for i in soup.select('div.content_title')][0]

    return news_title


def scrape_news_paragraph(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    html1 = browser.html
    soup = bs(html1, "html.parser")

     ## Set news paragraph by using beautiful soup to scrape first index of div & class name
    news_p = [i.text for i in soup.select('div.article_teaser_body')][0]

    return news_p


def scrape_featured_img_url(browser):
    url = 'https://spaceimages-mars.com'
    browser.visit(url)
    time.sleep(1)
    html1 = browser.html
    soup = bs(html1, "html.parser")

    ## Set URL by using bs to scrape first img index & getting the src URL
    featured_image_url = url + "/" + [i for i in soup.select('img.headerimage')][0].get('src')

    return featured_image_url

def scrape_facts_page(browser):
    url = 'https://galaxyfacts-mars.com'
    browser.visit(url)
    
    html = browser.html
    fact_soup = bs(html, 'html.parser')

    factslocation = fact_soup.find('div', class_="diagram mt-4")
    factTable = factslocation.find('table')

    facts = ""

    facts += str(factTable)

    return facts

def scrape_facts_hemis_url(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    hemisphere_image_urls = []

    for i in range(4):

        hemisphereInfo = {}

        browser.find_by_css("a.product-item img")[i].click()

        sample = browser.links.find_by_text('Sample').first

        hemisphereInfo["img_url"] = sample[ 'href']

        hemisphereInfo['title'] = browser.find_by_css('h2.title').text

        hemisphere_image_urls.append(hemisphereInfo)

        browser.back()

    return hemisphere_image_urls