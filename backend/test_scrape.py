import requests
from bs4 import BeautifulSoup

url = "https://blinkit.com/prn/amul-taaza-toned-fresh-milk/prid/13247"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
response = requests.get(url, headers=headers)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    if script:
        print("Found NEXT_DATA!")
    else:
        print("No NEXT_DATA found.")
        print(response.text[:500])
else:
    print("Blocked.")
