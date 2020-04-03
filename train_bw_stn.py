import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config
from selenium.webdriver.chrome.options import Options



def train_bw_stn(info):
	src_stn = info["src_stn"]
	dst_stn= info["dest_stn"]
	# src_stn="BPL"
	# dst_stn="PUNE"
	# # train_num = info["train_num"]
	options = Options()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	options.add_argument("--log-level=3")
	# options.page_load_strategy = 'eager'
	driver = webdriver.Chrome('chromedriver',options=options)  # Optional argument, if not specified will search path.
	

	result={"response_code":None, "result":None}

	try:
		driver.get('https://runningstatus.in/trains');
		stn= driver.find_element_by_xpath('/html/body/div[2]/div/div/header/div/div/div[1]/form/div/input')
		stn.send_keys(src_stn)
		stn2= driver.find_element_by_xpath('/html/body/div[2]/div/div/header/div/div/div[2]/div/input')
		stn2.send_keys(dst_stn)

		searchButton= driver.find_element_by_xpath('/html/body/div[2]/div/div/header/div/div/div[5]/div/span/button')
		searchButton.click()
		driver.implicitly_wait(30)
		element1 = driver.find_element_by_xpath('//*[@id="accordion"]')
		html = element1.get_attribute('outerHTML')
		result["response_code"] = 200
		result["result"] = html
		return(result)

	except Exception as e :
		result["response_code"] = 503
		return(result)

	finally:
		driver.close()





