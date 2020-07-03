from django.core.management.base import BaseCommand, CommandError
import selenium as se
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrap.CCandidate import CCandidate
from scrap.CProject import CProject


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('name', type=str)

    def handle(self, *args, **kwargs):
        options = se.webdriver.ChromeOptions()
        options.add_argument('headless')

        driver = se.webdriver.Chrome(options=options, executable_path='/Users/i538262/Downloads/chromedriver')

        name = kwargs['name']

        c = CCandidate(name=name, driver=driver)
        c.scrap()

        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"'))
