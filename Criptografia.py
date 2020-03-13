import json
import requests
import hashlib


url = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=6bc24b20f0b1d36ab1667e24e10e23b1f4a5e21d'
try:
    req = requests.get(url)
except Exception as e:
    print("Error", e)

with open("answer.json", "w") as write_file:
    json.dump(req.json(), write_file)

with open("answer.json", 'r') as f:
    datastore = json.load(f)
    encoding = f.encoding

numero_casas = datastore['numero_casas']
cifrado = datastore['cifrado']


def decifrado(cifrado, numero_casas):

    cifrado.lower()
    letras = "abcdefghijklmnopqrstuvwxyz"
    result = ""
    for i in cifrado:
        if (letras.find(i) == -1):
            result = result + i
            continue
        pos = letras.find(i) - numero_casas
        if (pos < 0):
            pos += 26
        result = result + letras[pos]

    return result


datastore['decifrado'] = decifrado(cifrado, numero_casas)

datastore['resumo_criptografico'] = hashlib.sha1(
    datastore['decifrado'].encode(encoding)).hexdigest()


with open("answer.json", "w") as write_file:
    json.dump(datastore, write_file)


url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=6bc24b20f0b1d36ab1667e24e10e23b1f4a5e21d'
files = {'answer': open('answer.json', 'rb')}

headers = {"Content_Type": "multipart/form-data"}

params = {"file": "answer"}

r = requests.post(url, headers=headers, files=files)
print(r.text)
