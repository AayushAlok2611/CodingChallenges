from django.http import HttpResponse
from django. views. decorators. csrf import csrf_exempt

@csrf_exempt
def test_view(request):
    if request.method == 'GET':
        return HttpResponse("GET Request")

    if request.method == 'POST':
        return HttpResponse('POST Request')
    
    if request.method == 'DELETE':
        return HttpResponse('DELETE Request')
    
    return HttpResponse('Hello from URL Shortener App')