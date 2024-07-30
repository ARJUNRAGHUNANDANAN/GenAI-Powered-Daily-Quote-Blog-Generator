#This is just a test code.  Moved on to use Google AI Studio API since I dont have OpenAI premium or API credits. Google AI Studio calls are currently free. 

import requests
import json
from datetime import datetime
from langchain.llms import OpenAI
from langchain.chains import  LLMChain
from langchain.prompts import PromptTemplate

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
        return json.dumps(quote_data)
    else:
        return "Error fetching quote"

def append_quote_to_file(quote_data):
    """Appends the quote data to the quotes.txt file."""
    with open("quotes.txt", "a") as f:
        f.write(quote_data + "\n")

def generate_poem(quote_data):
    """Generates a poem based on the quote using Gemini Pro."""
    llm = OpenAI(temperature=0.7, api_key="YOUR_OPENAI_API_KEY", engine="text-davinci-003")
    prompt_template = PromptTemplate(
        input_variables=["quote"],
        template="Write a 12-line inspirational poem based on the following quote:\n\n{quote}"
    )
    chain = LLMChain(llm=llm, prompt=prompt_template)
    poem = chain.run(quote_data['quote'])
    return poem

if __name__ == "__main__":
    quote_data = get_quote_of_the_day()
    if quote_data != "Error fetching quote":
        append_quote_to_file(quote_data)
        print(f"Quote appended to quotes.txt: {quote_data}")
        quote_data = json.loads(quote_data)
        poem = generate_poem(quote_data)
        with open("poem.txt", "w") as f:
            f.write(poem)
        print(f"Poem written to poem.txt: {poem}")
    else:
        print(quote_data)