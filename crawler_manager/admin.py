from django.contrib import admin
from . import models
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
        # exclude = ('imported', )


@admin.register(models.CrawelIssue)
class CrawelIssueAdmin(ImportExportModelAdmin):
    resource_class = CrawelIssuekResource

    list_display = ('keyword', 'city_name', 'title', 'rating', 'votes', 'address', 'contact', 'website')
    list_filter = ['city_name', 'rating']
    search_fields = ['keyword', 'city_name', 'title', 'rating', 'votes', 'address', 'contact', 'website']


admin.site.site_header = 'Justdial Scrapper'
admin.site.site_title = 'Get data from Justdial by city and categories'
admin.site.index_title = 'Justdial Crawler'