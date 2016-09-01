import os
import csv
from django.conf import settings
from postgres_copy import CopyMapping
from django.core.management.base import BaseCommand
from salary.models import SalaryRecord

class Command(BaseCommand):
    help = "Merge, filter, and clean salary records from 2006 to 2015"

    def build_titles(self):
        titles = {}
        titles_file_path = os.path.join(settings.DATA_DIR, 'titles.csv')
        with open(titles_file_path, 'r') as titles_file:
            reader = csv.DictReader(titles_file)
            for row in reader:
                if row['keep'] == '1':
                    titles[row['db_title']] = row
        return titles

    def get_fieldnames(self):
        return ['year','location','first','middle','last','name','title','title_category','title_qualifier','title_year_code','gross','regular','overtime','other','base','eff_date']

    def clean_field(self, field):
        return field.replace('$','').replace(',','').strip().upper()

    def clean_row(self, row):
        return dict([(k,self.clean_field(v)) for k,v in row.items() if k in self.get_fieldnames()])

    def handle(self, *args, **options):
        titles_dictionary = self.build_titles()
        clean_file_path = os.path.join(settings.DATA_DIR, 'clean.csv')
        with open(clean_file_path, 'w') as clean_file:
            writer = csv.DictWriter(clean_file, fieldnames=self.get_fieldnames())
            writer.writeheader()

            for year in range(2006,2016):
                print('Processing {}'.format(year))
                raw_file_path = os.path.join(settings.DATA_DIR, 'salary_{}.csv'.format(year))
                with open(raw_file_path, 'r') as raw_file:
                    reader = csv.DictReader(raw_file)
                    for row in reader:
                        # Only Berkeley records
                        if 'BERKELEY' not in row['location'].upper():
                            continue

                        # First name and last name are distinct fields for 2013 onwards
                        if year > 2012:
                            # Don't care about starred names 
                            if '*' in row['last']:
                                continue
                        else:
                            # Don't care about starred names 
                            if '*' in row['name'] or '---' in row['name']:
                                continue
                            names = row['name'].split(',')
                            row['last'] = names[0]
                            row['first'] = ' '.join(names[1:])

                        # Only positions we care about
                        category = titles_dictionary.get(row['title'], None)
                        if category:
                            row['title_category'] = category['type']
                            row['title_qualifier'] = category['qualifier']
                            row['title_year_code'] = category['year_code']
                        else:
                            continue

                        row['location'] = 'BERKELEY'
                        row['year'] = str(year)

                        row = self.clean_row(row)

                        # Attempt to deal with middle names
                        first_names = [name.replace('.','') for name in row['first'].split(' ')]
                        if len(first_names) > 1:
                            row['first'] = first_names[0]
                            row['middle'] = ' '.join(first_names[1:])

                        row['name'] = '{}, {}'.format(row['last'], row['first'])

                        writer.writerow(row)
