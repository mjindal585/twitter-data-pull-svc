from django.shortcuts import render

from rest_framework.response import Response
import sys, json

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from sentiment import TwitterClient
@api_view(['GET','POST'])   
def post(request):
    params = json.loads(request.body)
    try:
        data = TwitterClient().get_tweets(query = params['query'], count = params['count'])
        return Response({
            "message": "success",
            "params": params,
            "data": data
        }, status = 200)
    except Exception as ex:
        print('::::: ERROR :: Error Fetching Tweet Details: '+ str(ex) + '\n')
        return Response({
            "message": "::::: ERROR :: Error Fetching Tweet Details: ",
            "error": str(ex)
        }, status = 500)
