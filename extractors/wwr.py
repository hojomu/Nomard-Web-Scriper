from requests import get
from bs4 import BeautifulSoup

def extract_wwr_jobs(keyword):
    base_url = "https://weworkremotely.com/remote-jobs/search?term="
    response = get(f"{base_url}{keyword}")
    if response.status_code != 200:
        print("Can't request website")
    else:
        results = [] # job_data를 담기위해 list 선언
        soup = BeautifulSoup(response.text , "html.parser")
        jobs = soup.find_all('section', class_="jobs")
        for job_section in jobs:
            job_posts = job_section.find_all('li')
            job_posts.pop(-1)
            for post in job_posts:
                anchors = post.find_all('a') # post 내부의 모든 a태그를 찾는다
                anchor = anchors[1] # 찾은 a 태그 중 두번째 요소만 anchor에 저장
                link = anchor['href']
                # anchor의 span 중 첫 번째 칸에 company를, 나머지를 kind와 region에 넣는다
                company, kind, region = anchor.find_all('span', class_="company")
                # .find_all은 list를 가져오고 .find는 결과를 가져온다
                title = anchor.find('span', class_='title')
                job_data = {
                    'link' : f"https://weworkremotely.com{link}",
                    'company' : company.string,
                    'region' : region.string,
                    'position' : title.string
                }
                results.append(job_data)
        # 나중에 파일에 넣을 수 있게 return
        return results