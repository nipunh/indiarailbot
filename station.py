import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import config




def train_btw_stn():
	src_stn = "BPL"
	dst_stn= "8"
	# train_num = info["train_num"]
	# options = webdriver.ChromeOptions()
	# options.add_argument('headless')
	# options.add_argument('window-size=1200x600')
	driver = webdriver.Chrome('C:/Users/Nipun Hedaoo/AppData/Local/Google/Chrome/chromedriver')#,chrome_options=options)  # Optional argument, if not specified will search path.
	driver.get('https://enquiry.indianrail.gov.in/ntes/index.html');
	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, "ui-id-2")))

	searchButton= driver.find_element_by_xpath('//*[@id="ui-id-2"]')
	searchButton.click()

	element = WebDriverWait(driver, 10).until(
		EC.presence_of_element_located((By.ID, "station1")))

	stn= driver.find_element_by_xpath('//*[@id="viaStation"]')
	stn.send_keys(src_stn)

	stn2= driver.find_element_by_xpath('//*[@id="viaStnWithinHrs"]')
	stn2.send_keys(dst_stn)

	searchButton= driver.find_element_by_xpath('//*[@id="viaStnGoBtn"]')
	searchButton.click()
	try:
	    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.xpath, '//*[@id="ui-id-106"]/table/tbody/tr[1]/td/span[1]')))
	    element1 = driver.find_element_by_xpath('//*[@id="ui-id-106"]/table/tbody/tr[2]')
	    html = element1.get_attribute('outerHTML')
	    print(html)
	except:
		print("External Server Error")
	finally:
		driver.quit()	

train_btw_stn()