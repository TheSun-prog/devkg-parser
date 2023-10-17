import db
import parser


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
    db.insertInfo(info)
    return ''


def getVacancyDescription(url):
    return parser.parseJobDescription(url)


def convertFilterWords(words):
    solution = []
    filterTypes = words.split(',')
    for el in filterTypes:
        solution.append([])
        el = el.split()
        for word in el:
            solution[-1].append([word, 0, []])

    return solution


def filteringJobsProccess(filterWords, jobsToFilter):
    before = len(jobsToFilter)
    for job in jobsToFilter:
        for section in filterWords:
            for technology in section:
                if technology[0] in job[0] or technology[0] in job[1]:
                    technology[1] += 1
                    technology[2].append(job[2])
                    try:
                        jobsToFilter.remove(job)
                    except Exception:
                        pass
                    break

    for section in filterWords:
        for technology in section:
            print(technology[0], technology[1])
    print(before, len(jobsToFilter))

    for job in jobsToFilter:
        print(job[0])


def filterJobs(filterWords):
    filteringJobsProccess(convertFilterWords(filterWords), db.getInfoForFilter())


