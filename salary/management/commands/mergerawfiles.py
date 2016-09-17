import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Merge and clean salary records from 2006 to 2015"

    def get_fieldnames(self):
        return ['year', 'location', 'first', 'middle', 'last', 'name', 'title',
                'gross', 'regular', 'overtime', 'other', 'base', 'eff_date']

    def clean_field(self, field):
        return field.replace('$', '').replace(',', '').strip().upper()

    def clean_row(self, row):
        return dict([(k, self.clean_field(v)) for k, v in row.items()
                     if k in self.get_fieldnames()])

    def handle(self, *args, **options):
        merged_file_path = os.path.join(settings.DATA_DIR, 'merged.csv')
        with open(merged_file_path, 'w') as merged_file:
            writer = csv.DictWriter(merged_file,
                                    fieldnames=self.get_fieldnames())
            writer.writeheader()

            for year in range(2006, 2016):
                print('Processing {}'.format(year))
                raw_file_path = os.path.join(settings.DATA_DIR,
                                             'salary',
                                             'salary_{}.csv'.format(year))
                with open(raw_file_path, 'r') as raw_file:
                    reader = csv.DictReader(raw_file)
                    for row in reader:
                        # First name and last name are distinct fields for
                        # 2013 onwards
                        if year > 2012:
                            # Don't want starred names
                            if '*' in row['last']:
                                continue
                        else:
                            # Don't want starred names
                            if '*' in row['name'] or '---' in row['name']:
                                continue
                            names = row['name'].split(',')
                            row['last'] = names[0]
                            row['first'] = ' '.join(names[1:])

                        row['year'] = str(year)
                        row = self.clean_row(row)

                        # Attempt to deal with middle names
                        first_names = [name.replace('.', '')
                                       for name in row['first'].split(' ')]
                        if len(first_names) > 1:
                            row['first'] = first_names[0]
                            row['middle'] = ' '.join(first_names[1:])

                        row['name'] = '{}, {}'.format(
                            row['last'],
                            row['first'])

                        writer.writerow(row)
