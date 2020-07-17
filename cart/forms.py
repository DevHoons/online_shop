from django import forms

# 클라이언트 화면에 입력 폼을 만들어주고, 입력값에 대한 전처리 담당
class AddProductForm(forms.Form):
    quantity = forms.IntegerField()
    is_update = forms.BooleanField(
        required=False, initial=False, widget=forms.HiddenInput
    )

