from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render

from .forms import FilePathForm

def passport_update(request, path):
    
    if request.method == 'POST':

        form = PostForm(request.POST)

        post = form.save(commit=False)
        post.author = request.user
        post.save()

        return redirect(reverse('post_view', kwargs={
            'username': username, 'post_id': post_id}))

    content = {
        'form': form,
        'post': user_post,
    }

    return render(request, 'new_post.html', content)

