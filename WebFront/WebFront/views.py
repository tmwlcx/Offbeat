from django.http import HttpResponse
 
def shout(request):
    return HttpResponse('This page is HERE')