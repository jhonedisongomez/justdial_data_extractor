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
    
    # def get_queryset(self, request):
    #     qs = super(CrawelIssueAdmin, self).get_queryset(request)
    #     return qs.filter(user=request.user)

    # def has_change_permission(self, request, obj=None):
    #     if not obj:
    #         # the changelist itself
    #         return True
    #     return obj.user == request.user
    #def save_model(self, request, obj, form, change):
    #    obj.user = request.user
    #    obj.save()

    #def get_queryset(self, request):
    #    qs = super(CrawelIssueAdmin, self).get_queryset(request)
    #    return qs.filter(user=request.user)

    #def has_change_permission(self, request, obj=None):
    #    if not obj:
            # the changelist itself
    #        return True
    #    return obj.user == request.user

    resource_class = CrawelIssuekResource

    list_display = ('keyword', 'city_name', 'title', 'rating', 'votes', 'address', 'contact', 'website')
    list_filter = ['city_name', 'keyword', 'rating']
    search_fields = ['keyword', 'city_name', 'title', 'rating', 'votes', 'address', 'contact', 'website']
    list_per_page = 5000

    #def get_queryset(self, request):
    #    qs = super(CrawelIssueAdmin, self).get_queryset(request)
    #    return qs.filter(created_by=request.user)

    #def save_model(self, request, obj, form, change):
    #    if not change:
    #        # the object is being created, so set the user
    #        obj.created_by = request.user
    #    obj.save()


admin.site.site_header = 'Justdial Scrapper'
admin.site.site_title = 'Get data from Justdial by city and categories'
admin.site.index_title = 'Justdial Crawler'
