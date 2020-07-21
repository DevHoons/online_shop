from django import forms
from .models import Coupon


class AddCouponForm(forms.Form):
    code = forms.CharField(label="쿠폰 번호")
