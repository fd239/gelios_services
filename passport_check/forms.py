from django import forms


class FilePathForm(forms.Form):
    file_path = forms.CharField(label='File path', max_length=500)
