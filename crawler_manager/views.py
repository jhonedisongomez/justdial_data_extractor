from __future__ import absolute_import, unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.admin.views.decorators import staff_member_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

from .tasks import start_srabbing
from django.contrib import messages


@staff_member_required
def home(request):
    if request.method == 'GET':
        return render(request, 'crawler_manager/crawler_page.html')
    if request.method == 'POST':
        
        city_name = request.POST.get('city_name')
        keyword = request.POST.get('keyword')
        numof_instance = request.POST.get('numof_instance')

        data = (city_name, keyword, numof_instance,)

        start_srabbing.delay(data)
        messages.success(request, 'We are scrabbing your requested data, please reload this page to se progressed data')

        return redirect('/admin/crawler_manager/crawelissue/')