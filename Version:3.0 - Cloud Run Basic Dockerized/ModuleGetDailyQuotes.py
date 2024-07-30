# GeminiBlog/Modules/ModuleGetDailyQuotes.py
# @arjunraghunandanan 2024
import requests
import json
import random
from datetime import datetime
import os
import sys
import logging

import dotenv
from dotenv import load_dotenv
load_dotenv()
# load_dotenv()  # Load environment variables from .env

# # Configure logging
# logging.basicConfig(filename='Logs/gemini_main.log', level=logging.INFO,
#                     format='%(asctime)s - %(levelname)s - %(filename)s - %(lineno)d - %(message)s')

class ResponseQuote:
    """Represents a quote response with date, content, and author."""
    def __init__(self, date: str, content: str, author: str, source: str):
        self.date = date
        self.content = content
        self.author = author
        self.source = source

    def __str__(self):
        return f"{{'date': '{self.date}', 'content': '{self.content}', 'author': '{self.author}', 'source': '{self.source}'}}"


def QuotablesIO():
    logging.info("Entering Inside QuotablesIO Function")
    """Fetches a random quote from QuotablesIO."""
    url = "https://api.quotable.io/random"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        logging.info(f"Quote fetched from QuotablesIO: {data}")
        # Remove apostrophes from content and author
        data['content'] = data['content'].replace("'", "")
        data['author'] = data['author'].replace("'", "")
        return ResponseQuote(date, data['content'], data['author'], 'QuotablesIO')
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching quote from QuotablesIO: {e}")
        raise Exception(f"Error fetching quote from QuotablesIO: {e}")
    except json.decoder.JSONDecodeError as e:
        logging.error(f"Error decoding JSON response from QuotablesIO: {e}")
        raise Exception(f"Error decoding JSON response from QuotablesIO: {e}")


def LocalQuoteIO():
    logging.info("Entering Inside LocalQuoteIO Function")
    """Fetches a quote from a local source (implement your logic here)."""
    with open("Backup_Repository/local_quotes.json", "r") as f:
        quotes = json.load(f)
    if quotes:
        random_quote = random.choice(quotes)
        logging.info(f"Quote fetched from local_quotes.json: {random_quote}")
        return ResponseQuote(random_quote['date'], random_quote['content'], random_quote['author'], 'LocalQuoteIO')
    else:
        logging.error("No quotes found in local_quotes.json")
        raise Exception("No quotes found in local_quotes.json")

def ZenQuotesIO() :
    logging.info("Entering Inside ZenQuotesIO Function")
    """Fetches a quote from ZenQuotesIO."""
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:  
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            logging.info(f"Quote fetched from ZenQuotesIO: {data}")
            # Remove apostrophes from content and author
            data[0]['q'] = data[0]['q'].replace("'", "")
            data[0]['a'] = data[0]['a'].replace("'", "")
            return ResponseQuote(date, data[0]['q'], data[0]['a'], 'ZenQuotesIO') 
        else:
            logging.error("Invalid response format from ZenQuotesIO")
            raise Exception("Invalid response format from ZenQuotesIO")
    else:
        logging.error(f"Error fetching quote from ZenQuotesIO: {response.text}")
        raise Exception(f"Error fetching quote from ZenQuotesIO: {response.text}")
        
def fetch_daily_quote(source: str):
    """Fetches a daily quote based on the specified source."""
    try:
        if source == 'QuotablesIO':
            quote = QuotablesIO()
        elif source == 'LocalQuoteIO':
            quote = LocalQuoteIO()
        elif source == 'ZenQuotesIO':
            quote = ZenQuotesIO()
        else:
            raise ValueError(f"Invalid quote source: {source}")
        return str(quote)
    except ValueError as e:
        logging.error(f"Error: {e}")
        print(f"Error: {e}")
        print("Due to this, for now, defaulting to a random quote from local_quotes.txt.")
        quote = LocalQuoteIO()
        logging.info(f"Defaulting to a random quote from local_quotes.txt: {quote}")
        return str(quote)

# you can change source to 'QuotablesIO', 'LocalQuoteIO', 'ZenQuotesIO' ALL ARE WORKING
def fetch_daily_quote_from_source(quote_source: str):
    """Fetches a daily quote from the specified source, handling errors gracefully."""
    try:
        quote_response = fetch_daily_quote(quote_source)
        # Remove single quotes from the quote response before parsing
        quote_response = quote_response.replace("'", '"')
        quote_data = json.loads(quote_response)
        logging.info(f"Quote data returned to main: {quote_data}")
        return {"quote": quote_data['content'], "author": quote_data['author'], "source": quote_data['source']}
    except Exception as e:  # Catch all exceptions for more robust error handling
        logging.error(f"Error fetching quote from {quote_source}: {e}")
        print(f"Error fetching quote from {quote_source}: {e}")
        print("Defaulting to a random quote from local_quotes.json.")
        quote_data = json.loads(fetch_daily_quote('LocalQuoteIO').replace("'", '"'))
        logging.info(f"Defaulting to a random quote from local_quotes.json: {quote_data}")
        return {"quote": quote_data['content'], "author": quote_data['author'], "source": quote_data['source']}

if __name__ == "__main__":
    quote_source = "LocalQuoteIO"  # Only to test other sources when running FetchDailyQuotes.py by itself
    quote_response = fetch_daily_quote_from_source(quote_source)
    print(f"Quote Response: {quote_response}")
