import requests

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
            audio_url =  {
                "96_kbps": audio_url1[0:a+1]+"96.mp4",
                "160_kbps": audio_url1[0:a+1]+"160.mp4",
                "320_kbps": audio_url1[0:a+1]+"320.mp4"
            }
            return audio_url
        return None
    return None 

import json
l = search_songs("Let me down slowly feat Alissa")
for i in l:
    print(json.dumps(l, indent=1))
print(audio_url(l[0].get('encrypted_media_url')))