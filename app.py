import requests
from flask import Flask, make_response, request, jsonify
import logging

import json
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_songs(search):
    session = requests.session() 
    url = "https://www.jiosaavn.com/api.php"
    headers={
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }
    payload={
        "p": 1,
        "q": search,
        "_format": "json",
        "_marker": 0,
        "api_version": 4,
        "ctx": "wap6dot0",
        "n": 20,
        "__call": "search.getResults"
    }
    response = session.get(url=url, headers=headers, params=payload)
    session.close()
    results = dict(response.json()).get('results')
    data = []
    for item in results:
        item = dict(item)
        info=dict(item.get('more_info'))
        i = {
            "encrypted_media_url": info.get('encrypted_media_url'),
            "key": item.get("id"),
            "title": item.get("title"),
            "subtitle": item.get("subtitle"),
            "perma_url": item.get("perma_url"),
            "image": item.get("image"),
            "language": item.get("language"),
            "year": item.get("year"),
            "play_count": item.get("play_count"),
            "more_info": 
            {
                "album": info.get("album"),
                "label": info.get("label"),
                "album_url": info.get("album_url"),
                "duration": info.get("duration"),
                "artistMap": info.get("artistMap"),
            }
        }
        data.append(i)
    return data
    
def audio_url(encrypted_url):
    session = requests.session() 
    url="https://www.jiosaavn.com/api.php"
    payload={
        "__call": "song.generateAuthToken",
        "url": encrypted_url,
        "bitrate": 128,
        "api_version": 4,
        "_format": "json",
        "ctx": "wap6dot0",
        "_marker": 0   
    }
    headers={
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }
    response = session.get(url=url, headers=headers, params=payload)
    session.close()
    if response.status_code==200:
        audio_url1 = dict(response.json()).get('auth_url')
        status = dict(response.json()).get('status')
        if status == "success":
            audio_url1 = str(audio_url1).replace("https://ac.cf", "https://aac")
            i = audio_url1.index('?')
            audio_url1 = audio_url1[0:i]
            a = audio_url1.index('_')
            audio_url =  [
                {"96_kbps": audio_url1[0:a+1]+"96.mp4"},
                {"160_kbps": audio_url1[0:a+1]+"160.mp4"},
                {"320_kbps": audio_url1[0:a+1]+"320.mp4"}
            ]
            return audio_url
        return None
    return None 
# print(search_songs("Let me down Slowly")[0]['encrypted_media_url'])
# print(audio_url("ID2ieOjCrwfgWvL5sXl4B1ImC5QfbsDykJc9GKuqYAscqeQDCNDW0sQN9L1Aj0zgrfixrw7BYNiSHpFk/2oZPhw7tS9a8Gtq"))


@app.route('/')
def home():
    print('**************************************************************')
    print("Home Page reached ALERT: ", request.remote_addr)
    print('*************************************************************')
    return make_response(jsonify({"results":['So you successfully managed to reached here']}))
@app.route('/getdata')
def getdata():
    song = str(request.args.get('q'))
    a = song
    print(song)
    print(request.remote_addr)
    if song != "None" and len(a.replace(' ', ''))!=0:
        try:
            results = search_songs(song)
            res = {"results":results}
            response = make_response(jsonify(res))
            response.headers["Content-Type"] = "application/json"
            return response, 200
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return jsonify({'error': 'An error occurred while processing the request.'}), 500

    return jsonify({"results":[]}), 200
# print(audio_url("ID2ieOjCrwfgWvL5sXl4B1ImC5QfbsDyBlrJGTfFbyAhRCAkx//LGIlozHj/EqcPOiQvaQf6g3CFte9EDf+yEhw7tS9a8Gtq"))
@app.route('/getsong', methods=['POST', 'GET'])
def getsong():
    if request.method != 'POST':
        return jsonify({"results":['Expecting a post request']}), 200
    url=dict(request.get_json()).get('url')
    print(url)
    a = url
    if url!=None and len(a.replace(' ', ''))!=0:
        try:
            results = audio_url(url)
            res = {"results":list(results)}
            response = make_response(jsonify(res))
            response.headers["Content-Type"] = "application/json"
            return response, 200
        except Exception as e:
            logger.error(f"Error occurred: {str(e)}")
            return jsonify({'error': 'An error occurred while processing the request.'}), 200

    return jsonify({"results":[]}), 200

if  __name__ == "__main__":
    with app.app_context():
        app.run()