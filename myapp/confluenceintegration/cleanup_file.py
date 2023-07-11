import os
import pandas as pd
from markdown import markdown
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def cleanup_file(filename,directory):
    # Define the directory where the files are located
   
    directory = f"/home/ec2-user/myproject/{directory}/.autodoc/docs/markdown"

    # Create the file path by combining the directory and filename
    filepath = os.path.join(directory, filename)

    # Get the file extension
    file_extension = os.path.splitext(filename)[1]

    if file_extension == '.txt':
        # Read the content of a text file
        with open(filepath, 'r') as file:
            content = file.read()

    elif file_extension == '.md':
        # Read the content of a Markdown file and convert it to HTML
        with open(filepath, 'r') as file:
            content = file.read()
        content = markdown(content)

    elif file_extension == '.html':
        # Read the content of an HTML file
        with open(filepath, 'r') as file:
            content = file.read()

    elif file_extension == '.pdf':
        # Convert a PDF file to HTML
        content = convert_pdf_to_html(filepath)

    elif file_extension == '.csv':
        # Read a CSV file and convert it to an HTML table
        df = pd.read_csv(filepath)
        content = df.to_html(index=False)

    else:
        # Handle unsupported file formats
        print(f"Unsupported file format: {file_extension}")
        return None

    # Basic cleanup: remove any leading/trailing whitespace
    content = content.strip()
    return content

def convert_pdf_to_html(filepath):
    content = ''

    # Extract text content from each page of the PDF
    for page_layout in extract_pages(filepath):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            # Append the text character to the content
                            content += character.get_text()
                    # Add a new line after each text line
                    content += '\n'

    return content
