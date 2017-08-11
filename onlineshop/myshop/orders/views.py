# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False) # 延后保存order对象
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            cart.clear()
            order_created.delay(order.id)  # 开启异步任务
            return render(request, 
                            'orders/order/created.html', 
                            {'order': order})

    else:
        form = OrderCreateForm()
    return render(request, 
                 'orders/order/create.html',
                 {'cart': cart, 'form': form})

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    return render(request,
                    'admin/orders/order/detail.html',
                    {'order': order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order,id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order}) 
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename=order_{}.pdf'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response, 
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
