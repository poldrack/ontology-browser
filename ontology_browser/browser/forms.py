from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by ID or description...'
        })
    )
    type_filter = forms.ChoiceField(
        choices=[
            ('all', 'All Types'),
            ('task', 'Task'),
            ('survey', 'Survey')
        ],
        required=False,
        initial='all',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )