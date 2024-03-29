import requests


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup




def get_driver(driver_url):
    # initialize options
    options = webdriver.ChromeOptions()
    # pass in headless argument to options
    options.add_argument('--headless')
    # initialize driver
    driver = webdriver.Chrome(options=options, executable_path=driver_url)
    return driver


def connect_to_site(browser, base_url):
    connection_attempts = 0
    while connection_attempts < 3:
        try:
            browser.get(base_url)
            # wait for table element with id = 'flugdaten-abflug' to load
            # before returning True


            WebDriverWait(browser, timeout=10).until(
                EC.visibility_of_element_located((By.ID, 'flugdaten-abflug'))
            )

            return True
        except Exception as ex:
            connection_attempts += 1
            print(f'Error connecting to (base_url).')
            print(f'Attempt #{connection_attempts}.')
            return False


def parse_html(html):
    # create soup object
    soup = BeautifulSoup(html, 'html.parser')
    output_list = []

    try:

        # parse soup object to get row cel td2
        # todo maybe use "detail_info" for more precise location
        #div_blocks = soup.find_all(class_="detail-table__cell text-uppercase fdabf-td2")
        div_blocks = soup.find_all("div",class_="details__info")

        for div in div_blocks:

            span=div.find("span", text="Stadt, Land:")

            if span is not None:
                location=span.find_next_sibling("span").string
                if location not in output_list:
                    output_list.append(location)



    except Exception as ex:
        print(f'Parsing failed (ex)')
    return output_list


def get_load_time(article_url):
    try:
        # set headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        # make get request to url
        response = requests.get(
            article_url, headers=headers, stream=True, timeout=3.000)
        # get page load time
        load_time = response.elapsed.total_seconds()
    except Exception as ex:
        load_time = 'Loading Error'

    return load_time


