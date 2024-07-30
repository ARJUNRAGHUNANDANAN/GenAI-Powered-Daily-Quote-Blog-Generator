# GeminiBlog-Version:2.0/ModulePoemGenerator.py

import os
import json
import requests
#from openai import OpenAI, AuthenticationError
import google.generativeai as genai
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')
load_dotenv() 

def generate_poem_from_source(quote: str, source: str) -> str:  
    # I am using this repo for generation : https://github.com/google-gemini/generative-ai-python/blob/main/docs/api/google/generativeai
    if source == 'Gemini':
        genai.GenerativeModel(
            model_name = 'gemini-1.0-pro',
            safety_settings = None,
            generation_config  = None,
            tools  = None,
            tool_config = None,
            system_instruction = None
        )
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        model = genai.GenerativeModel('models/gemini-1.0-pro')
        try:
            response = model.generate_content(f'You are a Daily Inspiration Quote, Poem generator that will generate inspirational poems based on a quote sent to you. Generate a 12 line Poem that is inspired on the following Quote "{quote}".\n You must not respond with a blank statement. Your response should be public friendly. It should not be harmful or explicit. Your response should be in a plain text format like the following\n {"4liner poem paragraph -space- 4liner poem paragraph - 4 liner poem paragraph each with newline notation as necessary"}')
            if response:
                # Check if the response is in the expected format
                if isinstance(response.text, str):
                    logging.info(f"Poem generated from Gemini: {response.text}")
                    return response.text
                else:
                    logging.error(f"Gemini API returned an unexpected response type: {type(response.text)}")
                    return "Error: Gemini API returned an unexpected response type."
            else:
                logging.error("Gemini API returned an empty response.")
                return "Error: Gemini API returned an empty response."
        except Exception as e:
            logging.error(f"Error generating poem from Gemini: {e}")
            return f"Error generating poem from Gemini: {e}"


    elif source == 'OpenAI':
        print("Code Disabled at the moment, Please use Gemini")
        # api_key = os.getenv("OPENAI_API_KEY")
        # if not api_key:
        #     print("OPENAI_API_KEY environment variable not set.")
        #     return "Error: OPENAI_API_KEY environment variable not set."  # Return error message
        # url = "https://api.openai.com/v1/completions"
        # headers = {
        #     "Content-Type": "application/json",
        #     "Authorization": f"Bearer {api_key}"
        # }
        # data = {
        #     "model": "text-davinci-003",
        #     "prompt": f"Write a poem inspired by this quote: '{quote}. Only respond with the poem, no other message needed.'",
        #     "max_tokens": 100,
        #     "temperature": 0.7,
        #     "n": 1,
        #     "stop": "\n\n"
        # }
        # response = requests.post(url, headers=headers, json=data)
        # if response.status_code == 200:
        #     return response.json()["choices"][0]["text"]
        # else:
        #     print(f"Error generating poem from OpenAI: {response.text}")
        #     return f"Error generating poem from OpenAI: {response.text}"  # Return error message
    elif source == 'Perplexity':
        print("Code Disabled at the moment, Please use Gemini")
    #     # Implement logic to generate poem using Perplexity
    #     api_key = os.getenv("PERPLEXITY_API_KEY")
    #     if not api_key:
    #         print("PERPLEXITY_API_KEY environment variable not set.")
    #         return "Error: PERPLEXITY_API_KEY environment variable not set."  # Return error message
    #     client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")
    #     messages = [
    #         {
    #             "role": "system",
    #             "content": (
    #                 "You are an artificial intelligence assistant and you need to "
    #                 "engage in a helpful, detailed, polite conversation with a user."
    #             ),
    #         },
    #         {
    #             "role": "user",
    #             "content": f"Write a 12 line short beautiful poem inspired by this quote: '{quote}. Only respond with the poem, no other message needed.'"
    #         },
    #     ]
    #     try:
    #         response = client.chat.completions.create(
    #             model="llama-3-sonar-large-32k-online",
    #             messages=messages,
    #         )
    #         return response.choices[0].message.content
    #     except AuthenticationError as e:
    #         return f"Authentication error from Perplexity: {e}"
    #     except Exception as e:
    #         return f"Error generating poem from Perplexity: {e}"
    # else:
    #     raise ValueError(f"Invalid poem source: {source}")

if __name__ == "__main__":
    quote = "The mind is everything. What you think you become. - Buddha"
    source = 'Gemini'  # This is only used if you run generatePoem.py on its own for testing. 
    poem = generate_poem_from_source(quote, source)
    print(poem)

# you can change source to 'Gemini', 'OpenAI', 'Perplexity' ONLY GEMINI WORKS AT THE MOMENT for free.
def generate_poem(poem_source: str = 'Gemini', quote: str = "") -> str:
    poem_content = generate_poem_from_source(quote, poem_source)
    return poem_content
