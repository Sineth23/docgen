import os
import requests
from dotenv import load_dotenv

load_dotenv()

def update_page(page_id, version, title, content, email, username, spacekey, passport):
    # Construct the base URL for updating the page
    base_url = f"https://{username}.atlassian.net/wiki/rest/api/content/{page_id}"

    # Prepare the data payload for updating the page
    data = {
        "version": {
            "number": version
        },
        "type": "page",
        "title": title,
        "space": {
            "key": spacekey
        },
        "body": {
            "storage": {
                "value": content,
                "representation": "storage"
            }
        }
    }

    # Send a PUT request to update the page
    response = requests.put(
        base_url, 
        json=data, 
        auth=(email, password)
    )

    if response.status_code != 200:
        # Handle failed page update
        print("Failed to update page.")
        print(response.json())
    else:
        # Handle successful page update
        print("Page updated successfully.")
        print(response.json())
