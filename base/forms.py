from django import forms
from django.contrib.auth import get_user_model # djangoが設定しているユーザーモデル


class UserCreationForm(forms.ModelForm):
    password = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password', )

    def clean_password(self):
        # cleaned_dataにはformの中で 検証された後適切なデータとして確認されたデータが入ります。
        password = self.cleaned_data.get("password")
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user