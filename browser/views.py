import os
from django.shortcuts import render
from django.utils.text import slugify
from bakery.views import BuildableListView, BuildableDetailView
from salary.models import Person, Department, SalaryRecord, DirectoryRecord
from django.db.models import Avg


class SalaryRecordListView(BuildableListView):
    """
    The landing page, with a full list of people.
    """
    model = SalaryRecord
    template_name = "browser/home.html"
    build_path = 'index.html'

    def get_queryset(self):
        return self.model.objects.filter(year='2015').exclude(person__directory_record__department_obj=None)


class PersonDetailView(BuildableDetailView):
    """
    All salary and department information for an individual person.
    """
    model = Person
    template_name = "browser/person_detail.html"


class DepartmentListView(BuildableListView):
    """
    List of departments with salary by position.
    """
    model = Department
    template_name = "browser/department_list.html"
    build_path = 'departments/index.html'

    def get_context_data(self, **kwargs):
        context = super(DepartmentListView, self).get_context_data(**kwargs)
        return context


class DepartmentDetailView(BuildableDetailView):
    """
    Average salary by position, and a full list of people for a department.
    """
    model = Department
    template_name = "browser/department_detail.html"

    def get_context_data(self, **kwargs):
        context = super(DepartmentDetailView, self).get_context_data(**kwargs)
        context['by_title_category'] = SalaryRecord.objects.filter(year=2015).filter(person__directory_record__department_obj=self.object).values('title_category').annotate(Avg('gross')).order_by('gross__avg').reverse()
        for d in context['by_title_category']:
            d['all__avg'] = SalaryRecord.objects.filter(year=2015).filter(title_category=d['title_category']).aggregate(Avg('gross'))['gross__avg']

        context['by_year'] = []
        for year in range(2006, 2016):
            year = str(year)
            avg = SalaryRecord.objects.filter(year=year).filter(person__directory_record__department_obj=self.object).aggregate(Avg('gross'))['gross__avg']
            berkeley_avg = SalaryRecord.objects.filter(year=year).aggregate(Avg('gross'))['gross__avg']
            context['by_year'].append({
                'year': year,
                'avg': avg,
                'berkeley_avg': berkeley_avg
            }) 

        return context
