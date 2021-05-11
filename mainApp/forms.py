from django import forms

PAYMENT_CHOICES = (
    ('EP', 'E-pay'), 
    ('LIV', 'A la livraison'), 
    ('PA', 'Paypal')
)
CITIES_CHOICES = (
    ('TETOUAN', 'Tétouan'),
    ('MARTIL', 'Martil'),
    ('MEDIQ', 'Mediq'),
    ('FNIDEQ', 'Fnideq')
)

class CheckoutForm(forms.Form):
    streetaddress = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Nb rue apt etg',
        'class' : 'form-control',
        'id' : 'streetaddress',
    }))  
    postcodezip = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder' : 'Zip code',
        'class' : 'form-control',
        'id' : 'postcodezip',
    }))
    ville = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control', 'id':'ville'}), choices=CITIES_CHOICES)
    payment_method = forms.ChoiceField(widget=forms.RadioSelect(attrs={'class':'form-control'}), choices=PAYMENT_CHOICES)

