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
        print("request sent", r.json())
        if r["status_code"] == 200:
            if r.json()['content'] == "null" or r.json()['content'] == None:
                return "I dont know"
            return r.json()['content']
        else:
            return "something wrong in the API server"
    except:
        return "something wrong in the API server2"