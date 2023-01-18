from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
import sys, json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# third-party imports
from rest_framework.views import APIView
from sentiment import TwitterClient
@api_view(['GET','POST'])   
def post(request):
    params = json.loads(request.body)
    try:
        print('params : ', params)
        ap = TwitterClient().get_tweets(query = 'sports', count = 2000)
        return Response({
            "message": "success",
            "params": params,
        }, status = 200)
    except Exception as ex:
        print('::::: ERROR :: Error Fetching Tweet Details: '+ str(ex) + '\n')
        return Response({
            "message": "::::: ERROR :: Error Fetching Tweet Details: ",
            "error": str(ex)
        }, status = 500)
