import urllib.request
import os
import shutil
import pprint
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time
import traceback

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
from datetime import datetime, timedelta
import pickle

import sys

sys.path.insert(0, '../dbinterface/')
from classes import *
from server_connection import phoneExists, phoneDelete


def getorderedfiles(dirpath):
    a = [s for s in os.listdir(dirpath)
         if os.path.isfile(os.path.join(dirpath, s))]
    a.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return a


DOWNLOAD_PATH = "/home/umberto/Scaricati/"


def delete_chat(driver, chat_id):
    usersDiv = driver.find_element_by_id("side")
    messageDiv = driver.find_element_by_id("main")
    actionChains = ActionChains(driver)
    contacts = usersDiv.find_elements_by_class_name("_2wP_Y")
    print("inizio delete")

    for contact in contacts:
        chatTitle = contact.find_elements_by_class_name("_1wjpf")
        if chatTitle[0].text == chat_id:
            try:
                contact.click()

                wait = WebDriverWait(driver, 10)
                apri_menu = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'ZR5SB')))
                apri_menu.click()
                """apertura menu a tendina"""
                time.sleep(1)
                buttons_menu = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_3s1D4')))
                #buttons_menu = driver.find_element_by_class_name("_3s1D4")

                wait2 = WebDriverWait(buttons_menu,10)
                wait2.until(EC.presence_of_element_located((By.CLASS_NAME, '_3lSL5')))
                buttons_menu.find_elements_by_class_name("_3lSL5")[2].click()
                """clicco sul bottone per eliminare chat"""
                time.sleep(1)
                pop_up = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_1CnF3')))
                # pop_up = driver.find_element_by_class_name("_1CnF3")
                if pop_up:
                    wait3 = WebDriverWait(pop_up, 10)
                    wait3.until(EC.element_to_be_clickable((By.CLASS_NAME, '_1WZqU')))
                    pop_up.find_elements_by_class_name("_1WZqU")[1].click()
                    time.sleep(1)
                break
            except Exception:
                print("Errore nella delete")
                print(traceback.format_exc())
                driver.get('https://web.whatsapp.com')



def get_date_from_msg(text):
    date_rex = re.compile('\[(.+?)\]')
    pre_date = date_rex.findall(text)[0]
    h, mi, d, mo, y = [int(s) for s in re.findall(r'\d+', pre_date)]
    date = datetime(y, mo, d, h, mi)
    print(date)
    return date


"""
   @save_msg
   salvo tutti i messaggi contenuti in messageList. dopo di questo metodo è necessario fare un delete_chat
"""


def save_msg(driver, messageList, chatTitle):
    ts = str(time.time())
    msg_dir = "inbox/" + chatTitle + '/' + ts
    try:
        os.makedirs(msg_dir)
    except:
        pass

    text = ""
    m = {}
    photo = []
    date = ""
    location = []

    for m in messageList:
        images = m.find_elements_by_tag_name("img")
        audio = m.find_elements_by_tag_name("audio")
        copyableText = m.find_elements_by_class_name("copyable-text")
        if audio:
            print ("Audio")
        elif (images or copyableText):
            if images:
                im = images[0]
                pos_class = im.get_attribute("class")
                # is_pop = im.find_elements_by_class_name("_1Qnxi")
                if pos_class == "_1Qnxi":
                    print("posizione trovata")
                    # pos = father.get_attribute("href")
                    pos = im.get_attribute("src")
                    if ("maps" in pos):

                        # https://maps.google.com/maps?q=44.7649225%2C10.3085252&z=17&hl=it
                        # print(pos)
                        # lat_rex = re.compile(r'q=(.+?)%2C')
                        # long_rex = re.compile(r'%2C(.+?)&z=')
                        lat_rex = re.compile(r'%7C(.+?)%2C%20')
                        long_rex = re.compile(r'%2C%20(.+?)&signature')
                        if lat_rex.findall(pos) and long_rex.findall(pos):
                            lat = float(lat_rex.findall(pos)[0])
                            lon = float(long_rex.findall(pos)[0])
                            location = [lat, lon]
                            print(location)

                elif pos_class == "_2H6ea":
                    print("link esterno")

                else:
                    src = im.get_attribute("src").replace("blob:", "")

                    # testo aggiunto come didascalia alla foto
                    didasc = m.find_elements_by_class_name("_1RiwZ")
                    if didasc:
                        did_text = didasc[0].find_elements_by_class_name("copyable-text")
                        if did_text:
                            text += did_text[0].text + ' '

                    im.click()
                    # mpt = driver.find_elements_by_class_name("media-panel-tools")[0]
                    mpt = driver.find_elements_by_class_name("_3Kxus")[0]
                    buttons = mpt.find_elements_by_class_name("rAUz7")
                    # download
                    buttons[3].click()
                    # close window
                    buttons[4].click()

                    # look for last downloaded file
                    time.sleep(1)
                    downloaded_files = getorderedfiles(DOWNLOAD_PATH)
                    downloaded_files.reverse()
                    firstfile = downloaded_files.pop(0)

                    if firstfile.startswith("WhatsApp"):
                        print("Moving file : " + DOWNLOAD_PATH + firstfile)
                        downloaded_fname = firstfile.replace("WhatsApp Image ", str(datetime.now()))
                        # downloaded_fname = downloaded_fname.replace(" ", "_")
                        # downloaded_fname = downloaded_fname.replace(" ", "_")
                        # downloaded_fname = downloaded_fname.replace("_at_", "__")

                        # downloaded_fname = datetime.now()

                        shutil.move(DOWNLOAD_PATH + firstfile, msg_dir + "/%s" % downloaded_fname)
                        photo.append(msg_dir + "/%s" % downloaded_fname)

                    # content = open(filename, 'rb').read()

            elif copyableText:
                # for ct in copyableText[0:1]:
                #  print("ct = ", ct.text)
                try:
                    ct = copyableText[1]
                except IndexError:
                    for ct in copyableText[0:1]:
                        print("ct = ", ct.text)

                # precise timestamp data-pre-plain-text = [16:52, 18/3/2018]
                pre_text = copyableText[0].get_attribute("data-pre-plain-text")
                if pre_text:
                    date = get_date_from_msg(pre_text)
                # timestamp = m.find_elements_by_class_name("_2f-RV")
                # for ts in timestamp[0:1]:
                # print("ts = ", ts.text)

                text += ct.text + ' '
    if (not date):
        date = datetime.now()

    m = {
        "message_id": ts,
        "date": date,
        "text": text,
        "user": chatTitle,
        "photo": photo,
        "location": location,
    }

    # print(m)
    pprint.pprint(m, open(msg_dir + "/" + 'msg.dict', 'w'))
    segnalazione = msg_to_segnalazione(m, msg_dir)
    if segnalazione:
        segnalazione.printIssue()
        segnalazione.save()
        with open(msg_dir + "/" + 'issue.pickle', 'wb') as output:
            pickle.dump(segnalazione, output, pickle.HIGHEST_PROTOCOL)


def is_timeout(date):
    now = datetime.now()
    delta = timedelta(seconds=180)
    print(now - date)

    if now - date > delta:
        print("Tempo scaduto")
        return True
    else:
        print("non ancora")
        return False


def msg_to_segnalazione(msg, msg_dir):
    if msg:

        msg_id = msg["message_id"]
        user_id = msg["user"]

        text = msg.get("text", "")
        photo = msg.get("photo", [])
        date = msg.get("date", "")
        pos = msg.get("location", [])
        # text_classification_dict = msg.get("text_category", [])

        segnalazione = Issue(msg_id)
        segnalazione.setInfo("channel", "whatsapp")
        segnalazione.setInfo("text", text)
        if date:
            segnalazione.setInfo("datetime", date.strftime("%Y-%m-%d %H:%M:%S"))
            # segnalazione.setInfo("date", date.strftime("%Y-%m-%d"))
            # segnalazione.setInfo("time", date.strftime("%H:%M:%S"))
        segnalazione.setInfo("user_id", user_id)
        segnalazione.setInfo("phone_number", user_id)

        if pos:
            segnalazione.setLatitude(pos[0])
            segnalazione.setLongitude(pos[1])
        # segnalazione.setCategory(msg.get("category",""))
        # segnalazione.setClassificationDict(text_classification_dict)
        for p in photo:
            image = IssueImage(p)
            # print(image)
            segnalazione.addImage(image)

        return segnalazione

    print("ERROR: message not defined")


def main(driver, chatHistory, replyQueue, firstRun):
    # driver.switch_to_window(driver.window_handles[0])

    try:
        usersDiv = driver.find_element_by_id("side")
        actionChains = ActionChains(driver)
        contacts = usersDiv.find_elements_by_class_name("_2wP_Y")
    except NoSuchElementException:
        contacts = []
        print("Caricamento...")
    # messageDiv = driver.find_element_by_id("main")

    new_messages = []
    received_msgs = []

    # DISTINGUERE DA USER A GROUP
    # <span data-icon="default-user"
    # <span data-icon="default-group"

    for contact in contacts:
        chatTitle = contact.find_elements_by_class_name("_1wjpf")
        # print("chatTitle = ", chatTitle[0].text)
        # unread = contact.find_elements_by_class_name("unread")
        # forse al posto di unread ci vuole "OUeyt"

        data_icon = contact.find_element_by_class_name("_3ZW2E")
        try:
            user = data_icon.find_element_by_xpath('.//span[@data-icon="default-user"]')
        except NoSuchElementException:
            user = None
            print ("Gruppo")

        if user:
            print(chatTitle[0].text)
            # click on contact element and read all incoming messages
            ct = ""
            ts = ""
            messageList = []
            messageDiv =[]
            messageOut=[]
            #driver.implicitly_wait(1.5)

            print("=" * 100)
            try:
                contact.click()
                messageDiv = driver.find_element_by_id("main")
                messageOut = messageDiv.find_elements_by_class_name("message-out")
            except:
                print("No contact")
            if not messageOut:
                ##INVIO MESSAGGIO INIZIALE
                if not phoneExists(chatTitle[0].text):
                    input_box = driver.find_element_by_class_name('_2S1VP')
                    input_box.send_keys(
                        "Benvenuto! Può inviare altri messaggi, foto o posizione. La segnalazione verrà presa in carico dal sistema qualche minuto dopo l'ultimo messaggio. Per salvare la segnalazione il sistema conserverà anche il suo numero di telefono. Se non vuole che ciò accada invii un messaggio con scritto: \"Cancellami\" e la segnalazione non verrà salvata. Può anche eliminare il suo numero in qualsiasi momento inviando lo stesso messaggio \"Cancellami\".")
                    driver.find_element_by_xpath('//span[@data-icon="send"]').click()

                else:
                    input_box = driver.find_element_by_class_name('_2S1VP')
                    input_box.send_keys(
                        "Grazie! Può inviare altri messaggi, foto o posizione. La segnalazione verrà presa in carico dal sistema qualche minuto dopo l'ultimo messaggio e le sarà inviato un messaggio di conferma.")
                    driver.find_element_by_xpath('//span[@data-icon="send"]').click()
                # time.sleep(0.5)
            try:
                messageDiv = driver.find_element_by_id("main")
                messageList = messageDiv.find_elements_by_class_name("message-in")
                print("messageList = ", len(messageList))

            except:
                print("No message")

            if messageList:
                ##cerco ultimo messaggio, testo o foto e calcolo tempo passato
                last_msg = messageList[-1]
                date = ""
                copyableText = last_msg.find_elements_by_class_name("copyable-text")
                if copyableText:
                    # precise timestamp -> data-pre-plain-text = [16:52, 18/3/2018]
                    text = copyableText[0].text.lower().replace(" ", "").replace("!", "").replace("'", "").replace(".","").replace(",", "")
                    if text == "cancellami":
                        phoneDelete(chatTitle[0].text)
                        input_box = driver.find_element_by_class_name('_2S1VP')
                        input_box.send_keys("Elimino la segnalazione e il numero. Grazie e arrivederci.")
                        driver.find_element_by_xpath('//span[@data-icon="send"]').click()
                        delete_chat(driver, chatTitle[0].text)
                        break
                    pre_text = copyableText[0].get_attribute("data-pre-plain-text")
                    if pre_text:
                        date = get_date_from_msg(pre_text)
                if not date:
                    time_d = last_msg.find_element_by_class_name("_3EFt_")
                    print(time_d.text)
                    h, mi = [int(s) for s in re.findall(r'\d+', time_d.text)]
                    now = datetime.now()
                    date = now.replace(hour=h, minute=mi)

                if is_timeout(date):
                    save_msg(driver, messageList, chatTitle[0].text)

                    ##INVIO MESSAGGIO
                    input_box = driver.find_element_by_class_name('_2S1VP')
                    input_box.send_keys("Segnalazione Ricevuta, Grazie!")

                    wait = WebDriverWait(driver, 10)
                    send = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]')))
                    # driver.find_element_by_xpath('//span[@data-icon="send"]').click()
                    send.click()

                    delete_chat(driver, chatTitle[0].text)
                    break
