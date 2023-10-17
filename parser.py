import requests
from bs4 import BeautifulSoup as BS

import proccesing

url = 'https://devkg.com'

jobsList = []


def parseAllPages(pageNum):
    print(pageNum)
    pageUrl = url + f'/ru/jobs?page={pageNum}'
    req = requests.get(pageUrl)
    pageHtml = BS(req.content, 'lxml')
    pageJobs = pageHtml.find('div', class_="jobs-list").findAll('article', class_="item")

    statusCode = ''

    jobsCount = len(pageJobs)
    quaterPart = jobsCount/4
    num = 0

    for jobInfo in pageJobs:
        href = url + jobInfo.find('a', class_='link').get('href')
        statusCode = proccesing.getMainInfo(jobInfo, href)
        if statusCode == 'stop':
            return

        num += 1
        if num == quaterPart:
            print('25%')
        elif num == quaterPart * 2:
            print('50%')
        elif num == quaterPart * 3:
            print('75%')

    if statusCode == 'stop':
        return
    else:
        parseAllPages(pageNum + 1)


def parseJobDescription(url):
    req = requests.get(url)
    pageHtml = BS(req.content, 'lxml')
    return pageHtml.find('main', class_='job-body').text
