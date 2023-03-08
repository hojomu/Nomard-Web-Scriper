from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from extractors.wwr import extract_wwr_jobs

options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

browser = webdriver.Chrome(options=options)

browser.get("https://kr.indeed.com/jobs?q=python&l=&from=searchOnHP&vjk=1015284880e2ff62")

print(browser.page_source)

'''
if response.status_code != 200:
    print("Can't request page")
else:
    soup = BeautifulSoup(response.text, "html.parser")
    job_list = soup.find("ul", class_="jobsearch-Resultslist")
    jobs = job_list.find_all('li', recursive=False)
    '''