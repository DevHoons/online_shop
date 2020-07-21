from django.shortcuts import redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .forms import AddCouponForm
from .models import Coupon


@require_POST
def add_coupon(request):
    now = timezone.now()
    form = AddCouponForm(request.POST)
    if form.is_valid():
        # 안전성을 위해서 cleaned_data에 넣어서 사용해주는 것이 좋음
        code = form.cleaned_data["code"]

        # 쿠폰번호를 추가하는 작업
        try:
            coupon = Coupon.objects.get(
                code__iexact=code, use_from__lte=now, use_to__gte=now, active=True
            )
            request.session["coupon_id"] = coupon.id
        except Coupon.DoesNotExist:
            request.session["coupon_id"] = None

    return redirect("cart:detail")
