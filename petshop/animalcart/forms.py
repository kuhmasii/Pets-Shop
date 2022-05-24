from django import forms


class CartProductForm(forms.Form):
    QUANTITY = [
        (i, str(i)) for i in range(1, 21)
    ]

    quantity = forms.TypedChoiceField(
        choices=QUANTITY, coerce=int
    )
    override = forms.BooleanField(
        required=False, initial=False,
        widget=forms.HiddenInput
    )
