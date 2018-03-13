import urllib.request
import os
import shutil
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def getorderedfiles(dirpath):
	a = [s for s in os.listdir(dirpath)
		 if os.path.isfile(os.path.join(dirpath, s))]
	a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
	return a

DOWNLOAD_PATH = "/home/giulio/Scaricati/"

def main(driver, chatHistory, replyQueue, firstRun):		
	
	driver.switch_to_window(driver.window_handles[0])
	usersDiv = driver.find_element_by_id("side")
	messageDiv = driver.find_element_by_id("main")
	actionChains = ActionChains(driver)

	contacts = usersDiv.find_elements_by_class_name("_2wP_Y")
	
	new_messages = []
	received_msgs = []
	
	for contact in contacts:
		chatTitle = contact.find_elements_by_class_name("_1wjpf")
		#print("chatTitle = ", chatTitle[0].text)
		unread = contact.find_elements_by_class_name("unread")
		#print("unread = ", unread)
		
		if unread:
			# click on contact element and read all presents messages
			print("New message(s) for ", chatTitle[0].text)
			contact.click()
			messageList = messageDiv.find_elements_by_class_name("msg")
			print("messageList = ", len(messageList))
			print("="*100)
			
			messageList.reverse()
			
			new_messages.append(messageList)

		if chatTitle[0].text == "Giulio":
			# click on contact element and read all incoming messages
			contact.click()
			messageList = messageDiv.find_elements_by_class_name("message-in")
			print("messageList = ", len(messageList))
			print("="*100)
			for m in messageList:
				copyableText = m.find_elements_by_class_name("copyable-text")
				#print("copyableText = ", copyableText)
				for ct in copyableText[0:1]:
					print("ct = ", ct.text)
				
				timestamp = m.find_elements_by_class_name("_2f-RV")
				for ts in timestamp[0:1]:
					print("ts = ", ts.text)
				
				received_msgs.append({
					"ts": ts.text,
					"text": ct.text,
					"user": chatTitle[0].text,
				})
				
				# look for images..
				images = m.find_elements_by_tag_name("img")
				print("Images = ", images)
				for im in images:
					src = im.get_attribute("src").replace("blob:", "")
					#print("im = ", src)
					try:
						os.makedirs(chatTitle[0].text)
					except:
						pass
#					time.sleep(30)
					# right click and save
					#actionChains.context_click(im).perform()
					#print("Keys.ARROW_DOWN = ", Keys.ARROW_DOWN)
					#actionChains.send_keys(Keys.ARROW_DOWN).perform()
					#actionChains.send_keys("l").perform()
					im.click()
					
					# look for save image button
#					driver.switch_to_window(driver.window_handles[0])
					mpt = driver.find_elements_by_class_name("media-panel-tools")[0]
					buttons = mpt.find_elements_by_class_name("rAUz7")
#					print(buttons)
					# download
					buttons[3].click()
					# close window
					buttons[4].click()

					# look for last downloaded file
					downloaded_files = getorderedfiles(DOWNLOAD_PATH)
					downloaded_files.reverse()
					firstfile = downloaded_files[0]
					
					#print("downloaded_files = ", downloaded_files)
					
					#print(DOWNLOAD_PATH+firstfile)
					#local_filename, headers = urllib.request.urlretrieve(src)
					#print("local_filename = ", local_filename)
					
					if firstfile.startswith("WhatsApp"):
						print("Moving file : " + DOWNLOAD_PATH+firstfile)
						downloaded_fname =  firstfile.replace("WhatsApp Image ", "")
						downloaded_fname =  downloaded_fname.replace(" ", "_")
						downloaded_fname =  downloaded_fname.replace(" ", "_")
						downloaded_fname =  downloaded_fname.replace("_at_", "__")
						shutil.move(DOWNLOAD_PATH+firstfile, chatTitle[0].text + "/%s" % downloaded_fname)
#					
					time.sleep(2)

#					urllib.urlretrieve(src, chatTitle[0].text + "/filename.png")
#					f = urllib.request.urlopen(src)
#					content = f.read()
#					f.close()
#					open(chatTitle[0].text + "/filename.png", "wb").write(content)
			
	print("Received Messages: ")
	for m in received_msgs:
		print(m)

