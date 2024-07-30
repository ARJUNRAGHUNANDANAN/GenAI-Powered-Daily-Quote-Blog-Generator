import requests
import json
from datetime import datetime
import os

def get_quote_of_the_day():
    """Fetches the quote of the day from a free API and returns it as a JSON response."""
    url = "https://api.quotable.io/random"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        quote = data['content']
        author = data['author']
        date = datetime.now().strftime("%Y-%m-%d")
        quote_data = {"date": date, "quote": quote, "author": author}
        return quote_data
    else:
        return None

def load_quotes_from_file():
    """Loads quotes from Quotes.json file, or returns an empty list if file does not exist or is empty."""
    if os.path.exists("Quotes.json"):
        with open("Quotes.json", "r") as file:
            quotes = json.load(file)
            if quotes:
                return quotes
    return []

def save_quote_to_file(quote_data):
    """Saves the quote data to Quotes.json file."""
    quotes = load_quotes_from_file()
    quotes.append(quote_data)
    with open("Quotes.json", "w") as file:
        json.dump(quotes, file, indent=4)

def main():
    quote_data = get_quote_of_the_day()
    if quote_data:
        quotes = load_quotes_from_file()
        if not quotes:
            # Create initial Quotes.json file with the first quote
            save_quote_to_file(quote_data)
            print(f"Quotes.json created with initial quote: {quote_data}")
        else:
            save_quote_to_file(quote_data)
            print(f"Quote appended to Quotes.json: {quote_data}")
    else:
        print("Error fetching quote")

if __name__ == "__main__":
    main()
