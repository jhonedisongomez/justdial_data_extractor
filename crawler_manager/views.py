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
        
        city_name = request.POST['city_name']
        keyword = request.POST['keyword']
        numof_instance = request.POST['numof_instance']

        user = request.user.id
        print (type(user))
        user = str(request.user.id)
        print (type(user))

        keywordCompleted = ''
        keywords = keyword.split(" ")

        for i,x in enumerate(keywords):
                if i == 0:
                    keywordCompleted = x.capitalize()
                elif i > 0:
                    keywordCompleted = keywordCompleted + "-" + x.capitalize()

        data = (city_name, keywordCompleted, numof_instance, user,)
        print (data)
        start_srabbing(data)
        messages.success(request, 'We are scrabbing your requested data, please reload this page to see progressed data')

        return redirect('/admin/crawler_manager/crawelissue/')

@staff_member_required
def second_scrap(request):
    if request.method == 'GET':
        return render(request, 'crawler_manager/crawler_page.html')
        