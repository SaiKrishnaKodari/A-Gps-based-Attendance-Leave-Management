from django.forms import ModelForm
from . import models
class LeaveModelForm(ModelForm):
    class Meta:
        model=models.LeaveModel
        exclude=["date","isApproved","isRejected","user"]