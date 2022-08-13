
from django import forms
from django.core.exceptions import ValidationError
from .models import Help, HELP_CATEGORIES

class HelpRequestForm(forms.ModelForm):
    category = forms.ChoiceField(choices= HELP_CATEGORIES, initial= None,widget= forms.Select
                           (attrs={'placeholder':'Select a help category'}))
    description= forms.CharField(max_length=1000, widget= forms.Textarea
                           (attrs={'placeholder':'Add a description', 'rows':4, 'cols':15}))
    
    class Meta:
        model = Help
        fields = ('category','description')

    def __init__(self, *args, **kwargs):
        super(HelpRequestForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'w-full mt-2 px-4 py-2 rounded-xl background-white'
