from django.contrib import admin
# Register your models here.
from .models import *

class UserAdmin( admin.ModelAdmin) :
    search_fields = ('id','name','email')
    list_display =['id','name','email']
    list_filter = ['id']

class UniversityAdmin( admin.ModelAdmin) :
    search_fields = ('name',)
    list_display =['name','mail']
    list_filter = ['name','mail']
class QuestionAdmin(admin.ModelAdmin):
    search_fields =('name','title','university')
    
    list_display = ('id','title', 'user', 'university', 'upvotes_count', 'downvotes_count')

    def upvotes_count(self, obj):
        return obj.upvotes.count()

    def downvotes_count(self, obj):
        return obj.downvotes.count()
    
class AnswerAdmin(admin.ModelAdmin):
    search_fields =('name','text','university')

    list_display = ('id', 'user', 'question', 'upvotes_count', 'downvotes_count')


    def upvotes_count(self, obj):
        return obj.upvotes.count()

    def downvotes_count(self, obj):
        return obj.downvotes.count()


admin.site.register(User,UserAdmin)

admin.site.register(University,UniversityAdmin)
admin.site.register(Question,QuestionAdmin)
admin.site.register(Answer,AnswerAdmin)