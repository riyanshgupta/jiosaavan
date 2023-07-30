import requests

url = "http://127.0.0.1:5000/getdata"

payload = {'url': "ID2ieOjCrwfgWvL5sXl4B1ImC5QfbsDyBlrJGTfFbyAhRCAkx//LGIlozHj/EqcPOiQvaQf6g3CFte9EDf+yEhw7tS9a8Gtq"}
headers = {
  'Content-Type': 'application/json'
}
params={
    'q' : 'Takeaway'
}

response = requests.request("GET", url, headers=headers, params=params)

print(response.text)