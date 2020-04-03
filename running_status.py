import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import json




def train_rst(info):
	train_num = info["train_num"]
	# train_num =  "22686"
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.
	driver.get('https://runningstatus.in/');
	result = {"response_code": None, "result":None}
	try:
		elem = driver.find_element_by_xpath("/html/body/div[1]/div/div/header/div/div/div[1]/form/div/input")
		elem.send_keys(train_num)

		searchButton= driver.find_element_by_xpath('/html/body/div[1]/div/div/header/div/div/div[3]/div/span/button')
		searchButton.click()

		driver.implicitly_wait(30)
		trainDetails = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/div[1]/h1')
		html1 = trainDetails.get_attribute('outerHTML')
		status = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/div[1]/strong')
		html2 = status.get_attribute('outerHTML')
		tableHead = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/div[2]/table/thead[1]')
		html3 = tableHead.get_attribute('outerHTML')
		tableData = driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div/div[1]/div/div[2]/table/tbody')
		html4 = tableData.get_attribute('outerHTML')
		result =  {"response_code":200, "result" : {"trainDetails": html1, "status": html2, "tableHead": html3, "tableData" : html4}}
		driver.close()
		return(result)

	except Exception as e:
		result["response_code"] = 503
		return (result)