import requests

REMOTE_SERVER_IP = 'http://192.168.4.28:5000'

def write_to_db(st: str):
    url = REMOTE_SERVER_IP + '/write'
    
    try:
        requests.post(url, json={'content': st})
        return True
    except:
        return False
