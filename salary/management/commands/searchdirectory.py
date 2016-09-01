import bs4
import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from salary.models import Person, DirectoryRecord


class Command(BaseCommand):
    help = "Search online Berkeley directory for department affiliations"

    def search(self, first, last):
        """
        Queries Berkeley directory and returns person information or None.
        """
        url = 'http://www.berkeley.edu/directory/results?search-type=lastfirst&search-base=staff&search-term={}+{}'.format(last, first)
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.text)
        search_results = soup.find(class_='search-results')
        try:
            results = self.process_page(search_results)
            results['success'] = True
            print('Success!')
        except:
            results = {}
            results['success'] = False
            print('No results found')
            
        results['searched_name'] = '{} {}'.format(first, last)
        return results

    def process_page(self, search_results):
        """
        Takes BeautifulSoup markup and returns a dict of processed information.
        """
        fieldnames = ['uid','title','department','home_department']

        # If there is a result
        results = {field: '' for field in fieldnames}
        # Name in directory
        results['directory_name'] = search_results.h2.text

        for field in search_results.find_all('p'):
            contents =  field.contents
            label =  contents[0].text.lower().replace(' ','_')

            # Skip labels we don't care about
            if label not in fieldnames:
                continue
            else:
                value = contents[2]

            if type(value) is bs4.element.Tag:
                value = value.text

            results[label] = value

        return results

    def handle(self, *args, **options):
        for person in Person.objects.filter(directory_record=None).filter(search_attempt=False):
            print(person)
            if person.latest_record.year != '2015':
                continue
            person.search_attempt = True
            results = self.search(person.first, person.last)
            if results:
                print(results)
                record = DirectoryRecord(**results)
                record.save()
                person.directory_record = record
            person.save()
