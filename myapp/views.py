from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import time
import pexpect
import json             
from django.shortcuts import render
from .confluenceintegration.list_files import list_files
from .confluenceintegration.cleanup_file import cleanup_file
from .confluenceintegration.create_page import create_page
from .autodoc.main import autodoc




         
@csrf_exempt
def home(request):
    if request.method == 'POST': 
        # Retrieving form data
        repo_name = request.POST.get('repo_name')
        repo_url = request.POST.get('repo_url')
        email = request.POST.get('email')
        username = request.POST.get('username')
        spacekey = request.POST.get('spacekey')
        password = request.POST.get('password')
        directory = str(repo_name)


        openai_api_key = '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'

        try:
            child = pexpect.spawn('/bin/bash', timeout=120)  # Increase timeout to 120 seconds
            child.sendline('export OPENAI_API_KEY="{0}"'.format(openai_api_key))
            time.sleep(1)

            #child.sendline('git clone {0}'.format(repo_url))
            #time.sleep(5)

            #child.sendline('cd {0}'.format(repo_name))
            #time.sleep(1)

            #child.sendline('doc init')

            # Update expect calls to match exact prompts, or use more generic patterns
            #child.expect('Enter the name of your repository[:]?')  # Use regex to allow optional colon at the end
            #child.sendline(repo_name)

            #child.expect('Enter the GitHub URL of your repository[:]?')
            #child.sendline(repo_url)

            #child.expect('Select which LLMs you have access to')
            #child.sendline('GPT-3.5 Turbo')
            #time.sleep(5)

            #child.sendline('doc index')
            #child.expect('Do you want to continue with indexing\?')  # Escape question mark
            #child.sendline('Yes')
            #time.sleep(80)
            #print(child.before.decode())
            autodoc(repo_url)
         


            files  = list_files(directory)
    
            for filename in files:

                # Extract the title from the filename
                title = os.path.splitext(filename)[0]
                
                # Clean up the file content based on its format
                content = cleanup_file(filename,directory)

                # Create a Confluence page with the title and content
                create_page(title, content, email, username, spacekey, password)



            

 





            return JsonResponse({'status': 'success'})
        except pexpect.ExceptionPexpect as e:
            return JsonResponse({'error': 'Error during command execution', 'details': str(e)}, status=500)

    # If the request method is GET, render the HTML form
    elif request.method == 'GET':
        return render(request, 'home.html')
