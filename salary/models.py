from django.db import models
from django.utils.text import slugify
from django.contrib.postgres.fields import ArrayField


class SalaryRecord(models.Model):
    """
    Individual salary record for one person in one year.
    """
    year = models.CharField(max_length=4)
    location = models.CharField(max_length=256, null=True)
    first = models.CharField(max_length=256, null=True)
    middle = models.CharField(max_length=256, null=True)
    last = models.CharField(max_length=256, null=True)
    name = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=True)
    title_category = models.CharField(max_length=256, null=True)
    title_qualifier = models.CharField(max_length=256, null=True)
    title_year_code = models.CharField(max_length=16, null=True)
    gross = models.DecimalField(null=True, decimal_places=2, max_digits=20)
    regular = models.DecimalField(null=True, decimal_places=2, max_digits=20)
    overtime = models.DecimalField(null=True, decimal_places=2, max_digits=20)
    other = models.DecimalField(null=True, decimal_places=2, max_digits=20)
    base = models.DecimalField(null=True, decimal_places=2, max_digits=20)
    eff_date = models.CharField(max_length=16, null=True)

    person = models.ForeignKey('Person', null=True)

    def __str__(self):
        return '{}: {}'.format(self.name, self.year)

    class Meta:
        ordering = ['-year']


class DirectoryRecord(models.Model):
    """
    Individual record from the online Berkeley directory. Possibly
    belongs to a Department.
    """
    searched_name = models.CharField(max_length=256, null=True)
    directory_name = models.CharField(max_length=256, null=True)
    title = models.CharField(max_length=256, null=True)
    department = models.CharField(max_length=256, null=True)
    home_department = models.CharField(max_length=256, null=True)
    uid = models.CharField(max_length=256, null=True)
    success = models.BooleanField(default=False)

    department_obj = models.ForeignKey('Department', null=True)

    def __str__(self):
        return self.searched_name

    class Meta:
        ordering = ['person__last']


class Department(models.Model):
    """
    An academic department, which contains DirectoryRecords
    and may have multiple codes.
    """
    codes = ArrayField(models.CharField(max_length=5), null=True)
    desc = models.CharField(max_length=256, null=True)
    canonical = models.CharField(max_length=256)
    discipline = models.CharField(max_length=256, null=True)
    slug = models.CharField(max_length=256, null=True)

    def get_absolute_url(self):
        return '/departments/{}/'.format(self.slug)

    @property
    def avg_salary_2015(self):
        return SalaryRecord.objects.filter(
            person__directory_record__department_obj=self).filter(year='2015').aggregate(models.Avg('gross'))['gross__avg']

    def avg_salary_by_category(self, category):
        return SalaryRecord.objects.filter(person__directory_record__department_obj=self).filter(title_category=category).filter(year='2015').aggregate(models.Avg('gross'))['gross__avg']

    @property
    def avg_salary_professor(self):
        return self.avg_salary_by_category('PROFESSOR')

    @property
    def avg_salary_associate_professor(self):
        return self.avg_salary_by_category('ASSOCIATE PROFESSOR')

    @property
    def avg_salary_assistant_professor(self):
        return self.avg_salary_by_category('ASSISTANT PROFESSOR')

    @property
    def avg_salary_lecturer(self):
        return self.avg_salary_by_category('LECTURER')

    def __str__(self):
        return self.canonical


class Person(models.Model):
    """
    A person with one or more SalaryRecords and possibly
    one DirectoryRecord.
    """
    first = models.CharField(max_length=256, null=True)
    last = models.CharField(max_length=256, null=True)
    slug = models.CharField(max_length=256, null=True)

    search_attempt = models.BooleanField(default=False)
    directory_record = models.OneToOneField('DirectoryRecord', null=True)

    @property
    def latest_record(self):
        return self.salaryrecord_set.first()

    def get_absolute_url(self):
        return '/person/{}/'.format(self.slug)

    def save(self, *args, **kwargs):
        self.slug = slugify('{} {}'.format(self.first, self.last))
        super(Person, self).save(*args, **kwargs)

    def __str__(self):
        return '{}, {}'.format(self.last, self.first)

    class Meta:
        ordering = ['last']
