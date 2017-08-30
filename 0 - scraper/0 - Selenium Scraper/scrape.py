from selenium import webdriver, common
from selenium.webdriver.support.ui import WebDriverWait
import time, os
from DB import DB
from URL import URL

source = ''
def compare_source(browser):
    try:
        return source != browser.page_source
    except WebDriverException:
        pass

os.system('PATH=$PATH:.')

db = DB('play.db')
db.create_tables()
db.add_seeds('seed.txt')
browser = webdriver.Firefox()

test = 0

count = 0

test = 3
while test:

	count = count + 1
	url = db.get_unpr()
	# url = 'https://play.google.com/store/apps/details?id=com.instagram.android&hl=en'

	browser.get(url)

	url = URL(url)
	app_id = url.get_qs('id')
	print app_id

	id_app_title = browser.find_elements_by_class_name("id-app-title")[0].text.strip()
	name = browser.find_element_by_xpath('//span[@itemprop="name"]').text.strip()
	genre = browser.find_element_by_xpath('//span[@itemprop="genre"]').text.strip()
	installs = browser.find_element_by_xpath('//div[@itemprop="numDownloads"]').text.strip()
	description = browser.find_element_by_xpath('//div[@jsname="C4s9Ed"]').text
	current_version = browser.find_element_by_xpath('//div[@itemprop="softwareVersion"]').text.strip()
	website = browser.find_elements_by_class_name('dev-link')[0].get_attribute('href')
	
	try:
		address = browser.find_element_by_xpath('//div[@class="physical-address"]').text
	except common.exceptions.NoSuchElementException:
		address = None

	try:
		bt = None
		bt = browser.find_elements_by_class_name("badge-title")[0].text
		if (bt == 'Editors\' Choice'):
			editors_choice = 1
		else:
			editors_choice = 0
		# editors_choice = 1
	except Exception as e:
		editors_choice = 0

	permission_button = browser.find_elements_by_class_name('id-view-permissions-details')[0]
	permission_button.click()
	source = browser.page_source
	WebDriverWait(browser, 5).until(compare_source)

	permission_buckets = browser.find_elements_by_class_name('permission-bucket')
	permissions = ''
	for bucket in permission_buckets:
		permissions += bucket.text

	# print description
	# print id_app_title
	# print name
	# print genre
	# print installs
	# print current_version
	# print address
	# print website
	# print bt, editors_choice

	if not db.exists('metadata', app_id):
		db.insert('metadata', {
	                    'id': app_id,
	                    'name': id_app_title,
	                    'org': name,
	                    'genre': genre,
	                    'installs': installs,
						'description': description,
						'version': current_version,
						'address': address,
						'website': website,
						'editors': editors_choice,
						'permissions': permissions
	                })
				# print permissions
				# soup.find('div', attrs = {'itemprop' : "numDownloads"})

	bar_numbers = browser.find_elements_by_class_name('bar-number')
	# bar_numbers = bar_numbers[::-1]
	rating = {"id": app_id, 0: 0}
	i = 5
	for bar in bar_numbers:
		rating[i] = int(bar.text.replace(',', ''))
		i = i - 1
	print rating
	db.insert('rating', rating)

	test = test - 1