from django.contrib import admin
from . import models
from .models import CrawelIssue
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import AdminSite
from django.http import HttpResponse


    
class CrawelIssuekResource(resources.ModelResource):
    
    class Meta:
        model = models.CrawelIssue
        skip_unchanged = True
        report_skipped = False
        # fields = ('id', 'name', 'price',)
        #exclude = ('user', )


@admin.register(models.CrawelIssue)
class CrawelIssueAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    resource_class = CrawelIssuekResource

    list_display = ('keyword', 'city_name', 'title', 'rating', 'votes', 'address', 'contact', 'website')
    list_filter = ['city_name', 'keyword', 'rating']
    search_fields = ['keyword', 'city_name', 'title', 'rating', 'votes', 'address', 'contact', 'website']
    list_per_page = 5000

admin.site.site_header = 'Justdial Scrapper'
admin.site.site_title = 'Get data from Justdial by city and categories'
admin.site.index_title = 'Justdial Crawler'
