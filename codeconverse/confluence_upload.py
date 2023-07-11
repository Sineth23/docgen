import os
import re
import requests
from atlassian import Confluence
from urllib.parse import urlparse, unquote
import mistune

class ConfluenceRenderer(mistune.Renderer):
    # Custom renderer for mistune to convert Markdown to Confluence markup
    def heading(self, text, level):
        return f"<h{level}>{text}</h{level}>\n\n"

    
    def blank_line(self, token=None, state=None):
        return '\n'

    def list(self, body, ordered=True):
        list_type = "#" if ordered else "*"
        if isinstance(body, str):
            return f"{list_type} {body}\n"
        elif isinstance(body, list):
            items = "".join(f"{list_type} {self.render(item)}\n" for item in body)
            return items


    def list_item(self, text):
        return text

    def paragraph(self, text):
        return '{}\n'.format(text)

    def table(self, header, body):
        return '||' + '||'.join(header.split('|')) + '||\n' + body + '\n'

    def table_row(self, content):
        return '|' + '|'.join(content.split('|')) + '|\n'

    def table_cell(self, content, **flags):
        return content + '|'
    
    def inline_code(self, text):
        return f"{{{text}}}"

    def codespan(self, text):
        return f"{{{{code}}}}{text}{{{{code}}}}"
    
    def inline_math(self, text):
        return text  # Replace with suitable Confluence markup or plain text
   
    def block_quote(self, text):
        body = self.render_inner(text)
        return f"bq. {body}\n\n"

    def link(self, link, title, text):
        return '[{}|{}]'.format(text, link)
    
    def unknown_block(self, text):
        return text
    
    def unknown_inline(self, text):
        return text
    
    def render_inner(self, token):
        if isinstance(token, str):
            return token
        children = token.get("children", [])
        return "".join(self.render(child) for child in children)

def sanitize_text(text):
    # Remove unsupported macros or syntax
    text = re.sub(r'\{[^}]+\}', '', text)  # Remove macros enclosed in curly braces
    text = re.sub(r'\[\[.*?\]\]', '', text)  # Remove Confluence-style links

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    return text

def convert_to_confluence_markup(text):
    # Function to convert Markdown to Confluence markup
    sanitized_text = sanitize_text(text)

    renderer = ConfluenceRenderer()
    markdown = mistune.Markdown(renderer=renderer)
    return markdown(sanitized_text)

def get_google_doc_content(url):
    # Function to download Google Docs as plain text
    google_export_url = url.replace('/edit', '/export?format=txt')
    response = requests.get(google_export_url)
    response.raise_for_status()  # Ensure we got a valid response
    return convert_to_confluence_markup(response.text)

def create_page_and_attach_file(confluence, space, title, body, filename, content):
    # Function to create a new Confluence page and attach a file
    try:
        result = confluence.create_page(space, title, body)
        page_id = result['id']
        attachment = confluence.create_attachment(
            page_id=page_id,
            title=filename,
            file=content.encode(),
            content_type='application/octet-stream'
        )
        attachment_id = attachment['id']
        print(f"Successfully created page and attached file {filename} (Attachment ID: {attachment_id})")
    except Exception as e:
        print(f"Failed to create page or attach file: {str(e)}")


def list_local_files():
    # Set your project's folder path here
    path = 'C:/Users/areeb/hello/RepoReader/'
    return [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

def get_user_input():
    local_files = list_local_files()

    # Enumerate over the local files and print them out with their index
    for i, file in enumerate(local_files):
        print(f'{i}: {file}')

    while True:
        print('Select a local file number from the list:')
        user_input = input()
        
        try:
            file_index = int(user_input)
            if file_index < 0 or file_index >= len(local_files):
                raise ValueError('Invalid file index.')
            return local_files[file_index]
        except ValueError:
            print('Invalid input. Please enter a valid local file number.')

def main():
    # Main function to run the script
    try:
        confluence = Confluence(
            url='https://autodocai.atlassian.net/wiki',
            username='areebilyasmianoor@gmail.com',
            password='ATATT3xFfGF0_qe3OAKh19g1Y0VS8rVMGV94njPxHQkPdmd4MhmLV_6EngAx1I97HEP0FAOSUhxeshmJu_AuPAZ52HDQy9GmIK7yUg0ZmhX46PPC_XydHFt7CpA6eiwIu08U3tgUh1TIdADVqJf1nlzzwpR3Y88uVwgXo9SGNUu2PPjlxFu7uOk=9646ECF3'
        )
    except Exception as e:
        print(f"Failed to connect to Confluence: {str(e)}")
        return

    space = '~5b3f83822485ad2dbd803989'

    filepath_or_url = get_user_input()

    if filepath_or_url.startswith('http'):
        filename = unquote(urlparse(filepath_or_url).path.split('/')[-1]) + '.txt'
        body = get_google_doc_content(filepath_or_url)
    else:
        filename = filepath_or_url
        with open(filename, 'r') as f:
            content = f.read()
        body = convert_to_confluence_markup(content)
        
    title = os.path.splitext(filename)[0]
    create_page_and_attach_file(confluence, space, title, body, filename, body)

if __name__ == "__main__":
    main()
