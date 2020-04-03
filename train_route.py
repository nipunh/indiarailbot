import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config


def train_rt(info):
	result = {"response_code":None, "result":None}
	train_num = info["train_num"]
	# train_num = info["train_num"]
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('chromedriver',chrome_options=options)
	try:
		driver.get('https://www.trainspnrstatus.com/train-schedule');

		elem = driver.find_element_by_id("tags")
		elem.send_keys(train_num)

		searchButton= driver.find_element_by_xpath('//*[@id="contact_form"]/div/button')
		searchButton.click()

		element = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/table/thead')
		html = element.get_attribute('outerHTML')
		element1 = driver.find_element_by_xpath('/html/body/div/div/div[1]/div[3]/table/tbody')
		html1 = element1.get_attribute('outerHTML')
		result["response_code"] = 200
		result["result"] = html+html1
		return(result)
	except Exception as e:
		result["response_code"] = 503
		return(result)
	finally:
		driver.close	
