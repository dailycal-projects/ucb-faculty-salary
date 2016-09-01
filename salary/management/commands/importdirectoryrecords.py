import os
import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from salary.models import Person, DirectoryRecord


class Command(BaseCommand):
    help = "Import Berkeley directory for department affiliations"

    def build_cache(self):
        """
        Returns dict with {searched_name: row}
        """
        cache = {}
        cache_path = os.path.join(settings.DATA_DIR, 'directory.csv')
        with open(cache_path, 'r') as cache_file:
            reader = csv.DictReader(cache_file)
            for row in reader:
                cache[row['searched_name']] = row
        return cache

    def handle(self, *args, **options):
        cache = self.build_cache()
        for person in Person.objects.filter(directory_record=None):
            print(person)
            results = cache.get('{} {}'.format(person.first, person.last), None)
            if results:
                record = DirectoryRecord(**results)
                record.save()
                person.directory_record = record
                person.save()
