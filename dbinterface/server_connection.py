
import requests

def postServer(issue):
    user_json= { "user_id":issue.getInfo("user_id"), "channel":issue.getInfo("channel"), "phone_number":issue.getInfo("phone_number"),"username": issue.getInfo("username"),"first_name":issue.getInfo("firstname"),"last_name":issue.getInfo("lastname")}
    issue_json= { "datetime":issue.getInfo("datetime"), "channel":issue.getInfo("channel"), "msg_id":issue.getInfo("msg_id"),"latitude": issue.getLatitude,"longitude":issue.getLongitude,"text":issue.getInfo("text"),"category": issue.getCategory,"status":issue.getStatus,"classification_dict":issue.getClassificationDict}
    
    r = requests.post('http://', data = {'user':user_json,'issue':issue_json})
    

    
