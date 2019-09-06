from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse


from .models import OrderItem, Order
from .forms import OrderCreateForm
from .tasks import order_created

from cart.cart import Cart


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            order_created.delay(order.id)
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html',
        {'form': form, 'cart': cart}
    )


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(
        request,
        'admin/orders/order/detail.html',
        {'order': order}
    )
