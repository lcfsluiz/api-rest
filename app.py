#!/usr/bin/python3

import requests

requisicao = requests.get("https://viacep.com.br/ws/08270630/json/")

print(requisicao.json()