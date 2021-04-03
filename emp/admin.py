from django.contrib import admin
from .models import *
my_models=[LeaveModel,InTimeModel,OutTimeModel,Profile,production_time]
admin.site.register(my_models)