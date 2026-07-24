import random
import string

from offers.models import Coupon


def generate_coupon_code(length=8):

    while True:

        code = ''.join(
            random.choices(
                string.ascii_uppercase + string.digits,
                k=length
            )
        )

        if not Coupon.objects.filter(coupon_code=code).exists():
            return code