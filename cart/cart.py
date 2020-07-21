from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupon.models import Coupon


class Cart(object):
    def __init__(self, request):  # 초기화 작업
        self.session = request.session
        cart = self.session.get(settings.CART_ID)
        if not cart:
            cart = self.session[settings.CART_ID] = {}
        self.cart = cart
        self.coupon_id = self.session.get("coupon_id")

    def __len__(self):  # 리스트, 딕셔너리에 사용 되는 파이썬 문법, 개수를 셀때 주로 사용
        # cart에 담긴 제품의 갯수를 더해줌
        return sum(item["quantity"] for item in self.cart.values())

    def __iter__(self):  # for문을 사용할때 요소들을 어떤식으로 건네줄건지?
        # 제품들 번호 목록 가져오기
        product_ids = self.cart.keys()
        # filter 를 이용해서 장바구니에 들어있는 제품만 가지고 오기
        products = Product.objects.filter(id__in=product_ids)

        # 담긴 제품을 하나씩 꺼내서 가지고 옴
        for product in products:
            self.cart[str(product.id)]["product"] = product

        # 제품 가격 업데이트 (숫자형으로)
        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]

            yield item

    def add(self, product, quantity=1, is_update=False):
        product_id = str(product.id)

        # product_id가 있지 않으면 제품 정보를 집어넣어주는 작업
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0, "price": str(product.price)}

        # 제품 정보를 수정하는 작업
        if is_update:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity

        self.save()

    # session에 정보를 업데이트 하기 위한 함수
    def save(self):
        # 제품 정보가 최초로 등록될 때 반영이 됌
        self.session[settings.CART_ID] = self.cart
        # 제품 정보가 중간중간에 업데이트 됐을 때 반영해주는 작업
        self.session.modified = True

    def remove(self, product):
        product_id = str(product.id)
        # 제품이 cart에 들어있다면 지우는 작업
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    # 장바구니 비워주는 함수
    def clear(self):
        self.session[settings.CART_ID] = {}
        self.session["coupon_id"] = None
        self.session.modified = True

    # 제품들의 가격과 갯수를 가지고와서 계산해주는 함수
    def get_product_total(self):
        return sum(item["price"] * item["quantity"] for item in self.cart.values())

    @property
    def coupon(self):
        if self.coupon_id:
            return Coupon.objects.get(id=self.coupon_id)
        return None

    # 쿠폰 적용 후 계산하기 위한 함수
    def get_discount_total(self):
        if self.coupon:
            if self.get_product_total() >= self.coupon.amount:
                return self.coupon.amount
        return Decimal(0)

    # 실제 결제해야되는 금액 계산해주는 함수
    def get_total_price(self):
        return self.get_product_total() - self.get_discount_total()
