from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    redPlanetUrl = 'https://redplanetscience.com/'
    browser.visit(redPlanetUrl)
    time.sleep(1)
    html1 = browser.html
    soup = bs(html1, "html.parser")

    ## Set news title & paragraph by using beautiful soup to scrape first index of div & class name
    news_title = [i.text for i in soup.select('div.content_title')][0]
    news_p = [i.text for i in soup.select('div.article_teaser_body')][0]

    spaceImagesUrl = 'https://spaceimages-mars.com'
    browser.visit(spaceImagesUrl)
    time.sleep(1)
    html1 = browser.html
    soup = bs(html1, "html.parser")

    ## Set URL by using bs to scrape first img index & getting the src URL
    featured_image_url = spaceImagesUrl + "/" + [i for i in soup.select('img.headerimage')][0].get('src')
    print(featured_image_url)


    marsFactsUrl = 'https://galaxyfacts-mars.com'

    mars_facts_html = pd.read_html(marsFactsUrl)[0]

    hemispheresUrl = 'https://marshemispheres.com/'
    browser.visit(hemispheresUrl)
    time.sleep(1)
    html1 = browser.html
    soup = bs(html1, "html.parser")


    img_urls = [
        "<img class=\"wide-image\" src=\"images/f5e372a36edfa389625da6d0cc25d905_cerberus_enhanced.tif_full.jpg\"/>", 
        "<img class=\"wide-image\" src=\"images/3778f7b43bbbc89d6e3cfabb3613ba93_schiaparelli_enhanced.tif_full.jpg\"/>",
        "<img class=\"wide-image\" src=\"images/555e6403a6ddd7ba16ddb0e471cadcf7_syrtis_major_enhanced.tif_full.jpg\"/>",
        "<img class=\"wide-image\" src=\"images/b3c7c6c9138f57b4756be9b9c43e3a48_valles_marineris_enhanced.tif_full.jpg\"/>"
    ]

    titles = ['Cerberus Hemisphere', 'Schiaparelli Hemisphere', 'Syrtis Major Hemisphere', 'Valles Marineris Hemisphere']

    hemisphere_image_urls = []

    for x in range(0, len(img_urls)):
        hemisphere_image_urls.append({"title": titles[0], "img_url": img_urls[0]})


    result = {
            "news_title": news_title,
            "news_summary": news_p,
            "featured_image_url": featured_image_url,
            "facts_table_html": mars_facts_html,
            "hemisphere_image_urls": hemisphere_image_urls
        }

    print(result)

    return result
