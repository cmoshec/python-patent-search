from bs4 import BeautifulSoup
import requests
import re
import csv
import random
from time import sleep

print('Searching patents:')

phrase1='phytoene'
pubNum=[]
with open('results.csv','r') as csv_file_read:
    csv_reader=csv.reader(csv_file_read)
    for line in csv_reader:
        print(line[0])
        pubNum.append(line[0])


    csv_file=open('Patents.csv','w')
    csv_writer=csv.writer(csv_file)
    csv_writer.writerow(['Title','Pub number','Assignee','Issue Date','Description','Claim 1','Link',phrase1])


for pn in pubNum:

    url='https://patents.google.com/patent/'+pn
    r = requests.get(url)
    data = r.text

    soup = BeautifulSoup(data,'html.parser')

    title = soup.findAll(attrs={"name": re.compile("DC.title")})
    print('\n', 'Title: ', title[0]['content'])

    pubNumber= soup.find('dd', itemprop='publicationNumber').text
    print('Publication: ',pubNumber,'\n')

    assignee= soup.find('dd', itemprop='assigneeOriginal', repeat="").text
    print('Assignne: ',assignee,'\n')

    datesub = soup.findAll(attrs={"name": re.compile("DC.date", re.I),"scheme": re.compile("dateSubmitted", re.I)})
    print('Date: ',datesub[0]['content'],'\n')

    claim= soup.find('div', class_='claim-text').text
    print('Claim : ',claim, '\n')

    if phrase1 in claim:
        print(phrase1,' found in claim 1')
        found='found'
    else:
        print(phrase1,' not found in claim 1')
        found = 'not found'

    csv_writer.writerow([title[0]['content'],pubNumber,assignee,datesub[0]['content'],claim,url,found])

    delay = 25 + random.random()*10
    some_randomnum = random.randint(1,10)
    delay += random.uniform(0,some_randomnum)
    time_output = "\ndelaying for " + str(delay) + " seconds"
    print (time_output)
    sleep(delay)

csv_file.close()
csv_file_read.close()



