import requests
import urllib.parse

REMOTE_SERVER_IP = 'http://192.168.4.28:5000'

def write_to_db(st: str):
    url = REMOTE_SERVER_IP + '/write'
    
    try:
        requests.post(url, json={'content': st})
        return True
    except:
        return False

def recall_stuff(st: str):
    url = REMOTE_SERVER_IP + '/query'
    encoded_query = urllib.parse.quote(st)
    try:
        r = requests.get(f"{url}?query={encoded_query}")
        if r.json()['response'] == "null" or r.json()['response'] == None:
                return "I dont know"
        return r.json()['response']
    except:
        return "something wrong in the API server2"