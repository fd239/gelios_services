from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .forms import FilePathForm
from .models import Passport

import bz2
import csv
import pandas as pd
import sqlite3
import urllib
import numpy as np

from datetime import datetime


PASSPORT_LIST_URL = 'http://guvm.mvd.ru/upload/expired-passports/list_of_expired_passports.csv.bz2'
LOCAL_FILE_PATH = r'D:\\gitDev\\gelios_services\\gelios_services\\list_of_expired_passports'


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

    start_time = datetime.now()

    sqliteConnection = sqlite3.connect(
        settings.DATABASES['default']['NAME'])

    sqliteCursor = sqliteConnection.cursor()
    sqliteCursor.execute('DELETE FROM passport_check_passport')
    sqliteCursor.execute('DROP INDEX IF EXISTS num_serries_index')

    request_result = urllib.request.urlretrieve(
        PASSPORT_LIST_URL, 'list_of_expired_passports.bz2')

    filepath = request_result[0]
    zipfile = bz2.BZ2File(filepath)
    data = zipfile.read()
    newfilepath = filepath[:-4]
    open(newfilepath, 'wb').write(data)

    last_id = 0

    for chunk in pd.read_csv(newfilepath, dtype={0: 'S4', 1: 'S6'}, chunksize=25_000_000):

        chunk.insert(0, 'id', range(last_id, last_id + len(chunk)))
        last_id += len(chunk)

        str_df = chunk.select_dtypes([np.object])
        str_df = str_df.stack().str.decode('latin1').unstack()

        for col in str_df:
            chunk[col] = str_df[col]

        chunk.to_sql('passport_check_passport', sqliteConnection,
                     if_exists='append', index=False)

    createSecondaryIndex = 'CREATE INDEX num_serries_index ON passport_check_passport(PASSP_SERIES, PASSP_NUMBER)'
    sqliteCursor.execute(createSecondaryIndex)

    return HttpResponse(f'<html><body>Done. Total time = [{datetime.now() - start_time}]</body></html>')


def load_passporsts(file_path):

    Passport.objects.all().delete()

    with open(file_path) as file:
        reader = csv.reader(file)
        for row in reader:
            NewPassport = Passport.objects.create(
                series=row[0], number=row[1])
            NewPassport.save()
