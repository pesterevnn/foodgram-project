from ..models import Purchases


def get_purchases_count(request):
    curent_user = request.user
    if curent_user.is_authenticated:
        purchases = Purchases.objects.filter(customer=curent_user)
        purchases_count = purchases.count()
    else:
        purchases = None
        purchases_count = 0
    return{
        'purchases': purchases,
        'purchases_count': purchases_count
    }
