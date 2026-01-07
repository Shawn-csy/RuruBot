import time
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.features.astro import get_astro_info
from services.constants import astro

print(f"Starting speed test for 12 constellations...")
print("-" * 50)

total_start = time.time()
success_count = 0

for name in astro.keys():
    print(f"Fetching {name}...", end="", flush=True)
    start = time.time()
    try:
        data = get_astro_info(name, "daily")
        duration = time.time() - start
        
        if data and "無法獲取" not in data[0] and "連線超時" not in data[0]:
            print(f" Done ({duration:.2f}s)")
            print(f"   Preview: {data[0][:30]}...") # Print first 30 chars
            success_count += 1
        else:
            print(f" Failed ({duration:.2f}s) - {data[0] if data else 'Unknown error'}")
            
    except Exception as e:
        print(f" Error: {e} ({time.time() - start:.2f}s)")

total_duration = time.time() - total_start
print("-" * 50)
print(f"Test completed in {total_duration:.2f}s")
print(f"Success rate: {success_count}/{len(astro)}")
print(f"Average time per request: {total_duration/len(astro):.2f}s")
