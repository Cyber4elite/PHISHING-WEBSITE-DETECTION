from django import forms


class URLScanForm(forms.Form):
    url = forms.CharField(
        label='Enter URL to scan',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter any text or URL',
            'required': False
        }),
        max_length=1000,
        required=False
    )
