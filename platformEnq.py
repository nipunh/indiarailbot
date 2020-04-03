import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config




def platform_enquiry(info):
	# train_num = "22686"
	# stn_code = "BPL"
	train_num = info["train_num"]
	stn_code=info["station_code"]
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.
	result={"response_code":None, "result":{"trainDetails":None,"platform":None}}
	try:
		driver.get('https://pnrstatuslive.com/platform-enquiry/');

		elem = driver.find_element_by_id("train_num")
		elem.send_keys(train_num)

		elem1 = driver.find_element_by_id("train_station")
		elem1.send_keys(stn_code)

		searchButton= driver.find_element_by_xpath('//*[@id="train_form"]/div/input')
		searchButton.click()

		driver.implicitly_wait(10)
		element = driver.find_element_by_xpath('//*[@id="platform_enquiry_load"]/div[1]/div/h3/span')
		html = element.get_attribute('outerHTML')
		element1 = driver.find_element_by_xpath('//*[@id="platform_enquiry_load"]/div[2]/div/div[1]/span[1]')
		html1 = element1.get_attribute('outerHTML')
		result["response_code"] = 200
		result["result"]["trainDetails"] = html
		result["result"]["trainDetails"] = html1
		return(result)
	except:
		result["response_code"] = 503
		return(result)
	finally:	
		driver.close()
	



