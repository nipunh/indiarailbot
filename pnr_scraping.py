import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config



def pnr_enqiury(info):
	pnr = info["pnr_number"]
	options = webdriver.ChromeOptions()
	options.add_argument('headless')
	options.add_argument('window-size=1200x600')
	options.add_argument("--log-level=3")
	driver = webdriver.Chrome('chromedriver',chrome_options=options)  # Optional argument, if not specified will search path.
	driver.get('https://www.trainspnrstatus.com/')
	result = {"response_code":None, "result":None}
	try:
		pnr_input = driver.find_element_by_xpath('//*[@id="fullname"]')
		pnr_input.send_keys(pnr)

		searchButton= driver.find_element_by_xpath('//*[@id="idbtn"]')
		searchButton.click()


		try:
		    element = WebDriverWait(driver, 10).until(
		        EC.presence_of_element_located((By.ID, "pd")))
		    element = driver.find_element_by_xpath('//*[@id="pd"]')
		    html = element.get_attribute('outerHTML')
		    result["response_code"] = 200
		    result["result"] = html
		    return(result)
		except:
			result["response_code"] = 503
			return(result)
			   
	except:
		result["response_code"] = 503
		return(result)

	finally:
		driver.quit()


