import os
import shutil
import time

from django.http.response import HttpResponse
from django.shortcuts import render

from .forms import NpmDetailForm
from .iputil import get_ip
from .npmpackageinfo import getnpmpackagedependencies, getpackagetarball
from .npmpackageinfo import package_list, packagec_list
from .ziputil import zipDir


def npminfo(request):
    package_list.clear()
    packagec_list.clear()
    dir_name = 'download/' + get_ip(request)
    if os.path.exists(dir_name+".zip"):
        os.remove(dir_name + ".zip")
    if not os.path.exists("download/"):
        os.mkdir("download")
    if not os.path.exists("download/"+get_ip(request)):
        os.mkdir("download/"+get_ip(request))
    else:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.mkdir("download/" + get_ip(request))
    if request.method == 'POST':
        form = NpmDetailForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            version = form.cleaned_data['version']
            type = form.cleaned_data['type']
            print("Download started : %s" % time.ctime())
            getpackagetarball(name, version, request)
            getnpmpackagedependencies(name, version, request)
            print("Download finished : %s" % time.ctime())
            zipDir(dir_name)
            package_list.clear()
            packagec_list.clear()
            response = HttpResponse(open("download/" + get_ip(request) + ".zip", 'rb'), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=NpmPackage.zip'
            if os.path.exists(dir_name + ".zip"):
                os.remove(dir_name + ".zip")
            if os.path.exists(dir_name):
                shutil.rmtree(dir_name)
            return response
    form = NpmDetailForm()
    return render(request, 'form.html', {'form': form})
