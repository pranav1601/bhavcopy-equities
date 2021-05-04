from django import forms  
class searchForm(forms.Form):  
    search_equity =forms.CharField(
        label='',
        max_length=30,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search for equity here',
                'class':'search'
            }
        )
    )