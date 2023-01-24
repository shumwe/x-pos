from posApp.models import Notify, Products

def low_stock(request):
    notifications = Notify.objects.filter(resolved=False)
    len_notifications = len(notifications)
    return dict(low_stock_notifications=len_notifications)

def resolve_stock_notifaction(request):
    nots = Notify.objects.filter(resolved=False)
    if nots:
        for n in nots:
            if n.product:
                p_id = n.product.id
                product = Products.objects.get(id=p_id)
                if product.product_count > product.minimum_stock:
                    n.resolved = True
                    n.save()
                elif product.product_count <= product.minimum_stock:
                    n.resolved = False
                    n.save()
            return {"True": True}
    else:
        return {"False": False}