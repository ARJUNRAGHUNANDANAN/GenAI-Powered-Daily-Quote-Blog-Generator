import requests
import json
LimeWireAPI_KEY=""

url = "https://api.limewire.com/api/image/generation"

payload = {
  "prompt": "Generate a cover image that can go along with this quote : The buried talent is the sunken rock on which most lives strike and founder. Output image shoudl have No Text. Must be Inspirational",
  "aspect_ratio": "1:1"
}

headers = {
  "Content-Type": "application/json",
  "X-Api-Version": "v1",
  "Accept": "application/json",
  "Authorization": f"Bearer {LimeWireAPI_KEY}"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
print(data)
# Check for successful response before writing to file
if response.status == "COMPLETED":
  print("SUCCESS \n")
  print(data)
  # Define filename (replace 'output.json' with your desired name)
  filename = "output.json"

  # Open the file in write mode with UTF-8 encoding
  with open(filename, 'w', encoding='utf-8') as outfile:
    # Use json.dump to write indented JSON data to the file
    json.dump(data, outfile, indent=4)
    print(f"Response data written to {filename}")
else:
    print("SOMETHING WENT WRONG \n")
    print(f"Error: API request failed with status code {response.status_code}")
