import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
import signal
import time
from selenium.webdriver.chrome.options import Options

def fare_enquiry(info):
	train_num = info["train_num"]
	src_stn = info["src_stn"]
	dest_stn = info["dest_stn"]
	# train_num = "11077" 
	# src_stn = "PUNE"
	# dest_stn = "BPL"
	options = Options()
	options.add_argument('headless')
	options.add_argument('window-size=1920x1080')
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('chromedriver',options=options)  # Optional argument, if not specified will search path.
	driver.get('https://indianrailways.info/fare_enquiry');

	result = {"response_code":None, "result":None}
	try:
		# driver.manage().timeouts().pageLoadTimeout(30, TimeUnit.SECONDS);
		elem = driver.find_element_by_id("train_no")
		elem.send_keys(train_num)

		elem1 = driver.find_element_by_id("from_station_code")
		elem1.send_keys(src_stn)

		elem2 = driver.find_element_by_id("to_station_code")
		elem2.send_keys(dest_stn)

		searchButton= driver.find_element_by_xpath('//*[@id="submitform"]/div[2]/button')
		searchButton.click()

		driver.implicitly_wait(20)
		
		status = driver.find_element_by_xpath('//*[@id="showrest"]/div[4]/div[1]/div/div[2]/table/tbody')
		html2 = status.get_attribute('outerHTML')
		tablehead = driver.find_element_by_xpath('//*[@id="showrest"]/div[4]/div[2]/div/div[2]/table/thead')
		html3 = tablehead.get_attribute('outerHTML')
		tableData = driver.find_element_by_xpath('//*[@id="showrest"]/div[4]/div[2]/div/div[2]/table/tbody')
		html4 = tableData.get_attribute('outerHTML')
		result =  {"response_code":200,"result":{"status": html2, "tablehead":html3, "tableData" : html4}}
		return(result)

	except Exception as e:
		result["response_code"] = 503
		return(result) 	

	finally:
		driver.close()	

