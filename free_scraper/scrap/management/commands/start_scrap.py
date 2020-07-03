from django.core.management.base import BaseCommand, CommandError
import selenium as se
import os
import sys
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrap.CCandidate import CCandidate
from scrap.CProject import CProject
from scrap.models import MProject
from scrap.models import MCandidate


class Command(BaseCommand):

    def visit_projects(self, driver):
        c = 0
        consecutive_err = 0
        nbids_tot, nbids_err_tot, nusers_tot = 0, 0, 0
        while MProject.objects.filter(visited=0).exists():
            try:
                mproject = MProject.objects.filter(visited=0).first()
                project = CProject(driver=driver, project_url=mproject.url)
                project.scrap()
                nbids, nbids_err, nusers = project.visit()
                nbids_tot += nbids
                nbids_err_tot += nbids_err
                nusers_tot += nusers
                c += 1
                consecutive_err = 0
            except Exception as e:
                consecutive_err += 1
                if consecutive_err >= 50:
                    sys.exit('{} BREAK : 5 users scrapings failed'.format(datetime.now()))
                mproject.delete()
                self.stdout.write(self.style.ERROR(str(e)) )

        self.stdout.write(self.style.SUCCESS(
            '{} Projects visited : {} user added, {} bids, {} bids err'.format(str(c), str(nusers_tot), str(nbids_tot), str(nbids_err_tot)))
        )

    def visit_users(self, driver):
        c = 0
        while MCandidate.objects.filter(visited=0).exists() and c < 10:
            try:
                mcandidate = MCandidate.objects.filter(visited=0).first()
                candidate = CCandidate(driver=driver, name=mcandidate.name)
                candidate.visit()
                c += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e)) )
        self.stdout.write(self.style.SUCCESS('{} Users visited'.format(str(c))))



    def handle(self, *args, **kwargs):
        # Using Chrome
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = se.webdriver.Chrome(options=options, executable_path='{}/chromedriver'.format(os.getcwd()))
        c = 0
        while MCandidate.objects.filter(visited=0).exists() or MProject.objects.filter(visited=0).exists() :
            self.visit_projects(driver)
            self.visit_users(driver)
            c += 1
            self.stdout.write(self.style.SUCCESS('{} Iteration made'.format(str(c))))

        self.stdout.write(self.style.SUCCESS('No more User or Projects to visit'))
        # name = kwargs['name']
