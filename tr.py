import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config




def train_rt(info):
	train_num = info["train_num"]
	# train_num = info["train_num"]
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	driver = webdriver.Chrome('C:/Users/Nipun Hedaoo/AppData/Local/Google/Chrome/chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.
	driver.get('https://www.traininfo.in/train-schedule');

	elem = driver.find_element_by_id("train")
	elem.send_keys(train_num)

	searchButton= driver.find_element_by_xpath('/html/body/div[1]/div/div/div/form/div[2]/button')
	searchButton.click()

	element = driver.find_element_by_xpath('/html/body/div[3]/div/div[1]/div/div[3]')
	html = element.get_attribute('outerHTML')
	driver.close()
	return(html)

