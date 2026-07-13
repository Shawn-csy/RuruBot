import requests
import time

url = "https://astro.click108.com.tw/daily_0.php?iAstro=0&iAcDay=2026-01-06"
print(f"Testing connection to: {url}")

start = time.time()
try:
    res = requests.get(url, timeout=10)
    print(f"Status Code: {res.status_code}")
    print(f"Time taken: {time.time() - start:.2f}s")
    print("Preview:", res.text[:100])
except Exception as e:
    print(f"Error: {e}")
    print(f"Time taken: {time.time() - start:.2f}s")
