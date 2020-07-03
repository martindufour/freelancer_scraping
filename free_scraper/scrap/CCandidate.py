import selenium as se
from selenium import webdriver
from django.db import IntegrityError
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import time

from .models import MCandidate
from .models import MProject


class CCandidate():
    url = 'https://www.freelancer.com/u/'

    def __init__(self, driver, name):
        self.name = name
        self.url += name
        self.driver = driver
        self.driver.get(self.url)

        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        self.jobs_completed = None
        self.on_budget = None
        self.on_time = None
        self.repeat_hire_rate = None
        self.resume = None
        self.nstars = None
        self.nreviews = None
        self.mcandidate = None
        self.visited = False

        if MCandidate.objects.filter(name=name).exists():
            self.mcandidate = MCandidate.objects.filter(name=name).first()
            self.jobs_completed = self.mcandidate.jobs_completed
            self.on_budget = self.mcandidate.on_budget
            self.on_time = self.mcandidate.on_time
            self.repeat_hire_rate = self.mcandidate.repeat_hire_rate
            self.resume = self.mcandidate.description
            self.nstars = self.mcandidate.nstars
            self.nreviews = self.mcandidate.nreviews
            self.visited = self.mcandidate.visited



    def visit(self):
        print('Visiting User : "{}"'.format(self.url))
        if self.visited:
            return 0
        try:
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, 'ReviewItem'))
                WebDriverWait(self.driver, 5).until(element_present)
            except:
                self.visited = True
                self.mcandidate.visited = True
                self.mcandidate.save()
                return 0

            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            links = self.soup.find_all('a', {'class': 'LinkElement ng-star-inserted'})

            for l in links:
                if not l['href'].startswith('/projects/'):
                    continue
                MProject.objects.get_or_create(
                    url='https://www.freelancer.com' + l['href']
                )
            self.visited = True
            self.mcandidate.visited = True
            self.mcandidate.save()
            return 1
        except:
            return 0


    def exists(self):
        return MCandidate.objects.filter(name=self.name).exists()

    def set_mcandidate(self):
        self.mcandidate = MCandidate.objects.filter(name=self.name).first()

    def scrap(self):
        print('Scraping User :"{}"'.format(self.url))
        self.resume = self.get_resume()
        self.nstars = self.get_nstars()
        self.nreviews = self.get_nreviews()
        self.set_reputation_items()

        return self.save()

    def get_resume(self):
        try:
            element_present = EC.presence_of_element_located((By.CLASS_NAME, 'ReadMoreButton'))
            WebDriverWait(self.driver, 4).until(element_present)
            read_more_button = self.driver.find_element_by_class_name("ReadMoreButton")
            read_more_button.click()
        except (NoSuchElementException, AttributeError, TimeoutException):
            print('Scraping User : "{}" ReadMore Not clicked'.format(self.url))

        self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        resume = self.soup.find('app-user-profile-summary-description').find('div')
        return resume.getText()

    def get_nstars(self):
        nstars = self.soup.find('fl-bit', {'class': 'ValueText ng-star-inserted'})
        return float(nstars.getText())

    def get_nreviews(self):
        nreviews = self.soup.find('fl-bit', {'class': 'ReviewCount ng-star-inserted'})
        return int(nreviews.find('div').getText()[2:-9])

    def getNA_orVal(self, field):
        if 'N/A' in field:
            return None
        else :
            return float(field.strip()[:-1])  / 100

    def set_reputation_items(self):
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'ReputationItemLoading'))
        WebDriverWait(self.driver, 5).until_not(element_present)
        items = self.soup.find_all('app-user-profile-summary-reputation-item')

        for i in items:
            try:
                if i['label'] == 'Jobs Completed':
                    self.jobs_completed = self.getNA_orVal(i.find('div').getText())
                if i['label'] == 'On Budget':
                    self.on_budget = self.getNA_orVal(i.find('div').getText())
                if i['label'] == 'On Time':
                    self.on_time = self.getNA_orVal(i.find('div').getText())
                if i['label'] == 'Repeat Hire Rate':
                    self.repeat_hire_rate = self.getNA_orVal(i.find('div').getText())
            except KeyError:
                print('Error in finding reputation items')

    def save(self):
        defaults = {
            'nstars' : self.nstars,
            'nreviews' : self.nreviews,
            'jobs_completed' : self.jobs_completed,
            'on_budget' : self.on_budget,
            'on_time' : self.on_time,
            'repeat_hire_rate' : self.repeat_hire_rate,
            'description' : self.resume
        }

        try:
            self.mcandidate, created = MCandidate.objects.get_or_create(
                name=self.name,
                defaults=defaults
            )
            print('{} was added'.format(self.name))
            return 1
        except IntegrityError:
            print('{} could not be added'.format(self.name))
            return 0






