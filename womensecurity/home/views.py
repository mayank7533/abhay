from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from twilio.rest import Client
import json
import requests
from flask import *
from django.http import HttpResponseRedirect
from pprint import pprint
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from django.template import loader
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
import pprint
import json
from flask import *
from rest_framework import status
import requests
import random
import urllib.request
import urllib.parse
# Create your views here.

class UserRegister(APIView):
    def post(self,request):
        name=request.POST['name']
        password=request.POST['password']
        userId=request.POST['userid']
        phone = request.POST['phone']
        interest = request.POST['interest']
        userObjects = User.objects.all()
        success = 1
        responseDictionary = dict()
        for userObject in userObjects:
            if userObject.userId == userId:
                success = 0

        if success==1:
            userObj = User.objects.create(
                name=name,
                userId = userId,
                password = password,
                contact = phone,
                verificationCode = 000000,
                location = "26.884570, 80.995931",
                fieldOfInterest = interest,
                message = "Joined abhay",
            )
            userObj.save()
        responseDictionary['success'] = 1
        if success==0:
            return HttpResponse('registration failed')
        else :
            return HttpResponse(json.dumps(responseDictionary))


class UserLogin(APIView):
    def post(self,request):
        userId = request.POST['id']
        password = request.POST['password']
        userObjects = User.objects.all()
        success = 0
        responseDictionary = dict()
        for userObject in userObjects:
            if userObject.userId == userId and userObject.password == password:
                success = 1
                responseDictionary['name'] = userObject.name
                responseDictionary['interest'] = userObject.fieldOfInterest
                responseDictionary['id'] = userObject.id
        if success == 1:
            return HttpResponse(json.dumps(responseDictionary))
        else:
            return HttpResponse("unsuccessful")



class LocationUpdate(APIView):
    def post(self,request):
        userId = request.POST['id']
        lat = request.POST['currentlat']
        long = request.POST['currentlong']
        userObjects = User.objects.all()
        for userObject in userObjects:
            if userObject.userId == userId:
                location = str(lat)+","+str(long)
                userObject.location = location
                userObject.save()
        return HttpResponse('success')



class RequestOtp(APIView):
    def post(self,request):

        userId = request.POST['id']
        verification = random.randint(100000, 999999)
        userObjects = User.objects.all()
        responseDictionary = dict()
        success = 0
        for userObject in userObjects:
            if userObject.userId == userId:
                userObject.verificationCode = verification
                responseDictionary['otp'] = verification
                success = 1
                userObject.save()
        if success == 1:
            return HttpResponse(json.dumps(responseDictionary))
        else:
            return HttpResponse("failed")


class Message(APIView):
    def post(self,request):
        userId = request.POST['id']
        message = request.POST['message']
        date = request.POST['date']
        time = request.POST['time']
        userObjects = User.objects.all()
        for userObject in userObjects:
            if userObject.userId == userId:
                messageObject = Messages.objects.create(
                message=message,
                time = time,
                date = date,
                user = userObject,

                )
                messageObject.save()
        return HttpResponse("success")


class Sos(APIView):
    def post(self,request):
        userId = request.POST['id']

        parentObjects = Parent.objects.all()
        for parentObject in parentObjects:
            if parentObject.user.userId == userId:
                no = '91'+str(parentObject.user.contact)
                print(no)
                msg = str(parentObject.user.name)+" needs your help, last known location "+str(parentObject.user.location)+". Contact no "+str(parentObject.user.contact)
                contactNo = parentObject.contact
                data = urllib.parse.urlencode({'apikey': 'CH7rpIHvxIo-iOJr7LJjAHx0TodOyck3wGkVL5VjgR	', 'numbers': no,
                                               'message': msg})
                data = data.encode('utf-8')
                request = urllib.request.Request("https://api.textlocal.in/send/?")
                f = urllib.request.urlopen(request, data)
                fr = f.read()
                print(fr)
        return HttpResponse("success")



def home(request):
    template = loader.get_template('home/index.html')
    context = {
        'registrationfailed': 0,
        'loginfailed': 0,
    }
    return HttpResponse(template.render(context, request))





def register(request):
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    userId = request.POST['userId']
    verification = request.POST['verification']
    contact = request.POST['contact']
    userObjects = User.objects.all()

    exists = 0

    for userObject in userObjects:
        if userObject.userId == userId and userObject.verificationCode == verification:
            exists = 1
            parentObject = Parent.objects.create(
                name = name,
                userId = username,
                password = password,
                user = userObject,
                contact = contact,
            )
            parentObject.save()
            template = loader.get_template('home/index.html')
            context = {
                'registrationfailed': 0,
                'loginfailed': 0,
            }


    if(exists == 0):
        template = loader.get_template('home/index.html')
        context = {
            'registrationfailed': 1,
            'loginfailed': 0,
        }

    return HttpResponse(template.render(context,request))


def login(request):
    userId = request.POST['username']
    password = request.POST['password']
    parentObjects = Parent.objects.all()
    success=0
    for parentObject in parentObjects:
        if parentObject.userId == userId and parentObject.password == password:
            lat,long = parentObject.user.location.split(',')
            messageObjects = Messages.objects.all()
            messages = []
            for messageObject in messageObjects:
                if messageObject.user.userId == parentObject.user.userId:
                    message = dict()
                    message['message']=messageObject.message
                    message['date']=messageObject.date
                    message['time']=messageObject.time
                    messages.append(message)
            success=1
            template = loader.get_template('home/dashboard.html')
            context = {
                'registrationfailed': 0,
                'loginfailed': 0,
                'username' : parentObject.name,
                'messages' : messages,
                'lat' : lat,
                'long' : long,
            }
    if success==0:
        template = loader.get_template('home/index.html')
        context = {
            'registrationfailed': 0,
            'loginfailed': 1,
        }
    return HttpResponse(template.render(context,request))