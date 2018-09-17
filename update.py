import requests
import json
from pprint import pprint

def login(email, password):
  jsonData = {
    'email': email,
    'password': password
  }
  response = requests.post(
    'https://api.hyperbudget.net/account/login',
    json=jsonData
  )

  if response.status_code == requests.codes['ok'] and response.json()['token']:
    return response.json()['token']
  else:
    raise Exception("Error " + str(response.status_code) + ' ' + json.dumps(response.json()['error']))

def getTransactions(jwt, txnPassword):
  jsonData = {
    'password': txnPassword
  }
  response = requests.post(
    'https://api.hyperbudget.net/account/transactions/list',
    headers={
      'x-jwt': jwt
    },
    json=jsonData
  )

  if response.status_code == requests.codes['ok'] and response.json()['transactions']:
    return response.json()['transactions']
  else:
    raise Exception("Error " + str(response.status_code) + ' ' + json.dumps(response.json()['error']))

print("Enter email")
email = input()
print("Enter password")
password = input()
print("Enter transaction password")
txnPassword = input()

jwt = login(email, password)
txns = getTransactions(jwt, txnPassword)

#{ "index" : { "_index": "movies", "_type" : "movie", "_id" : "2" } }
# {"director": "Frankenheimer, John", "genre": ["Drama", "Mystery", "Thriller"], "year": 1962, "actor": ["Lansbury, Angela", "Sinatra, Frank", "Leigh, Janet", "Harvey, Laurence", "Silva, Henry", "Frees, Paul", "Gregory, James", "Bissell, Whit", "McGiver, John", "Parrish, Leslie", "Edwards, James", "Flowers, Bess", "Dhiegh, Khigh", "Payne, Julie", "Kleeb, Helen", "Gray, Joe", "Nalder, Reggie", "Stevens, Bert", "Masters, Michael", "Lowell, Tom"], "title": "The Manchurian Candidate"}

output = ""
id = 1

txns.sort(key = lambda txn: txn['date'])

for txn in txns:
  output += json.dumps({
    "update": { "_index": "transactions", "_type": "transaction", "_id": id, "retry_on_conflict": 3 }
  }) + "\n"
  output += json.dumps( { "doc": { "category_names": list(map(lambda cat: cat['name'], txn['categories'])) } } ) + "\n"
  id += 1

output += "\n"

print (output)

#print (json.dumps(txns, sort_keys=True, indent=4, separators=(',', ': ')))
