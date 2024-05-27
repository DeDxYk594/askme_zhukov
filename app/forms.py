from django import forms


class AskForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    text = forms.CharField(label="Text", max_length=2000)
    tags = forms.CharField(label="Tags", max_length=1000)
    image = forms.ImageField(label="Image")


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
    )
