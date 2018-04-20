
import requests
import json


def postServer(issue):
    user_dict= { "user_id":issue.getInfo("user_id"), "channel":issue.getInfo("channel"), "phone_number":issue.getInfo("phone_number"),"username": issue.getInfo("username"),"first_name":issue.getInfo("firstname"),"last_name":issue.getInfo("lastname")}
    issue_dict= { "datetime":issue.getInfo("datetime"), "channel":issue.getInfo("channel"), "msg_id":issue.getInfo("msg_id"),"latitude": issue.getLatitude(),"longitude":issue.getLongitude(),"text":issue.getInfo("text"),"category": issue.getCategory(),"status":issue.getStatus(),"classification_dict":json.dumps(issue.getClassificationDict())}
    user_json = json.dumps(user_dict)
    issue_json = json.dumps(issue_dict)
    
    files = []
    image = []
    for i in issue.getImages():
        image_dict = {'filename':i.getFilename(),'category':i.getCategory(), 'classification_dict':json.dumps(i.getClassificationDict())}
        im = (i.getFilename(), i.getContent())
        files.append(im)
        image.append(image_dict)
    
    image_json = json.dumps(image)
    #r = requests.post('http://montecchioreports.altervista.org/action/saveIssue', data = {'user':user_json,'issue':issue_json})
    r = requests.post('http://httpbin.org/post', data = {'user':user_json,'issue':issue_json, 'images':image_json}, files = files)
    print(r.text)
    

    
