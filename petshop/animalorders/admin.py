

import csv
import datetime as dt
from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponse
from . models import Order, OrderItem
from django.utils.safestring import mark_safe


def file_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(
        content_type='text/csv', headers={'Content-Disposition': f'attachment; "filename={opts.verbose_name}.csv"'}
    )
    writer = csv.writer(response)
    fields = [
        field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many
    ]

    # write a first row with header information
    writer.writerow([field.verbose_name for field in fields])
    # write data rows
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, dt.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response


file_to_csv.short_description = 'Exporting to CSV'



# def pdf_invoice(obj):
#     url = reverse('animalorders:animalorders-pdf', args=[obj.id])
#     return mark_safe(f'<a href="{url}">PDF</a>')
# pdf_invoice.short_description = 'Invoice'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


class OrderAdmin(admin.ModelAdmin):

    list_display = 'id first_name last_name email city paid created'.split()
    list_filter = 'paid created updated'.split()
    inlines = (OrderItemInline,)
    actions = (file_to_csv, )





admin.site.register(Order, OrderAdmin)
