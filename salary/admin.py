from django.contrib import admin
from salary.models import Person, SalaryRecord

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    pass
