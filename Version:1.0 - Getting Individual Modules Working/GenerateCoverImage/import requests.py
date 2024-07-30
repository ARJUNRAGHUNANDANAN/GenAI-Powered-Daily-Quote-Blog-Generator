import requests
Stability_Key  = os.getenv("Stability_Key")
def StableDiffusionImageGenerator(quote: str, media_dir: str) -> str:
    Stability_Key = 'Stability_Key'
    response = requests.post(
        f"https://api.stability.ai/v2beta/stable-image/generate/core",
        headers={
            "authorization": f"Bearer {Stability_Key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": f"A Scenic Picture matching this Quote by some famous person. Do not include Text in image. Make it scenic.  : {quote}",
            "output_format": "png",
        },
    )

    if response.status_code == 200:
        with open("./quote.png", 'wb') as file:
            file.write(response.content)
    else:
        raise Exception(str(response.json()))
    
if __name__ == "__main__":
    quote = "The mind is everything. What you think you become. - Buddha"
    StableDiffusionImageGenerator(quote, '/Dev')
