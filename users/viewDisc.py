from django.shortcuts import render
from django.http import HttpResponse

from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError


def datacor(countrie):
    
    url = 'https://www.worldometers.info/coronavirus/country/'+countrie
    try:
        r = requests.get(url)
    
        r.raise_for_status()
        
        data = r.content
        soup = BeautifulSoup(data, 'html.parser')
        active_cases = soup.find_all('li', {"class": "news_li"})
    except HTTPError as hp:
         active_cases="error"
   
    params = {"active_cases": active_cases[0].text[:-9]}

    return (params)