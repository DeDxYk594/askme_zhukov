from django import forms


class AskForm(forms.Form):
    title = forms.CharField(label="Title", max_length=200)
    text = forms.CharField(label="Text", max_length=2000)
    tags = forms.CharField(label="Tags", max_length=1000)
    image = forms.ImageField(label="Image")


class AnswerForm(forms.Form):
    answer = forms.CharField(label="Title", max_length=200)


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


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=3)
    email = forms.EmailField(max_length=100, min_length=8)
    password = forms.CharField(max_length=100, min_length=8, strip=True, required=True)
    repeat_password = forms.CharField(max_length=100, strip=True, required=True)
    avatar = forms.ImageField(required=True)


class SettingsForm(forms.Form):
    username = forms.CharField(max_length=100, min_length=3)
    email = forms.EmailField(max_length=100, min_length=8)
    password = forms.CharField(max_length=100, min_length=8, strip=True, required=False)
    repeat_password = forms.CharField(max_length=100, strip=True, required=False)
    avatar = forms.ImageField(required=False)
