from django.shortcuts import render
from django.http import HttpResponse

# Import your script or integrate its functions here

def home(request):
    if request.method == "POST":
        repo_name = request.POST.get('repo_name')
        repo_url = request.POST.get('repo_url')
        
        # Call your script functions here
        # ...
        
        return HttpResponse("Task submitted!")

    return render(request, 'home.html')
