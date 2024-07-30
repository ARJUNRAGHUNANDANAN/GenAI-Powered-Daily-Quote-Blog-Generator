import requests
import json
url = 'https://{cloudrun-deployment-url}.a.run.app/generate' # replace with your cloud run endpoint.
#url = 'http://localhost:8080/generate' #to test inside development environment # make sure you have gunicorn python3 version installed and accesible to local envrionment
headers = {'Content-Type': 'application/json'}
data = {
    "quote_source": "ZenQuotesIO",
    "poem_source": "Gemini",
    "image_source": "StabilityAIImage"
}

def basic_auth(username, password):
    """Simple authentication function."""
    return (username, password)
#auth = basic_auth("easyusername", "password123") #wrong username and password will return a forbidden code. 
auth = basic_auth("your-auth-password-set-inside-cloudrun-env", "password-in-cloud-run-environment") #set correct username and password here to send in POST Request for auth
# you can modify them in Cloud Run Deployment Settings after reployment. they will be named ADMIN_USERNAME and ADMIN_PASSWORD

response = requests.post(url, headers=headers, json=data, auth=auth)

print(response.json()) 
