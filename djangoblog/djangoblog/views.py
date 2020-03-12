from django.http import HttpResponse

def homepage(request):
    return HttpResponse('home')

def about(request):
    return HttpResponse('about')