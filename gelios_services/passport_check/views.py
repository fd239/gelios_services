from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render

from .forms import FilePathForm
from .models import Passport

import csv
import os
import urllib2
import bz2

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

    # TODO переделать здесь всё
    passport_file = urllib2.urlopen(PASSPORT_LIST_URL)
    with open('passport_file.csv', 'wb') as output:
        output.write(mp3file.read())

    with bz2.open("myfile.bz2", "wb") as f:
        load_passporsts(f)


def load_passporsts(file_path):

    Passport.objects.all().delete()

    with open(file_path) as f:
        reader = csv.reader(f)
        for row in reader:
            NewPassport = Passport.objects.create(series=row[0], number=row[1])
            NewPassport.save()
