from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render

from .forms import FilePathForm



# @login_required
def passport_update(request):
    
    if request.method == 'POST':
        form = FilePathForm(request.POST)
        if form.is_valid():
            return render(request, 'passport_update.html', {'form': form})

    else:
        form = FilePathForm()

    return render(request, 'passport_update.html', {'form': form})

