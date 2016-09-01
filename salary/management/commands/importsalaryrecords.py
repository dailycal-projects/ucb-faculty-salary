import os
import csv
from django.conf import settings
from postgres_copy import CopyMapping
from django.core.management.base import BaseCommand
from salary.models import SalaryRecord


class Command(BaseCommand):
    help = "Import clean salary records into the database"

    def handle(self, *args, **options):
        SalaryRecord.objects.all().delete()
        clean_file_path = os.path.join(settings.DATA_DIR, 'clean.csv')

        fields = [field.name for field in SalaryRecord._meta.get_fields() if field.name != 'id']
        mapping = {field: field for field in fields}

        c = CopyMapping(
            SalaryRecord,
            clean_file_path,
            mapping
        )
        c.save()
