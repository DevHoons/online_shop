import requests
from django.conf import settings

# key 를 이용하여 token 을 가지고 옴
def get_token():
    access_data = {
        "imp_key": settings.IAMPORT_KEY,
        "imp_secret": settings.IAMPORT_SECRET,
    }
    url = "https://api.iamport.kr/users/getToken"
    req = requests.post(url, data=access_data)
    access_res = req.json()

    if access_res["code"] is 0:
        return access_res["response"]["access_token"]
    else:
        return None


# order id로 결제를 할 수 있도록 해주는 함수
def payments_prepare(order_id, amount, *args, **kwargs):
    access_token = get_token()

    if access_token:
        access_data = {"merchant_uid": order_id, "amount": amount}
        url = "https://api.iamport.kr/payments/prepare"
        headers = {"Authorization": access_token}
        req = requests.post(url, data=access_data, headers=headers)
        res = req.json()

        if res["code"] != 0:
            raise ValueError("API 통신 오류")
    else:
        raise ValueError("토큰 오류")


# 결제가 되었을때, 실제 결제가 올바르게 되었는지 확인해주는 함수
def find_transaction(order_id, *args, **kwargs):
    access_token = get_token()

    if access_token:
        url = "https://api.iamport.kr/payments/find/" + order_id
        headers = {"Authorization": access_token}
        req = requests.post(url, headers=headers)
        res = req.json()

        if res["code"] == 0:
            context = {
                "imp_id": res["response"]["imp_uid"],
                "merchant_order_id": res["response"]["merchant_uid"],
                "amount": res["response"]["amount"],
                "status": res["response"]["status"],
                "type": res["response"]["pay_method"],
                "receipt_url": res["response"]["receipt_url"],
            }
            return context
        else:
            return None
    else:
        raise ValueError("토큰 오류")
