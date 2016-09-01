from django.core.management.base import BaseCommand
from salary.models import SalaryRecord, Person, DirectoryRecord


class Command(BaseCommand):
    help = "Populate a model with an instance for each unique person"

    def handle(self, *args, **options):
        DirectoryRecord.objects.all().delete()
        Person.objects.all().delete()
        names = set(SalaryRecord.objects.values_list('first','last'))
        total = len(names)
        counter = 0
        for first, last in names:
            counter += 1
            print('{}/{}: {}, {}'.format(counter, total, last, first))
            records = SalaryRecord.objects.filter(first=first, last=last)
            person = Person(
                first = first,
                last = last,
            )
            person.save()
            records.update(person=person)