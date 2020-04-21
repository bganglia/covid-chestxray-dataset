#WARNING: This code is very incomplete! I am just uploading it to be comprehensive

import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import numpy as np
import sys
import time

from urllib3.exceptions import ProtocolError


def wait():
    time.sleep(np.random.uniform(3, 5, 1)[0])

browser_downloads = os.path.join(os.path.dirname(__file__),"downloads")

options = webdriver.ChromeOptions()
options.gpu = False
options.headless = False
options.add_experimental_option("prefs", {
    "download.default_directory" : browser_downloads,
    'profile.default_content_setting_values.automatic_downloads': 2,
})

chrome_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"../chromedriver")
print(chrome_path)


desired = options.to_capabilities()
desired['loggingPrefs'] = { 'performance': 'ALL'}
browser = webdriver.Chrome(desired_capabilities=desired,
                           executable_path=chrome_path)

def safe_get(url):
    wait()
    try:
        browser.get(url)
    except ProtocolError:
        assert browser.current_url == url

def format_radiopaedia_search_url(search_terms, scope):
    base_url = "https://radiopaedia.org/search?utf8=%E2%9C%93&q={}&scope={}&lang=us"
    return base_url.format("+".join(search_terms), scope)

def format_search_url(search_terms):
    return format_radiopaedia_search_url(search_terms, "cases")

#def format_playlist_search_url(search_terms):
#    return format_radiopaedia_search_url(search_terms, "cases")

def extract_results_from_search_page():
    out = []
    #Yield from playlists
    #Yield cases
    for a in browser.find_elements_by_xpath("//a[contains(@href,'/cases/') and @class = 'search-result search-result-case']"):
        out.append(a.get_attribute("href"))
    return list(set(out))

def get_next_search_page():
    try:
        next_ref = browser.find_element_by_xpath(
            "//a[@class='next_page']"
        )
        return next_ref.get_attribute("href")
    except:
        return None

def get_search_results(search_terms):
    next_search_page = format_search_url(search_terms)
    while next_search_page:
        browser.get(next_search_page)
        wait()
        yield from extract_results_from_search_page()
        next_search_page = get_next_search_page()
        print("Proceed to next?", next_search_page)
        if input() == "n":
            break

def metadata_from_result_page():

    title = browser.find_element_by_xpath("//title").text

    demographics = browser.find_element_by_xpath("//p[@class='color-grey']").text

    standard_keys = [
        'CLINICAL HISTORY',
        'IMAGING FINDINGS',
        'DISCUSSION',
        'FINAL DIAGNOSIS'
    ]

    image_xpath = "//img[starts-with(@data-src,'/sites/default/files/styles/figure_image/public/')]"
    image_description_xpath = "//span[@class='mb-1 d-block']"

    images = browser.find_elements_by_xpath(image_xpath)
    image_descriptions = browser.find_elements_by_xpath(image_description_xpath)

    images = [image.get_attribute("data-src") for image in images]
    #Image descriptions broken?
    image_descriptions = [image_description.text for image_description in image_descriptions]

    out = {}

    out["images"] = images
    out["image_descriptions"] = image_descriptions

    for subsection in browser.find_elements_by_xpath("//div[@class='row' and div/@class='col-12 col-md-3']"):
        key = subsection.find_element_by_xpath("div[@class='col-12 col-md-3']").text
        value = subsection.find_element_by_xpath("div[@class='col-12 col-md-9']").text
        if key in standard_keys:
            out[key] = value
        if key == "DIFFERENTIAL DIAGNOSIS LIST":
            out[key] = value.split("\n")
    return out

search_terms = ["COVID"]
#result_pages = list(get_search_results(search_terms))
#print(result_pages)


def metadata_from_search_terms(search_terms):
    result_pages = list(get_search_results(search_terms))
    print(result_pages)
    for result_page in result_pages:
        browser.get(result_page)
        wait()
#        yield metadata_from_result_page()

#browser.get(format_search_url(search_terms))

#print(extract_results_from_search_page())

#print(get_next_search_page())

print(list(get_search_results(search_terms)))

#a = metadata_from_search_terms(["COVID"])

#browser.get("https://www.eurorad.org/advanced-search?search=COVID")

#for a in browser.find_elements_by_xpath("//a[contains(@href,'/case/')]"):
#    browser.get(a.get_attribute("href"))
#    break

#print(a)
#for i in a:
#    print(i.get_attribute("href"))

#url = a.get_attribute("href")

#    yield url
#    yield from iterate_results_pages(start_page)

#print(list(iterate_results_pages(start_page)))

#CLINICAL HISTORY

#/home/compssd1/Documents/proj/open_source/bio/wuhan/scrapers/chromedriver

#CLINICAL HISTORY
#IMAGING FINDINGS
#DISCUSSION
#FINAL DIAGNOSIS
#DIFFERENTIAL DIAGNOSIS LIST

#for image_section in browser.find_elements_by_xpath("//div[@class='figure-gallery__item__label' and imgfoaf:Image

#browser.get("https://radiopaedia.org/cases/covid-19-pneumonia-66?lang=us")

#print([i.text for i in browser.find_elements_by_xpath("//div[@class='data-item']")])

#presentation = browser.find_element_by_xpath("//div[@class='case-section view-section']")
#print("presentation", presentation.text)
