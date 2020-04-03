import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import config




def seat_availability():
	train_num = "11077"
	src_stn = "BPL"
	dst_stn= "PUNE"
	# train_num = info["train_num"]
	driver = webdriver.Chrome('C:/Users/Nipun Hedaoo/AppData/Local/Google/Chrome/chromedriver')  # Optional argument, if not specified will search path.
	driver.get('https://www.railyatri.in/seat-availability');

	
	train_num = driver.find_element_by_id('train_seat_avl')
	train_num.send_keys(train_num)


	searchButton= driver.find_element_by_xpath('//*[@id="submit_check"]')
	searchButton.click()

	element = driver.find_element_by_xpath('/html/body/div/div/div[1]/table[1]/tbody')
	html = element.get_attribute('outerHTML')
	driver.close();
	print(html)

seat_availability();