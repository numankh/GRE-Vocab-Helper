import requests
import json
from decouple import config

FILE_PATH = config('FILE_PATH')
greWordsFile = open(FILE_PATH+"/utils/greWords.txt", "r")
words = ""

for line in greWordsFile:
    words = words + line.strip() + ","

myobj = {"words": words}
greWordsFile.close()

url = 'http://192.168.5.73:4000/bulkWords'
x = requests.post(url, data = myobj)
print(x)