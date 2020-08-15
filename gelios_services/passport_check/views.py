from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render

from .forms import FilePathForm
from .models import Passport

import csv
import os
import bz2
import urllib
import sqlite3
import pandas as pd
from pandas import DataFrame
import numpy

PASSPORT_LIST_URL = 'http://guvm.mvd.ru/upload/expired-passports/list_of_expired_passports.csv.bz2'


def passport_manual_update(request):

    if request.method == 'POST':
        form = FilePathForm(request.POST)
        if form.is_valid():
            load_passporsts(form.cleaned_data['file_path'])
            return render(request, 'passport_update.html', {'form': form, 'updated': True})
    else:
        form = FilePathForm()

    return render(request, 'passport_update.html', {'form': form, 'updated': False})


def passport_auto_update(request):

    sqliteConnection = sqlite3.connect(settings.DATABASES['default']['NAME'])
    result = urllib.request.urlretrieve(
        PASSPORT_LIST_URL, 'list_of_expired_passports.bz2')

    filepath = result[0]
    zipfile = bz2.BZ2File(filepath)
    data = zipfile.read()
    newfilepath = filepath[:-4]
    open(newfilepath, 'wb').write(data)

    try:
        df = pd.read_csv(newfilepath, dtype={
                         0: 'S4', 1: 'S6'}, encoding='utf-8')
    except IOError as e:
        return HttpResponse(f'<html><body>{e}</body></html>')

    try:
        df.insert(0, 'id', range(0, len(df)))
    except IOError as e:
        return HttpResponse(f'<html><body>{e}</body></html>')

    try:
        df.to_sql('passport_check_passport', sqliteConnection,
                  if_exists='replace', index=False)
    except IOError as e:
        return HttpResponse(f'<html><body>{e}</body></html>')

    # createSecondaryIndex = 'CREATE INDEX num_serries_index ON parts (PASSP_SERIES, PASSP_NUMBER)'
    # sqliteCursor = sqliteConnection.cursor()
    # sqliteCursor.execute(createSecondaryIndex)

    return HttpResponse('<html><body>Done.</body></html>')


def create_id(row):
    return f'{row.PASSP_NUMBER}{row.PASSP_SERIES}'


def load_passporsts(file_path):

    Passport.objects.all().delete()

    with open(file_path) as file:
        reader = csv.reader(file)
        for row in reader:
            NewPassport = Passport.objects.create(series=row[0], number=row[1])
            NewPassport.save()
