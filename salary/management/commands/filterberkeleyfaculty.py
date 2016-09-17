import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Filter salary records to only Berkeley faculty"

    def build_titles(self):
        """
        Takes a CSV of titles that determines whether they correspond
        to a faculty position that we're interested in analyzing.
        """
        titles = {}
        titles_file_path = os.path.join(
            settings.DATA_DIR, 'directory', 'titles.csv')
        with open(titles_file_path, 'r') as titles_file:
            reader = csv.DictReader(titles_file)
            for row in reader:
                if row['keep'] == '1':
                    titles[row['db_title']] = row
        return titles

    def get_fieldnames(self):
        return ['year', 'location', 'first', 'middle', 'last', 'name',
                'title', 'title_category', 'title_qualifier',
                'title_year_code', 'gross', 'regular', 'overtime',
                'other', 'base', 'eff_date']

    def handle(self, *args, **options):
        titles_dictionary = self.build_titles()
        clean_file_path = os.path.join(
            settings.DATA_DIR, 'berkeley_faculty.csv')
        with open(clean_file_path, 'w') as clean_file:
            writer = csv.DictWriter(
                clean_file, fieldnames=self.get_fieldnames())
            writer.writeheader()

            merged_file_path = os.path.join(settings.DATA_DIR, 'merged.csv')
            with open(merged_file_path, 'r') as raw_file:
                reader = csv.DictReader(raw_file)
                for row in reader:
                    # Only Berkeley records
                    if 'BERKELEY' not in row['location'].upper():
                        continue

                    # Only positions we care about
                    category = titles_dictionary.get(row['title'], None)
                    if category:
                        row['title_category'] = category['type']
                        row['title_qualifier'] = category['qualifier']
                        row['title_year_code'] = category['year_code']
                    else:
                        continue

                    writer.writerow(row)
