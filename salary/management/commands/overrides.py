from django.core.management.base import BaseCommand
from salary.models import DirectoryRecord, Department


class Command(BaseCommand):
    help = "Manual overrides for department classifications"

    def handle(self, *args, **options):
        # James Demmel
        eecs = Department.objects.get(
            canonical='Electrical Engineering and Computer Science')
        DirectoryRecord.objects.filter(uid='8385').update(department_obj=eecs)

        # Mark Richards
        eps = Department.objects.get(canonical='Earth and Planetary Science')
        DirectoryRecord.objects.filter(uid='7517').update(department_obj=eps)

        # Deborah Nolan
        stats = Department.objects.get(canonical='Statistics')
        DirectoryRecord.objects.filter(uid='5474').update(department_obj=stats)

        # Bruce Baldwin
        biology = Department.objects.get(canonical='Biology')
        DirectoryRecord.objects.filter(
            uid='18020').update(department_obj=biology)

        # Stuart Bale
        physics = Department.objects.get(canonical='Physics')
        DirectoryRecord.objects.filter(
            uid='83763').update(department_obj=physics)

        # Gibor Basri
        astronomy = Department.objects.get(canonical='Astronomy')
        DirectoryRecord.objects.filter(
            uid='282').update(department_obj=astronomy)

        # David Tse
        DirectoryRecord.objects.get(searched_name='DAVID TSE').delete()
