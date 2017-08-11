# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
import datetime
from django.http import HttpResponse
from django.contrib import admin
from django.urls import reverse

from .models import Order, OrderItem

# 自定义行为，导出CSV文件
def export_to_csv(modeladmin, request, queryset): 
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;\
            filename={}.csv'.format(opts.verbose_name)
    writer = csv.writer(response)

    fields = [ field for field in opts.get_fields() 
                if not field.many_to_many and not field.one_to_many ]
    writer.writerow([ field.verbose_name for field in fields ])
    for obj in queryset:
        data_row = [] 
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

export_to_csv.short_description = 'Export to CSV'

# list-display的回调
def order_detail(obj):
    return '<a href="{}">View</a>'.format(
            reverse('orders:admin_order_detail', args=[obj.id]))
order_detail.allow_tags = True  # 注意django会自动转意html,这里避免转意

# 产生发票pdf
def order_pdf(obj):
    return '<a href="{}">PDF</a>'.format(
            reverse('orders:admin_order_pdf', args=[obj.id]))
order_pdf.allow_tags = True  
order_pdf.short_description = 'PDF bill'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'email', 'address',
                    'postal_code', 'city', 'paid', 'created', 'updated', 
                    'discount',
                    order_detail,
                    order_pdf]

    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [ export_to_csv ]

admin.site.register(Order, OrderAdmin)
