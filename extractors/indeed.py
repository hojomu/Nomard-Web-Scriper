from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def get_page_count(keyword):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # --headless : scrapping 할 때 browser를 띄우지 않는다.
    #options.add_argument("--headless")
    # --disable-gpu : headless 사용시 발생하는 오류를 막아준다.
    #options.add_argument('--disable-gpu')

    browser = webdriver.Chrome(options=options)

    browser.get(f"https://kr.indeed.com/jobs?q={keyword}")

    soup = BeautifulSoup(browser.page_source, "html.parser")
    pagination = soup.find("nav", role="navigation")
    if pagination == None:
        return 1
    pages = pagination.find_all("div", recursive=False)
    count = len(pages)
    print(count)
    if count >= 5:
        return 5
    else:
        return count

def extract_indeed_jobs(keyword):
    pages = get_page_count(keyword)
    results = []
    for page in range(pages):
        base_url = "https://kr.indeed.com/jobs"
        final_url = f"{base_url}?q={keyword}&start={page*10}"
        print(final_url)

        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        #options.add_argument("--headless")
        #options.add_argument('--disable-gpu')


        browser = webdriver.Chrome(options=options)

        browser.get(final_url)

        soup = BeautifulSoup(browser.page_source, "html.parser")
        job_list = soup.find("ul", class_="jobsearch-ResultsList")
        jobs = job_list.find_all("li", recursive=False)
        for job in jobs:
            zone = job.find("div", class_="mosaic-zone")
            if zone == None:
                h2 = job.find("h2", class_="jobTitle")
                anchor = job.select_one("h2 a")
                title = anchor['aria-label']
                link = anchor['href']
                company = job.find("span", class_="companyName")
                location = job.find("div", class_="companyLocation")
                job_data = {
                    'link' : f"https://kr.indeed.com{link}",
                    'company' : company.string.replace(","," "),
                    'location' : location.string.replace(","," "),
                    'position' : title.replace(","," ").replace(" 전체 세부 정보", "")
                }
                results.append(job_data)
    return results