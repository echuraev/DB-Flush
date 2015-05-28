import os
import time
import sqlite3 
from datetime import datetime
from selenium import webdriver

URL = 'http://www.nasdaq.com/symbol/aapl/real-time'
SLEEP_TIME = 30 #60 #min
DB_FILE = './stock_quotes.db'

if __name__ == '__main__':
    while True:
        if not os.path.isfile(DB_FILE):
            conn = sqlite3.connect(DB_FILE)
            conn.execute('''CREATE TABLE raw_data (id integer primary key, value double, time timestamp)''')
            conn.close()
            
        conn = sqlite3.connect(DB_FILE)
        
        os.environ['http_proxy'] = ""
        os.environ['https_proxy'] = ""
        fp = webdriver.FirefoxProfile()
        fp.set_preference("network.proxy.type", 2)
        fp.set_preference("network.proxy.autoconfig_url",
                          "http://autoproxy.intel.com/")
        browser = webdriver.Firefox(firefox_profile=fp)
        browser.get(URL)
       
        line = '<div class="qwidget-dollar" id="qwidget_lastsale">$'
        source = str(browser.page_source)
        source = source[source.find(line) + len(line):]
        price = source[:source.find('</div>')]
        
        conn.execute("INSERT INTO raw_data(value, time) values (?, ?)", (float(price), datetime.now()))
        conn.commit()

        browser.quit()
        print("Collected data! Price: " + price)
        time.sleep(SLEEP_TIME * 60)
        
        conn.close()
