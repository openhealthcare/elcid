"""
Forms for eLCID
"""
from django import forms

class BulkCreateUsersForm(forms.Form):
    """
    Form for uploading a CSV of users to add.
    """
    users = forms.FileField()
