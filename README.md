# citizens-reports

The aim of this project was to create a system capable of:
 * receiving and storing messages from italian citizen containing report about city problem using chatbots (one for WhatsApp and one for Telegram).
 * classify automatically each reports into a particular category (e.g environment, road maintenance, street lightinig, emergency) using Naive Bayes Classifier and Natural Language Processing

## Project Structure

 * **classifiers** directory contain all the files related to the creation of the Naive Bayes Classifier for the natural text in the citizens' reports. The dataset was created after searching and download real citizens' report for public italian cities' websites.
 * **whatsapp** contains the Python script which executes the WhatsApp chatbot. This was built using Selenium framework.
 * **telegram** contains 'demobot.py' which executes the Telegram chatbot.
 * **dbinterface** is the part of the system needed for the connection to the server where all messages are stored after being classified.
 *  **wsinterface** is the interface with Clarifai framework which is responsible for the analysis of the images in the citizens' reports.

## Dependencies


```
sudo apt-get install python3-mysqldb 

pip3 install telepot

pip3 install sklearn

pip3 install numpy

pip3 install scipy

pip3 install pandas

pip3 install clarifai

pip3 install selenium
```



