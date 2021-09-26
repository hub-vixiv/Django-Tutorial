from django.contrib import admin

# Register your models here.

from .models import Question, Choice

""" デフォルトのままで表示"""
# admin.site.register(Question)
# admin.site.register(Choice)


""" 順番を入れ替えてみる """
# class QuestionAdmin(admin.ModelAdmin):
#     fields = ['pub_date', 'question_text']

""" フィールドセットを作って表示してみる """
# class QuestionAdmin(admin.ModelAdmin):
#     fieldsets = [
#         (None,               {'fields': ['question_text']}),
#         ('Date information', {'fields': ['pub_date']}),
#     ]

""" Questionの登録時にChoiceも登録できるようにする"""
""" Choice 入力３つ＋配置はデフォルトのままで表示"""
# class ChoiceInline(admin.StackedInline):
#     model = Choice
#     extra = 3
""" Choiceをコンパクトに表示"""
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    """ 登録時のフィールドの表示"""
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    """ 変更画面のリスト表示　fieldsetsより先に書くと適用されない"""
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
# registerの第２引数に、作ったclass


