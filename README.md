The most complete, open-source database of UC Berkeley faculty salary data.

# What is this?

* `data`: A collection of CSVs with pay data for the University of California from 2006 to 2015. For 2010 to 2015, these are sourced from public records requests with the University of California. For 2006 to 2009, these are from Microsoft Access databases stored on CDs in the [UC Berkeley library](http://oskicat.berkeley.edu/record=b12681348~S1).
* `salary`: A Django app to load UC Berkeley faculty pay data and departmental information.
* `browser`: A Django app to browse UC Berkeley faculty salary information.

# How can I use this?

*Are you a journalist or a researcher who wants to use this data?*

Head to the [`data`](https://github.com/dailycal-projects/ucb-faculty-salary/tree/master/data) directory and download the raw CSVs with all UC employees, or the clean CSV with processed information for UC Berkeley faculty. If you have any questions, contact us at projects@dailycal.org. If you end up using the data, we'd love if you dropped us a line!

*Are you a programmer who wants to adapt our database to fit your own needs?*

First, get a Django project started.

Create a new virtualenv and clone the repository.
```
virtualenv ucb-faculty-salary
git clone https://github.com/dailycal-projects/ucb-faculty-salary.git
```
Install the requirements.
```
pip install -r requirements.txt
```
Create a Postgres database. For example, if you wanted to call it `salary`:
```
createdb salary
```
Set the following environment variables using `EXPORT VARIABLE = 'VALUE'`:
  * `DB_NAME`: name of the Postgres database
  * `DB_HOST`: name of the database host
  
Migrate the database.
```
python manage.py migrate
```

The data is processed with a series of Django management commands, which you can run with `python manage.py [command]`. They are, in the order they should be run:

*`mergerawfiles` Process and join the raw CSVs in `data/salary`, creating a merged, cleaned CSV at `data/merged.csv`. This file includes information for every UC campus. It's big — about 180 MB.
* `filterberkeleyfaculty`:  Filters for UC Berkeley faculty. Here's where you could, for example, include other campuses or administrative positions. Creates `data/berkeley_faculty.csv`.
* `importsalaryrecords`: Uses `django-postgres-copy` to import the clean Berkeley faculty CSV into a Postgres database.
* `collapsepeople`: Looks for common names in the ten years of data and creates `Person` objects for each unique faculty member.
* `importdirectoryrecords`: Imports information from the UC Berkeley directory that associates people with department codes, and associates `People` with `DirectoryRecord` objects.
* `processdepartments`: Imports information associating department codes to canonical departments, and creates `Department` objects for `DirectoryRecord` objects, where applicable.
* `overrides`: Manually corrects for some errors, like professors who have left UC Berkeley or whose departments are incorrect.

Alternatively, run `python manage.py initialize` to bootstrap the project, which will call the above commands in succession.
