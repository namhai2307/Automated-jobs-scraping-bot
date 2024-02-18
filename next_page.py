#import relevant module
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
next_lst = []         
def next(url):
    url_tem = url
    #extract raw html
    response = requests.get(url_tem)
    soup = BeautifulSoup(response.text, 'html.parser')
    next_card = soup.find_all('li', 'y735df0 _1iz8dgsa6 _1iz8dgs9v _1iz8dgsw')
    for n_link in next_card:
        n_link = n_link.find('a').get('href')
        next_lst.append("https://www.seek.com.au"+str(n_link))
        if n_link != None:
            return next("https://www.seek.com.au"+str(n_link))
        else: 
            break
    print(response)
    print(next_lst)
    print(len(next_lst))
#print(next_card)
next("https://www.seek.com.au/automation-engineer-jobs/in-All-Perth-WA?classification=1223%2C1209&subclassification=6224%2C6225%2C6023%2C6028%2C6031%2C6035%2C6036%2C6037%2C6042")
with open('test_file.csv', 'r') as file:
    with open('test_file.csv', 'w') as file:
        file.write('link' + "/n")
        for i in next_lst:
            file.write(i + '/n')