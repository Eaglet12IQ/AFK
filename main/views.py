from django.shortcuts import render

def main(request):
    return render(request, "main.html", {'user': request.user})

def top(request):
    return render(request, "top.html")
