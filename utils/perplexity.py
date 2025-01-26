import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables
perplexity_api_key = os.getenv("PERPLEXITY_API_KEY")

def fetch_structured_data_from_perplexity(query):
    """
    Fetch structured data (name and email) from the Perplexity API based on the query.
    """
    url = "https://api.perplexity.ai/chat/completions"
    headers = {"Authorization": f"Bearer {perplexity_api_key}"}
    
    # Define the request payload
    payload = {
        "messages": [
            {"role": "user", "content": query + " Provide the response as a structured JSON with name and email."}
        ],
        "model": "sonar",  # Replace with the appropriate model name
        "response_format": {
            "type": "text"  # Keep the response as raw text for now
        },
        "temperature": 0.2,
        "max_tokens": 500
    }

    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=payload)

        # Handle the response
        if response.status_code == 200:
            data = response.json()

            # Debug: Log the parsed JSON data
            print("Parsed JSON Data:", data)

            # Extract text response and citations
            choices = data.get("choices", [])
            raw_text = choices[0].get("message", {}).get("content", "") if choices else ""
            citations = data.get("citations", [])

            # Debug: Log raw text response and citations
            print("Raw Text Response:", raw_text)
            print("Citations:", citations)

            # Parse the raw text for potential email addresses
            structured_data = []
            lines = raw_text.split("\n")
            print("Lines to Parse:", lines)  # Debug: Check the lines being parsed
            for line in lines:
                if "@" in line:  # A basic check to identify emails
                    parts = line.split("-")
                    if len(parts) == 2:
                        name = parts[0].strip()
                        email = parts[1].strip()
                        structured_data.append({"name": name, "email": email})

            # If no emails are found, include the citations as additional output
            if not structured_data:
                structured_data = [{"citation": url} for url in citations]

            # Debug: Log the final structured data
            print("Structured Data:", structured_data)

            return structured_data
        else:
            print(f"Error {response.status_code}: {response.text}")
            return []
    except Exception as e:
        print(f"Exception occurred while fetching data from Perplexity: {str(e)}")
        return []