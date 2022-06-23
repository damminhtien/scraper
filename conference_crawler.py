from numpy import False_
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

session = requests.Session()

PAGE_RANGE = range(1, 10)
start_month_year = 'October, 2022'
end_month_year = 'March, 2023'
URL_CI = "https://conferenceindex.org/conferences/computer-science"
URL_SJR = "https://www.scimagojr.com/"
URL_SJR_SEARCH = "https://www.scimagojr.com/journalsearch.php"

start_datetime_object = datetime.strptime(start_month_year, '%B, %Y')
end_datetime_object = datetime.strptime(end_month_year, '%B, %Y')

list_conferences = []

print("Start scraping conferences on conferencindex ============")

for page in PAGE_RANGE:
    r = session.get(URL_CI, params={'page': page})
    html_soup = BeautifulSoup(r.text, 'html.parser')
    # print(html_soup)
    div_card_years = html_soup.find_all(class_='card-year')
    # print(len(div_card_years))
    for div_card_year in div_card_years:
        div_card_header = div_card_year.find(class_='card-header')
        date_month_year = div_card_header.text.strip()
        # print(date_month_year)

        datetime_object = datetime.strptime(date_month_year, '%B, %Y')
        if (start_datetime_object < datetime_object and end_datetime_object > datetime_object):
            print("Checking conferences in ", date_month_year)
            div_conferences = div_card_year.find_all(class_='card-body')
            for div_conference in div_conferences:
                a_conferences = div_conference.find_all(['a'])
                for a_conference in a_conferences:
                    list_conferences.append(a_conference.text.strip())
                    print(a_conference.text.strip())


print("\nThere are {} conferences from {} to {}".format(len(list_conferences), start_month_year, end_month_year))


# Extract conference's strings to ISSN
list_conferences_issn = []
for conference in list_conferences:
    try:
        issn = re.findall(r"\((.+?)\)", conference)
        if (len(issn) < 1): 
            continue
        list_conferences_issn.append(issn[0])
    except AttributeError:
        print('Failed to extract ISSN from conference')
print(list_conferences_issn)

print("\nStart checking conferences on SJR ============")
print("Potential conferences:")

list_potientail_conferences = []
for issn in list_conferences_issn:
    r = session.get(URL_SJR_SEARCH, params={'q': issn})
    html_soup = BeautifulSoup(r.text, 'html.parser')
    div_search_results = html_soup.find(class_='search_results')
    if (len(div_search_results)):
        a_search_result =  div_search_results.find_all('a', href=True)
        if (len(a_search_result) < 1):
            continue
        hindexs = []
        conferences_info = []
        for a in a_search_result:
            r_conference = session.get(URL_SJR + a['href'])
            html_soup_conference = BeautifulSoup(r_conference.text, 'html.parser')
            div_hindexnumber = html_soup_conference.find(class_='hindexnumber')
            hindex = div_hindexnumber.text.strip()
            hindexs.append(int(hindex))
            h1_name_conference = html_soup_conference.find(['h1'])
            conferences_info.append("h-index: {} {} {}".format(hindex, h1_name_conference.text.strip(), URL_SJR + a['href']))
        is_smaller_than_8 = True
        for hindex in hindexs:
            if (hindex >= 8):
                is_smaller_than_8 = False
                break
        if (is_smaller_than_8):
            continue
        list_potientail_conferences.append(issn)
        print(issn)
        for conference_info in conferences_info:
            print(conference_info)
        print('================================\n')
print("Found {} potential conferences".format(len(list_potientail_conferences)))
