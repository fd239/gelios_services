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
    newfilepath = filepath[:-4]  # assuming the filepath ends with .bz2
    open(newfilepath, 'wb').write(data)
    # load_passporsts(newfilepath)
    # newfilepath = r'D:\list_of_expired_passports.csv'
    # dtypes = {'PASSP_SERIES': S4,
    #           'PASSP_NUMBER': numpy.int64}

    # dp = pd.read_csv(newfilepath, dtype={
    #                  0: 'S4', 1: 'S6'}, encoding='utf-8') -- рабочая строчка

    df = pd.read_csv(newfilepath, dtype={0: 'S4', 1: 'S6'}, encoding='utf-8')
    df.insert(0, 'id', range(0, len(df)))
    # df['id'] = df['PASSP_SERIES'][0] + df['PASSP_NUMBER'][0]
    # df['id'] = df.apply(lambda row: create_id(row), axis=1)
    # df.apply(pd.to_numeric, errors='coerce')

    # dp.infer_objects()
    # pd.to_numeric(dp, errors='coerce')
    # dtype={0: 's4', 1: 'int64'}, skiprows=[0]
    df.to_sql('passport_check_passport', sqliteConnection,
              if_exists='replace', index=False, chunksize=70000)

    createSecondaryIndex = 'CREATE INDEX num_serries_index ON parts (PASSP_SERIES, PASSP_NUMBER)'
    sqliteCursor = sqliteConnection.cursor()
    sqliteCursor.execute(createSecondaryIndex)


def create_id(row):
    return f'{row.PASSP_NUMBER}{row.PASSP_SERIES}'


def load_passporsts(file_path):

    Passport.objects.all().delete()

    with open(file_path) as file:
        reader = csv.reader(file)
        for row in reader:
            NewPassport = Passport.objects.create(series=row[0], number=row[1])
            NewPassport.save()
