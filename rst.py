import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys




def train_rst(info):
	train_num = info["train_num"]
	# train_num = "11077"
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('chromedriver')#,chrome_options=options)  # Optional argument, if not specified will search path.
	driver.get('https://www.traininfo.in/running-status');

	elem = driver.find_element_by_xpath('//*[@id="train"]')
	elem.send_keys(train_num)
	
	searchButton= driver.find_element_by_xpath('/html/body/div[1]/div/form/div[2]/button')
	searchButton.click()

	driver.implicitly_wait(30)
	element1 = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[2]')
	html1 = element1.get_attribute('outerHTML')
	element2 = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]')
	html2 = element2.get_attribute('outerHTML')
	element3 = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[4]')
	html3 = element3.get_attribute('outerHTML')
	driver.close()
	return(html1+html2+html3)


