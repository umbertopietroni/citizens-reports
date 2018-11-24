import sys
sys.path.insert(0, '../dbinterface/')
from classes import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os

import time
import math

import main
import importlib
import traceback

class Message():
	def __init__(self, user, message):
		self.user = user
		self.message = message
	def __eq__(self, other):
		return self.message == other.message


if os.name == "nt":
	driverPath = "driver/chromedriver_2.24.exe"
	dataPath = "Data"
else:
	driverPath = "driver/chromedriver"
	dataPath = "Data/ChatBot"


options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + dataPath)
driver = webdriver.Chrome(chrome_options=options, executable_path=driverPath)
driver.get('https://web.whatsapp.com')
driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

#input("Choose a chat on whatsapp and press enter : ")
chatHistory = []
replyQueue = []
firstRun = True

print("Starting...")

while True:
	try:

		importlib.reload(main)

		main.main(driver, chatHistory, replyQueue, firstRun)

	except:
		print(traceback.format_exc())
		
	time.sleep(5)
