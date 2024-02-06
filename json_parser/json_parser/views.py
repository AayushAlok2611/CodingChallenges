from django.http import HttpResponse
from django. views. decorators. csrf import csrf_exempt

# Surprisingly current working directory is Coding Challenges/json_parser and not Coding Challenges/json_parser/json_parser
from json_parser.JSONParsingService.json_parsing_service import JsonParsingService
import os
from json import detect_encoding



@csrf_exempt
def test_view(request):
    if request.method == 'GET':
        return HttpResponse("GET Request")

    if request.method == 'POST':
        return HttpResponse('POST Request')
    
    if request.method == 'DELETE':
        return HttpResponse('DELETE Request')
    
    return HttpResponse('Hello from URL Shortener App')

@csrf_exempt
def parse_json(request):
    json = request.body
    json_string = None
    

    # Got this piece of code from the "loads" function of json library
    if isinstance(json,str):
        json_string = json
    elif isinstance(json, (bytes,bytearray)):
        json_string = json.decode(detect_encoding(json), 'surrogatepass')
    else:
        raise Exception("Unknown format of incoming json")

    parsed_json = None

    if len(json_string) > 0:
        parsed_json = JsonParsingService(json_string).parse()
        
    return HttpResponse(parsed_json)
