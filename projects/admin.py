from django.contrib import admin

from projects.models import Project, Review, Tag

# Register your models here.
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','source_link','vote_total','vote_ratio')
    list_display_links = ['title']
    search_fields= ['title']
    list_filter= ['title']
    
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('value','owner')
    

admin.site.register(Project,ProjectAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(Tag)