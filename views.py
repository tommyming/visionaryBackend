from django.shortcuts import render
from django.http import HttpResponse
import requests

def post_request(request):
    if request.method == 'POST':
        data = request.POST
        print(data)
        print(data['image'])
        image = data['image']
        print(image)
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": "f6e4b8d1b3b8e4f4d7f8e4b8d1b3b8e4f4d7f8e4",
            "image": image
        }
        response = requests.post(url, payload)
        print(response.json())
        return HttpResponse(response.json())
    return HttpResponse("Not a post request")