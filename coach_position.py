import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config




def coach_position(info):
	pnr = info["pnr_number"]
	driver = webdriver.Chrome('C:/Users/Nipun Hedaoo/AppData/Local/Google/Chrome/chromedriver')  # Optional argument, if not specified will search path.
	driver.get('https://www.trainspnrstatus.com/');

	pnr_input = driver.find_element_by_xpath('//*[@id="fullname"]')
	pnr_input.send_keys(pnr)

	searchButton= driver.find_element_by_xpath('//*[@id="idbtn"]')
	searchButton.click()




	try:
	    element = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.ID, "pd")))
	    element = driver.find_element_by_xpath('//*[@id="pd"]')
	    html = element.get_attribute('outerHTML')
	    return(html)
	except:
		return("External Server Error")    

	finally:
	    driver.quit()




