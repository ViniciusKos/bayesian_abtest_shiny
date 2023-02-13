from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import numpy as np
import time

chr_options = Options()
chr_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), chrome_options=chr_options)
driver.get("http://127.0.0.1:5000/home")

clicks = 10000
for click in range( clicks ):
    if np.random.random() < 0.5:
        driver.find_element( 'name', 'yescheckbox').click()
        driver.find_element( 'id', 'yesbtn').click()
        time.sleep(2)
    else:
        driver.find_element( 'name', 'nocheckbox').click()
        driver.find_element( 'id', 'nobtn').click()
        time.sleep(2)