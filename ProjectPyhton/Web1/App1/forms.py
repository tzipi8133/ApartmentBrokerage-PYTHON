from django import forms
from .models import Person, Seller, Appartment, Request
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class AddLoginForm(forms.Form):
    userName = forms.CharField(label="UserName", max_length=10)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

class AddRegisterForm(UserCreationForm):
    class Meta:
        model = Person
        fields = [
            "username",
            "password1",
            "password2",
            "email",
            "phone",
            "isSeller",
        ]


class AddAppartmentForm(forms.ModelForm):
    class Meta:
        model = Appartment
        fields = [
            "id",
            "city",
            "street",
            "buildingNum",
            "floorNum",
            "roomNum",
            "condition",
            "img",
            "brokerage",
        ]

    img = forms.ImageField(required=False, label="תמונה ראשית של הדירה")
    brokerage = forms.BooleanField(required=False, label="האם הדירה נמכרת בתיווך?")


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ["id", "message"]
        widgets = {
            "id": forms.TextInput(attrs={"placeholder": "Enter request ID"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Enter your message", "rows": 4}
            ),
        }
class UpdateStatusForm(forms.ModelForm):
    class Meta:
        model = Appartment
        fields = ['status']