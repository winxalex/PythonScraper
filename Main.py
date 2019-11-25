import datetime

from time import time
import requests_cache
from py_expression_eval import Parser
import pyowm
from scrapers.scraper import get_driver, connect_to_site, \
    parse_html
import threading

from storages.storage import create_connection, create_table, \
    data_entry, data_print, data_delete

#todo load from config

page_url = "https://www.viennaairport.com/passagiere/ankunft__abflug/abfluege"
driver_url = "D:\Projects\PythonScraper\chromedriver.exe"
database_url = r"D:\Projects\PythonScraper\scrapped.db"
weather_app_id = '4832c5bf5984665cd39ee2d7308311ac'
sql_table_name = "scrapped"

#destination, time, temperature and note into a database
sql_create_scrapped_table = """ CREATE TABLE IF NOT EXISTS scrapped (
                                        id integer PRIMARY KEY,
                                        destination text NOT NULL,
                                        time text,
                                        temperature integer,
                                        note text
                                    ); """

sql_insert_scrapped_table = "INSERT INTO scrapped (destination, time, temperature, note) VALUES (?,?,?,?)"

#from .csv or .db
#if >25 C in London, note = "Let's go for a pint" ○ if <5 C in Madrid, note = "!Que frio!"
note_rules = list()
note_rules.append({"rule": "t>25 and city=='London'", "note": "Let's go for a pint"})
note_rules.append({"rule": "t<10 and city=='London'", "note": "Frizzing"})
note_rules.append({"rule": "t<5 and city=='Madrid'", "note": "!Que frio!"})
note_rules.append({"rule": "t<5 and city=='Moskau'", "note": "!FFFFFF!"})


#print(parser.parse(note_rules[0]['rule']).evaluate({"t":3,"city":'London'}))



















def get_temp(o, loc):
    try:
        # Search for current weather in
        observation = o.weather_at_place(loc)

        w = observation.get_weather()

        return w.get_temperature('celsius')['temp']

    except Exception as ex:
        print("Retrieving temperature failed for location " + loc)
    return -255


def evaluate_rules(city, temp, n_rules):
    parser = Parser()

    for note_rule in n_rules:
        if parser.parse(note_rule['rule']).evaluate({"t": temp, "city": city}):
            return note_rule["note"]

    return ''


def run_process(p_url, d_url, db_url):

    browser = get_driver(d_url)

    if connect_to_site(browser, p_url):

        html = browser.page_source

        #print(html)
        locations = parse_html(html)

        #print(locations)

        owm = pyowm.OWM(weather_app_id)  # You MUST provide a valid API key

        #create a database connection
        conn = create_connection(db_url)

        if conn is not None:

            data_delete(conn, sql_table_name)

            #
            create_table(conn, sql_create_scrapped_table)
            #data_entry(conn,sql_insert_scrapped_table,[city,datetime.datetime.now().strftime('%Y%m%d%H%M%S'),12,"test note"])

            for location in locations:
                temp = get_temp(owm, location)
                if temp > -255:
                    city = location.split(',')[0]
                    data_entry(conn, sql_insert_scrapped_table,
                               [city, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), temp,
                                evaluate_rules(city, temp, note_rules)])

            data_print(conn, sql_table_name)

            conn.close()
        else:
            print("Error! cannot create the database connection.")

        #print(html)
        browser.quit()
    else:
        print('Error connecting to [p_url]')
        browser.quit()


def scrap_process():
    start_time = time()

    run_process(page_url, driver_url, database_url)

    end_time = time()
    elapsed_time = end_time - start_time
    print(f'Elapsed run time: {elapsed_time} seconds')

def scrap_every(sec):
    threading.Timer(sec, scrap_every, args=[sec]).start()
    scrap_process()

requests_cache.install_cache(expire_after=3600)  #after 1hour

#every hour
#from crontab import CronTab
#
#cron = CronTab(user='username')
#job = cron.new(command='E:\\Program Files\\Python3.8\\python D:\\Projects\\PythonScraper\\everyHour.py')
#job.hour.every(1)
#
#cron.write()
#scrap_every(3600)
scrap_every(5)

