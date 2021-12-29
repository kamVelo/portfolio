import requests as rq
from time import sleep
r = rq.get("https://coloors.co/generate")
sleep(20)
print(r.is_redirect)