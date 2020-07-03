import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from django.db import IntegrityError

from .models import MProject
from .models import MBids
from scrap.CCandidate import CCandidate


class CProject():
    base_url = 'https://www.freelancer.com/projects/'

    def __init__(self, driver, project_url):
        self.driver = driver
        self.url = project_url
        self.soup = None
        self.description = None
        self.skills = None
        self.visited = False
        self.mproject = None


        if MProject.objects.filter(url=project_url).exists():
            project_model = MProject.objects.filter(url=project_url).first()
            self.url = project_model.url
            self.description = project_model.description
            self.skills = project_model.skills
            self.visited = project_model.visited
            self.mproject = project_model


    def visit(self):
        if self.visited:
            return 0, 0, 0
        print('Visiting Project : "{}"'.format(self.url))

        self.driver.get(self.url)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        freelancers = self.soup.find_all('div', {'class': 'FreelancerInfo'})

        isFirst = True
        nbids_added = 0
        nusers_added = 0
        nbids_errors = 0

        for f in freelancers:
            if isFirst:
                status = 1
                isFirst = False
            else:
                status = 0
            cname = f.find('a', {'class': 'FreelancerInfo-username'})['href'][3:]
            cdesc = f.find('p', {'class': 'FreelancerInfo-about'})['data-descr-full']

            cprice = float(f.find('div', {'class': 'FreelancerInfo-price'}).getText().split(' ')[0][1:])
            ccurrency = f.find('div', {'class': 'FreelancerInfo-price'}).getText().split(' ')[1]
            try:
                cdays = int(f.find('div', {'class': 'FreelancerInfo-price'}).getText().split(' ')[3])
            except:
                cdays = None

            newc = CCandidate(name=cname, driver=self.driver)
            if newc.exists():
                newc.set_mcandidate()
            else:
                nusers_added += newc.scrap()

            try:
                bid = MBids(
                    bider=newc.mcandidate,
                    project=self.mproject,
                    description=cdesc,
                    price=cprice,
                    currency=ccurrency,
                    ndays=cdays,
                    status=status
                )
                bid.save()
                nbids_added += 1

            except IntegrityError:
                print('bid on "{}" from "{}" could not be added'.format(self.url, cname))
                nbids_errors += 1

        self.visited = True
        self.mproject.visited = True
        self.mproject.save()
        return nbids_added, nbids_errors, nusers_added




    def scrap(self):
        print('Scraping Project :"{}"'.format(self.url))

        self.driver.get(self.url)
        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        self.description = self.get_description()
        self.skills = self.get_skills()
        return self.save()

    def get_description(self):
        details = self.soup.find('div', {'class': 'PageProjectViewLogout-detail'}).find_all('p')
        description = ''
        for r in details[1:]:
            if r.get('class') != None:
                if r['class'][0] == 'PageProjectViewLogout-detail-tags':
                    break
            description += r.getText()
        return description

    def get_skills(self):
        skills = []
        skill_links = self.soup.find_all('a', {'class': 'PageProjectViewLogout-detail-tags-link--highlight'})
        for s in skill_links:
            skills.append(s.getText())
        return ';'.join(skills)

    def save(self):
        try:
            defaults = {
                'description': self.description,
                'skills': self.skills
            }
            p, created = MProject.objects.update_or_create(
                url=self.url,
                defaults=defaults
            )
            self.mproject = p
            self.mproject.save()
            return 1
        except:
            return 0
