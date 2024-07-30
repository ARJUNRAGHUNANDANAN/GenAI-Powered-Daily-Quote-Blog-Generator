import requests

def generate_cover_image(quote: str, api_key: str) -> None:
    url = "https://api.limewire.com/api/image/generation"
    headers = {
        "Content-Type": "application/json",
        "X-Api-Version": "v1",
        "Accept": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "prompt": quote,
        "aspect_ratio": "16:9"  # Change to 16:9 as per your requirement
    }
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        image_url = data.get('data', [{}])[0].get('url', 'No URL found')
        print(f"Image generated successfully. You can view it at: {image_url}")
    else:
        print(f"Failed to generate image. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Example usage
quote = "The only limit to our realization of tomorrow is our doubts of today."
api_key = "API+KEY"
generate_cover_image(quote, api_key)
