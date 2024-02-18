#import relevant module
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
lst_links = []
lst_name = []
lst_company = []
big_lst = []
lst_location = []
lst_position = []
lst_salary = []
lst_level = []
#next_lst = []

#interacting with the web
def extract(url):
    url_tem = url
    #extract raw html
    response = requests.get(url_tem)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', 'y735df0 _1iz8dgs4y _1iz8dgs4w')

    #extracting data from each card
    for card in cards:
        link = card.find('a')
        link = link.get("href")
        if link != None:
            lst_links.append("https://www.seek.com.au"+str(link))
        #print(link)
    for i in lst_links:
        jobs_rep = requests.get(i)
        jobs_soup = BeautifulSoup(jobs_rep.text, 'html.parser')
        jobs_name = jobs_soup.find_all('div', 'y735df0 _1iz8dgs6q _1iz8dgs6v')
        jobs_company = jobs_soup.find_all('span', 'y735df0 _1iz8dgs4y _94v4w0 _94v4w1 _94v4w21 _1wzghjf4 _94v4wd')
        jobs_location = jobs_soup.find('span', 'y735df0 _1iz8dgs4y _1iz8dgsr')
        jobs_position = jobs_location.find_next('span', 'y735df0 _1iz8dgs4y _1iz8dgsr')
        jobs_level = jobs_position.find_next('span', 'y735df0 _1iz8dgs4y _1iz8dgsr')
        jobs_salary = jobs_level.find_next('span', 'y735df0 _1iz8dgs4y _1iz8dgsr')
        
        for name in jobs_name:
            name = name.h1
            if name != None:
                match = re.search(r">([^<]*)<", str(name))
                name = match.group(1)
                #print(name)
                lst_name.append(name)
        for company in jobs_company:
            if company != None:
                if company.find('a') != None:
                    match = re.search(r">([^<]*)</a", str(company))
                    company = match.group(1)
                else:
                    match = re.search(r">([^<]*)<", str(company))
                    company = match.group(1)
                #print(company)
                lst_company.append(company)
        for location in jobs_location:
            if location != None:
                lst_location.append(location)
                #print(location)
        for position in jobs_position:
            lst_position.append(position)
        for level in jobs_level:
            lst_level.append(level)
            
        big_lst.append(jobs_salary)
    for i in big_lst:
        if i != None:
            match = re.search(r">([^<]*)<", str(i))
            i = match.group(1)
            lst_salary.append(i)
        else:
            lst_salary.append("None")

    #going to the next pages
    next_card = soup.find_all('li', 'y735df0 _1iz8dgsa6 _1iz8dgs9v _1iz8dgsw')
    for n_link in next_card:
        n_link = n_link.find('a').get('href')
        #next_lst.append("https://www.seek.com.au"+str(n_link))
        if n_link != None:
            return extract("https://www.seek.com.au"+str(n_link))
        else: 
            break
    print(len(cards))
    print(response)
    print(lst_name)
    print(len(lst_salary))
    print(len(lst_company))
    print(len(lst_name))
    print(len(lst_position))
    print(len(lst_links))
    print(len(lst_location))
    print(len(lst_level))
extract("https://www.seek.com.au/jobs-in-engineering/in-All-Australia?subclassification=6023%2C6028%2C6022%2C6024%2C6027%2C6031%2C6035%2C6025%2C6036%2C6038%2C6037%2C6041%2C6040%2C6034")
#import all data into a spread sheet
with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header row
    writer.writerow(["Name", "Company", "Position", "Location", "Salary", "Level", "Link to jobs"])
    
    # Write data rows
    for data in zip(lst_name, lst_company, lst_position, lst_location, lst_salary, lst_level, lst_links):
        writer.writerow(data)
