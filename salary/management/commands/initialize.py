from django.core.management import call_command
from django.core.management.base import BaseCommand
from salary.models import Person, DirectoryRecord, SalaryRecord, Department


class Command(BaseCommand):
    help = "Populate the database with salary, directory, \
    and department information"

    def handle(self, *args, **options):
        SalaryRecord.objects.all().delete()
        DirectoryRecord.objects.all().delete()
        Person.objects.all().delete()
        Department.objects.all().delete()

        call_command('mergerawfiles')
        call_command('filterberkeleyfaculty')
        call_command('importsalaryrecords')
        call_command('collapsepeople')
        call_command('importdirectoryrecords')
        call_command('processdepartments')
        call_command('overrides')
