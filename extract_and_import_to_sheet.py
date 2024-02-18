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
                print(name)
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

    print(len(cards))
    print(response)
    print(lst_name)
    print(len(lst_salary))


extract("https://www.seek.com.au/Automation-Engineer-jobs/in-All-Australia")

with open('test.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header row
    writer.writerow(["Name", "Company", "Position", "Location", "Salary", "Level", "Link to jobs"])
    
    # Write data rows
    for data in zip(lst_name, lst_company, lst_position, lst_location, lst_salary, lst_level, lst_links):
        writer.writerow(data)
