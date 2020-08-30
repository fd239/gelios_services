from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

from .forms import FilePathForm
from .models import Passport

import bz2
import csv
import numpy as np
import os
import pandas as pd
from sqlalchemy import create_engine
from urllib.request import urlopen
from datetime import datetime


PASSPORT_LIST_URL = 'http://guvm.mvd.ru/upload/expired-passports/list_of_expired_passports.csv.bz2'
LOCAL_FILE_PATH = r'D:\\gitDev\\gelios_services\\list_of_expired_passports'


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
    db_name = settings.DATABASES['default']['NAME']
    connection_str = f'postgresql://{settings.DATABASE_USER}:' \
        f'{settings.DATABASE_PASSWORD}@localhost/{db_name}'
    eng = create_engine(connection_str)
    con = eng.connect()

    con.execute('DELETE FROM passport_check_passport')
    con.execute('DROP INDEX IF EXISTS num_series_idx')

    with urlopen(PASSPORT_LIST_URL) as in_stream, bz2.BZ2File(in_stream) as zipfile:
        data = zipfile.read()
        newfilepath = 'list_of_expired_passports.csv'

        with open(newfilepath, 'wb') as f:
            f.write(data)
            last_id = 0
            colnames = ['series', 'number']

            # TODO: не забыть вернуть chunksize=25_000_000
            for chunk in pd.read_csv(newfilepath, dtype={0: 'S4', 1: 'S6'}, nrows=25, chunksize=5, names=colnames, header=0):

                chunk.insert(0, 'id', range(last_id, last_id + len(chunk)))
                last_id += len(chunk)

                str_df = chunk.select_dtypes([np.object])
                str_df = str_df.stack().str.decode('latin1').unstack()

                for col in str_df:
                    chunk[col] = str_df[col]

                chunk.to_sql('passport_check_passport', con,
                             if_exists='append', index=False)

    create_indexes = 'CREATE UNIQUE INDEX num_series_idx ON passport_check_passport (series, number)'
    con.execute(create_indexes)

    os.remove(newfilepath)

    return HttpResponse(f'<html><body>Done. Total time = [{datetime.now() - start_time}]</body></html>')


def load_passporsts(file_path):

    Passport.objects.all().delete()

    with open(file_path) as file:
        reader = csv.reader(file)
        for row in reader:
            NewPassport = Passport.objects.create(
                series=row[0], number=row[1])
            NewPassport.save()
