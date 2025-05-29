from django.shortcuts import render, redirect
from .forms import FileUploadForm
from .models import FileUpload, Task

def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_upload = form.save(commit=False)
            file_upload.uploaded_by = request.user
            file_upload.save()
            return redirect('dashboard')
    else:
        form = FileUploadForm()
    return render(request, 'tasks/upload.html', {'form': form})
