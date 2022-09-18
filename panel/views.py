from django.http import HttpResponse, HttpRequest

def index(request: HttpRequest):
    return HttpResponse("Panel page will be here")
