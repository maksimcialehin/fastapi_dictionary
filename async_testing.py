import time
import asyncio
import requests


URL = 'http://127.0.0.1:8000/'
start = time.time()
results = []

for i in range(20):
    results.append(requests.post(URL).content)
print(f'Time: {time.time() - start}')
print(results)
