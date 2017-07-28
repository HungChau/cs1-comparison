import requests


print ("Input a code program, and then parse the concepts")

data = {'code': "a =10\nprint(a)",'mode': "concepts"}
req = requests.post(url = 'http://acos.cs.hut.fi/python-parser', data=data)
print(req.text)