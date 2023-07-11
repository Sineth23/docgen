import os
from list_files import list_files
from cleanup_file import cleanup_file
from create_page import create_page

def main():
    # Ask the user to choose a file     
    directory = str(input("directory?"))
    email = str(input("confluence email?"))
    username = str(input("confluence username?"))
    password = str(input("confluence apikey?"))
    spacekey = str(input("confluence spacekey?"))
    files  = list_files(directory)
    
    for filename in files:

    # Extract the title from the filename
        title = os.path.splitext(filename)[0]
        
        # Clean up the file content based on its format
        content = cleanup_file(filename,directory)

        # Create a Confluence page with the title and content
        create_page(title, content, email, username, spacekey, password)

if __name__ == "__main__":
    # The main function is executed when the script is run directly
    main()
