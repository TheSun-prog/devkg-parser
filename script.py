import sqlite3
import requests
from bs4 import BeautifulSoup as BS

url = 'https://devkg.com'


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
        statusCode = getMainInfo(jobInfo, href)
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


def getMainInfo(jobInfo, url):
    elText = jobInfo.text.split('\n')

    for num in range(-4, 1):
        elText.pop(num * -2)

    info = []
    for txt in elText:
        info.append(txt.strip())
    info.append(url)

    if info[2] == '-':
        return 'stop'

    info.append(getVacancyDescription(url))
    insertInfo(info)
    return ''


def insertInfo(values):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
        company TEXT,
        vacancy TEXT,
        salary TEXT,
        type TEXT,
        url TEXT,
        description TEXT
    )""")
    con.commit()
    cur.execute('INSERT INTO jobs VALUES(?, ?, ?, ?, ?, ?)', tuple(values))
    con.commit()
    con.close()


def getInfoForFilter():
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS jobs(
        company TEXT,
        vacancy TEXT,
        salary TEXT,
        type TEXT,
        url TEXT,
        description TEXT
    )""")
    con.commit()

    solution = []
    cur.execute('SELECT * FROM jobs')
    rec = cur.fetchall()

    for el in rec:
        vacancy = el[1].lower().strip()
        description = el[5].lower().strip()
        solution.append([vacancy, description])

    con.commit()
    con.close()
    return solution


def getVacancyDescription(url):
    return parseJobDescription(url)


def start():
    parseAllPages(1)
    print('Proccess was finished')


def getInfo():
    return getInfoForFilter()


l1 = getInfo()
for el in l1:
    print(el[0])

