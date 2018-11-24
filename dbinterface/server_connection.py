"""
Perform server requests
"""

import requests
import json
from urllib import parse


hostname = 'http://montecchioreports.altervista.org'
bot_key = open('botkey.txt', 'r').read().replace("\n", "").replace("\r", "")


def postServer(issue):
    """
    Save issue with a POST request
    """
    user_dict = {"user_id": issue.getInfo("user_id"), "channel": issue.getInfo("channel"),
                 "phone_number": issue.getInfo("phone_number"), "username": issue.getInfo("username"),
                 "first_name": issue.getInfo("firstname"), "last_name": issue.getInfo("lastname")}
    issue_dict = {"datetime": issue.getInfo("datetime"), "channel": issue.getInfo("channel"),
                  "msg_id": issue.getInfo("msg_id"), "latitude": issue.getLatitude(), "longitude": issue.getLongitude(),
                  "text": issue.getInfo("text"), "category": issue.getCategory(), "status": issue.getStatus(),
                  "classification_dict": json.dumps(issue.getClassificationDict())}
    user_json = json.dumps(user_dict)
    issue_json = json.dumps(issue_dict)

    files = []
    image = []
    for i in issue.getImages():
        image_dict = {'filename': i.getFilename(), 'category': i.getCategory(),
                      'classification_dict': json.dumps(i.getClassificationDict())}
        im = ('images[]', (i.getFilename(), i.getContent()))
        files.append(im)
        image.append(image_dict)

    image_json = json.dumps(image)
    r = requests.post(
        hostname + '/api/report/insert/?key=' + bot_key,
        data={'user': user_json, 'issue': issue_json, 'images': image_json},
        files=files
    )
    print('Server response: ' + r.text)


def phoneExists(phone: str) -> bool:
    """
    Check if a phone number is already saved in database
    :param phone:
    :return: True if phone number exists
    """
    request = requests.get(
        hostname + '/api/privacy/phone_exists/' + parse.quote_plus(phone) + '/?key=' + bot_key
    )
    response = request.json()['data']['response']
    if type(response) is not bool:
        print('Server response: ' + response)
        return False
    return response


def phoneDelete(phone: str) -> bool:
    """
    Delete a phone number from database
    :param phone:
    :return: True if at least one phone number was deleted
    """
    request = requests.get(
        hostname + '/api/privacy/delete/' + parse.quote_plus(phone) + '/?key=' + bot_key
    )
    response = request.json()['data']['response']
    if type(response) is not bool:
        print('Server response: ' + response)
        return False
    return response

