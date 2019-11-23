import datetime
from itertools import repeat
from time import sleep, time
from multiprocessing import Pool, cpu_count
from py_expression_eval import Parser

from scrapers.scraper import get_driver, connect_to_base, \
    parse_html

from storages.storage import create_connection,create_table,data_entry,data_print

#load from config

page_url="https://www.viennaairport.com/passagiere/ankunft__abflug/abfluege"
driver_url="D:\Projects\PythonScraper\chromedriver.exe"
db_url= r"D:\Projects\PythonScraper\scrapped.db"

#api.openweathermap.org/data/2.5/weather?q=Bitola&appid=4832c5bf5984665cd39ee2d7308311ac

#from .csv or .db
#4832c5bf5984665cd39ee2d7308311ac
#if >25 C in London, note = "Let's go for a pint" ○ if <5 C in Madrid, note = "!Que frio!"
note_rules=[]
note_rules.append({"rule":"t>25 and city=='London'","note":"Let's go for a pint"})
note_rules.append({"rule":"t<5 and city=='Madrid'","note":"!Que frio!"})
#note_rules.append({"rule":"city=='London'","note":"Let's go for a pint"})


#print(parser.parse(note_rules[0]['rule']).evaluate({"t":3,"city":'London'}))


#destination, time, temperature and note into a database
sql_create_scrapped_table = """ CREATE TABLE IF NOT EXISTS scrapped (
                                        id integer PRIMARY KEY,
                                        destination text NOT NULL,
                                        time text,
                                        temperature integer,
                                        note text
                                    ); """

sql_insert_scrapped_table="INSERT INTO scrapped (destination, time, temperature, note) VALUES (?,?,?,?)"


def evaluate_rules(dest,temp,n_rules):

    parser = Parser()

    for note_rule in n_rules:
        if parser.parse(note_rule['rule']).evaluate({"t":temp,"city":dest}):
            return note_rule.note

    return ''

def run_process(p_url,d_url, db_url):
    browser = get_driver(driver_url)
    if connect_to_base(browser, p_url):
        #sleep(2)
        html = browser.page_source
        cities=parse_html(html)

        for city in cities:
            print(city)



        #create a database connection
        conn = create_connection(db_url)


        if conn is not None:
            #
            create_table(conn,sql_create_scrapped_table)
            data_entry(conn,sql_insert_scrapped_table,[city,datetime.datetime.now().strftime('%Y%m%d%H%M%S'),12,"test note"])
            data_print(conn,"scrapped")
        else:
            print("Error! cannot create the database connection.")





        #print(html)
        browser.quit()
    else:
        print('Error connecting to [p_url]')
        browser.quit()


if __name__ == '__main__':
    # set variables
    start_time = time()
    output_timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f'output_{output_timestamp}.csv'

    #browser = get_driver(driver_url)
    #result=connect_to_base(browser, base_url)

    run_process(page_url,driver_url,db_url)

    #print(result)

    # scrape and crawl
    #with Pool(cpu_count()-1) as p:
    #    p.starmap(run_process, zip(range(1, 21), repeat(page_url,driver_url,db_url)))
    #p.close()
    #p.join()
    end_time = time()
    elapsed_time = end_time - start_time
    print(f'Elapsed run time: {elapsed_time} seconds')
