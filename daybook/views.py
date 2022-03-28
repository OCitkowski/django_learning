from django.shortcuts import render
from django.http import HttpResponse

def index(reguest):
    ''' Mane page'''
    return render(reguest, 'daybook/index.html')
    # return HttpResponse("Hello, world. You're at the polls index.")