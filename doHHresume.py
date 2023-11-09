# import requests
# from bs4 import BeautifulSoup 
from os import name
import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
import json


class HHresume:
    def get_resume_soap(urlResume):
        ua =fake_useragent.UserAgent()
        res = requests.get(
            # url = f"https://spb.hh.ru/applicant/resumes/view?resume=af263aa3ff03948a760039ed1f4c7a6c464945/",
            url = urlResume,
            headers={"user-agent":ua.random}
        )
        if res.status_code != 200:
            return None
        return res.content
    def extract_info(soup, heade, clas):
        info = soup.find_all(heade, class_=clas)
        if len(info) == 0:
            return None
        
        return info[0].string
    def get_resume_info(urlResume):
        resume = HHresume.get_resume_soap(urlResume)
        if resume is not None:
            soup = BeautifulSoup(resume, "lxml")

            # llNews0 = soup.findAll('div')
            # llNews1 = soup.find_all("div", class_="resume-header-name")
            # llNews2 = soup.find_all("h2", class_="bloko-header-1")
            llNews2 = soup.find_all("h2", class_="bloko-header-2")
            llNews3 = soup.find_all("div", class_="resume-block__title-text-wrapper")

            userName = HHresume.extract_info(soup, "h2", "bloko-header-1")
            userPos = HHresume.extract_info(soup, "h2", "bloko-header-2")
            return (userName, userPos)
        return None
    def get_links(text):
        ua =fake_useragent.UserAgent()
        res = requests.get(
            # url=f"https://hh.ru/search/resume?text=Python&area=1&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&hhtmFrom=vacancy_search_list",
            
            # url = f"https://spb.hh.ru/resume/f385aa2e0001f248590039ed1f366659697166?query=python&hhtmFrom=resume_search_result",
            url = f"https://spb.hh.ru/applicant/resumes/view?resume=af263aa3ff03948a760039ed1f4c7a6c464945",
            
            # url=f"https://hh.ru/search/resume?relocation=living_or_relocation&gender=unknown&text={text}&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&search_period=0",
            headers={"user-agent":ua.random}
        )
        if res.status_code != 200:
            return
        soup = BeautifulSoup(res.content, "lxml")
        # llNews0 = soup.findAll('div', class_='resume-header-name')
        # llNews1 = soup.find('span', class_='a11y-fast-nav')
        llNews0 = soup.findAll('div')
        # llNews1 = soup.find('div', class ='a11y-fast-nav')
        llNews1 = soup.find_all("div", class_="resume-header-name")
        
        llNews2 = soup.find_all("h2", class_="bloko-header-1")
        return
        # for string in soup.strings:
            # print(repr(string))
        try:
            page_count = int(soup.find("div",attrs={"class":"pager"}).find_all("span",recursive=False)[-1].find("a").find("span").text)
        except:
            return
        data = []
        for page in range(page_count):
        # for page in range(3):
            try:
                res = requests.get(
                    url=f"https://hh.ru/search/resume?relocation=living_or_relocation&gender=unknown&text={text}&isDefaultArea=true&exp_period=all_time&logic=normal&pos=full_text&fromSearchLine=false&search_period=0&page={page}",
                    headers={"user-agent":ua.random}
                )
                if res.status_code == 200:
                    soup = BeautifulSoup(res.content, "lxml")
                    for a in soup.find_all("a", attrs={"class": "serp-item"}):
                    # for a in soup.find_all("a", attrs={"class": "serp-item__name"}):
                    # for a in soup.find_all("a",attrs={"class":"resume-search-item__name"}):
                        urlUser = f'https://hh.ru{a.attrs["href"].split("?")[0]}'
                        data.append(urlUser)
                        # yield f'https://hh.ru{a.attrs["href"].split("?")[0]}'
            except Exception as e:
                print(f"{e}")
            time.sleep(1)
        print(page_count)
        return data

    def get_resume(link):
        ua =fake_useragent.UserAgent()
        data = requests.get(
            url=link,
            headers={"user-agent":ua.random}
        )
        if data.status_code != 200:
            return
        soup = BeautifulSoup(data.content, "lxml")
        try:
            name = soup.find(attrs={"class":"resume-block__title-text"}).text
        except:
            name = ""
        try:
            salary = soup.find(attrs={"class":"resume-block__title-text_salary"}).text.replace("\u2009","").replace("\xa0"," ")
        except:
            salary = ""
        try:
            tags = [tag.text for tag in soup.find(attrs={"class":"bloko-tag-list"}).find_all("span",attrs={"class":"bloko-tag__section_text"})]
        except:
            tags = []
        resume = {
            "name":name,
            "salary":salary,
            "tags":tags,
        }
        return resume

    def download_data(tag, filename):
        data = []
        for a in HHresume.get_links(tag):
            data.append(HHresume.get_resume(a))
            time.sleep(1)
            with open(filename,"w",encoding="utf-8")as f:
                json.dump(data,f,indent = 4, ensure_ascii=False)

    def read_data(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    def get_skills(data, freq):
        skills = {}
        dataCount = 0
        for d in data:
            if not d:
                continue
            dataCount += 1
            for tag in d.get("tags", []):
                skills[tag] = skills.get(tag, 0) + 1
        
        skills = {k: v / dataCount for k, v in skills.items() if v / dataCount >= freq}
        skills_sorted = sorted(skills, key=lambda x: skills[x], reverse=True)
        return {skill: skills[skill] for skill in skills_sorted}
        
    def proceessResume(urlResume):
        user = HHresume.get_resume_info(urlResume)
        # py = HHresume.get_links(urlResume)
        return user
        '''
        data = []
        for a in HHresume.get_links("python"):
            res = HHresume.get_resume(a)
            data.append(res)
            time.sleep(1)
        return
        '''
        '''
        st_accept = "text/html" # говорим веб-серверу, 
        # что хотим получить html
        # имитируем подключение через браузер Mozilla на macOS
        st_useragent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15"
        # формируем хеш заголовков
        headers = {
            "Accept": st_accept,
            "User-Agent": st_useragent
        }

        
        req = requests.get("https://selectel.ru/blog/courses/", headers)
        # считываем текст HTML-документа
        src = req.text

        # uplResume = "https://habr.com/ru/companies/selectel/articles/754674/"
        req1 = requests.get(uplResume, headers)
        src1 = req1.text
        
        # response = requests.get("https://zenrows.com") 
        response = requests.get(uplResume) 
        soup = BeautifulSoup(response.content, 'html.parser') 
        src2 = soup.title.string

        with open("spb.hh.ru") as fp: 
            soup = BeautifulSoup(fp, "html.parser") 
        return
        '''