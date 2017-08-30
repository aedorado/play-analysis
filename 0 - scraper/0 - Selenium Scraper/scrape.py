from selenium import webdriver, common
import time, os
from DB import DB
from URL import URL

os.system('PATH=$PATH:.')

db = DB('play.db')
# db.create_tables()
# db.add_seeds('seed.txt')
browser = webdriver.Firefox()

test = 0

count = 0

test = 3
while test:

	count = count + 1
	url = db.get_unpr()

	browser.get(url)

	url = URL(url)
	app_id = url.get_qs('id')
	print app_id

	id_app_title = browser.find_elements_by_class_name("id-app-title")[0].text.strip()
	name = browser.find_element_by_xpath('//span[@itemprop="name"]').text.strip()
	genre = browser.find_element_by_xpath('//span[@itemprop="genre"]').text.strip()
	meta_info = browser.find_element_by_xpath('//div[@itemprop="numDownloads"]').text.strip()
	description = browser.find_element_by_xpath('//div[@jsname="C4s9Ed"]').text
	current_version = browser.find_element_by_xpath('//div[@itemprop="softwareVersion"]').text.strip()
	try:
		address = browser.find_element_by_xpath('//div[@class="physical-address"]').text
	except common.exceptions.NoSuchElementException:
		address = None
	website = browser.find_elements_by_class_name('dev-link')[0].get_attribute('href')

	# print description
	print id_app_title
	print name
	print genre
	print meta_info
	print current_version
	print address
	print website
				# soup.find('div', attrs = {'itemprop' : "numDownloads"})

	test = test - 1
	pass