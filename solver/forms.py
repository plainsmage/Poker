from django import forms

class SolverInputForm(forms.Form):
    hand = forms.CharField(max_length=10, required=True)
    board = forms.CharField(max_length=20, required=False)

