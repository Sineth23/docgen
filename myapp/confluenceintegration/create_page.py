import os
import requests
from .update_page import update_page
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_page(title, email, username, spacekey, password):
    # Base URL for Confluence API
    base_url = f"https://{username}.atlassian.net/wiki/rest/api/content"

    # Set the query parameters for the request
    params = {
        "title": title,
        "spaceKey": spacekey
    }

    # Send a GET request to retrieve the page
    response = requests.get(
        base_url, 
        params=params, 
        auth=(email, password)
    )

    if response.status_code != 200:
        # Handle failed request
        print("Failed to get page.")
        print(response.json())
        return None

    results = response.json().get("results", [])

    # Check if there are results.
    if results:
        # Get the page ID
        page_id = results[0]['id']

        # Make a second request to get the page history, which contains version info.
        response = requests.get(
            f"{base_url}/{page_id}/history",
            auth=(email, password)
        )

        if response.status_code == 200:
            # Get the version data
            version_data = response.json()

            # Attach version info to the original page data
            results[0]['version'] = version_data['lastUpdated']
            return results[0]
        else:
            # Handle failed request to get page version
            print("Failed to get page version.")
            print(response.json())
            return None
    else:
        return None

def create_page(title, content, email, username, spacekey, password):
    # Check if the page already exists
    existing_page = get_page(title, email, username, spacekey, password)

    if existing_page:
        # If the page exists, update it
        page_id = existing_page["id"]
        version = existing_page["version"]["number"] + 1
        update_page(page_id, version, title, content) 
    else:
        # If the page doesn't exist, create it
        base_url = f"https://{username}.atlassian.net/wiki/rest/api/content"
        headers = {
            "Content-Type": "application/json"
        }
        data = {
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
        
        # Send a POST request to create the page
        response = requests.post(
            base_url, 
            headers=headers, 
            json=data, 
            auth=(email, password)
        )

        if response.status_code != 200:
            # Handle failed request to create page
            print("Failed to create page.")
            print(response.json())
        else:
            # Page created successfully
            print("Page created successfully.")
            print(response.json())
