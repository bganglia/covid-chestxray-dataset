import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
import sys

browser_downloads = os.path.join(os.path.dirname(__file__),"downloads")

options = webdriver.ChromeOptions()
options.gpu = False
options.headless = False
options.add_experimental_option("prefs", {
    "download.default_directory" : browser_downloads,
    'profile.default_content_setting_values.automatic_downloads': 2,
})

chrome_path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"chromedriver")
print(chrome_path)


desired = options.to_capabilities()
desired['loggingPrefs'] = { 'performance': 'ALL'}
browser = webdriver.Chrome(desired_capabilities=desired,
                           executable_path=chrome_path)


def format_search_url(search_terms):
    return "https://www.eurorad.org/advanced-search?search=" + "+".join(search_terms)

def extract_results_from_search_page():
    out = []
    for a in browser.find_elements_by_xpath("//a[contains(@href,'/case/')]"):
        out.append(a.get_attribute("href"))
    return list(set(out))

def get_next_search_page():
    try:
        next_ref = browser.find_element_by_xpath(
            "//div[@class='pagination']/a[@title='Go to next page']"
        )
        return next_ref.get_attribute("href")
    except:
        return None

def get_search_results(search_terms):
    next_search_page = format_search_url(search_terms)
    while next_search_page:
        browser.get(next_search_page)
        yield from extract_results_from_search_page()
        next_search_page = get_next_search_page()

def metadata_from_result_page():

    title = browser.find_element_by_xpath("//title").text

    demographics = browser.find_element_by_xpath("//p[@class='color-grey']").text

    standard_keys = [
        'CLINICAL HISTORY',
        'IMAGING FINDINGS',
        'DISCUSSION',
        'FINAL DIAGNOSIS'
    ]

    out = {}

    for subsection in browser.find_elements_by_xpath("//div[@class='row' and div/@class='col-12 col-md-3']"):
        key = subsection.find_element_by_xpath("div[@class='col-12 col-md-3']").text
        value = subsection.find_element_by_xpath("div[@class='col-12 col-md-9']").text
        if key in standard_keys:
            out[key] = value
        if key == "DIFFERENTIAL DIAGNOSIS LIST":
            out[key] = value.split("\n")
    return out

def metadata_from_search_terms(search_terms):
    result_pages = list(get_search_results(search_terms))
    print(result_pages)
    for result_page in result_pages:
        browser.get(result_page)
        yield metadata_from_result_page()

if __name__ == "__main__":
    print("Searching for COVID images...")
    for i in metadata_from_search_terms(["COVID"]):
        print("Press Enter to see next metadata entry")
        input()
        print(i)
