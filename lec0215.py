import requests
from bs4 import BeautifulSoup

print('\n*********** Courses ***********')

CACHE_FNAME = "umsi_cache.json"
try:
    cache_file = open(CACHE_FNAME, "r")
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

baseurl = 'https://www.si.umich.edu/programs/courses/catalog'
header = {'User-Agent': 'SI_CLASS'}
page_text = requests.get(baseurl, headers=header).text
# print (page_text)
page_soup = BeautifulSoup(page_text, 'html.parser')
content_div = page_soup.find(class_='view-content')
# print (len(content_div))

table_rows = content_div.find('tbody').find_all('tr')
for tr in table_rows:
    print(tr)
    print('-'*20)


class CourseListing:
    def __init__(self, course_num, course_name):
        self.num = course_num
        self.name = course_name

def unique_i(baseurl, header):
    return baseurl + "_".join(header)

def get_details_cache(url):
    baseurl = "https://www.si.umich.edu/" + url
    header = {'User-Agent': 'SI_CLASS'}
    unique_ident = unique_i(baseurl, header)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        page_text = requests.get(baseurl, headers=header).text
        CACHE_DICTION[unique_ident] = page_text
        # dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME, "w")
        fw.write(str(CACHE_DICTION))
        fw.close()
        return CACHE_DICTION[unique_ident]
        # print(page_text)


course_num_list = []
course_name_list = []
course_link_list = []
for tr in table_rows:
    table_cells = tr.find_all('td')
    # print(len(table_cells))
    course_num_all = tr.find_all('td', class_ = 'views-field views-field-catalog')
    for ele in course_num_all:
        course_num = ele.find('a').text
        course_num_list.append(course_num)
        print(course_num)
        print('-'*20)
    course_name_all = tr.find_all('td', class_ = 'views-field views-field-title')
    for ele in course_name_all:
        course_name = ele.find('a').text
        course_name_list.append(course_name)
        print(course_name)
        print('-'*20)
        course_link = ele.find('a').get('href')
        course_link_list.append(course_link)
        page_text = get_details_cache(course_link)
        page_soup = BeautifulSoup(page_text, 'html.parser')
        content_div = page_soup.find('div', id ='content-inside')
        # print(content_div)
        description = content_div.find('p').text
        prerequisites = content_div.find('div', class_='course2prer').text
        if description != "":
            print(description)
        else:
            print("Course description: None")
        print('-'*20)
        if prerequisites != "":
            print(prerequisites)
        else:
            print("Requeired prerequisites: None")
        print('='*20)
        print("\n")
