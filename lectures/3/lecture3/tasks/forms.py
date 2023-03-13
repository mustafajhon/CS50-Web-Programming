from django import forms

class NewTaskForm(forms.Form):
    newTask = forms.CharField(label="New task", max_length= 500)
    priority= forms.IntegerField(label="Priority", min_value=1,max_value=10)



