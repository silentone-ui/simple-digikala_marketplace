from django import forms

class AddBalanceForm(forms.Form):
    amount = forms.DecimalField(
        label="مبلغ (تومان)",
        min_value=1000, 
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 10000'})
    )
