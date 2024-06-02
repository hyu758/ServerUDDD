from django.shortcuts import render
from django.views import View
from .models import order as Order
from .models import accounts as Account
from datetime import datetime, timedelta
import json
from django.db.models import Sum

class Dashboard(View):
    def get(self, request):
        one_week_ago = datetime.now() - timedelta(days=7)
        orders = Order.objects.filter(orderLabel__gte=one_week_ago.strftime('%Y%m%d')).order_by('orderLabel')
        
        # Extract dates and count orders per day
        order_data = {}
        revenue_data = {}
        for ord in orders:
            date_str = ord.orderLabel[:8]  # Get the YYYYMMDD part of the string
            date_obj = datetime.strptime(date_str, '%Y%m%d').date()
            if date_obj in order_data:
                order_data[date_obj] += 1
            else:
                order_data[date_obj] = 1

            if ord.token:
                if date_obj in revenue_data:
                    revenue_data[date_obj] += ord.totalAmount
                else:
                    revenue_data[date_obj] = ord.totalAmount
        
        order_list = [{'date': str(date), 'count': count} for date, count in order_data.items()]
        revenue_data_list = [{'date': key.strftime('%Y-%m-%d'), 'revenue': value} for key, value in revenue_data.items()]
        
        total_accounts = Account.objects.count()
        total_revenue = Order.objects.filter(token__isnull=False).exclude(token='').aggregate(Sum('totalAmount'))['totalAmount__sum'] or 0

        # Get top 5 spenders by email in the past week
        top_spenders = Order.objects.filter(orderLabel__gte=one_week_ago.strftime('%Y%m%d')).values('email').annotate(total_spent=Sum('totalAmount')).order_by('-total_spent')[:5]
        top_spenders_data = [{'email': spender['email'], 'total_spent': spender['total_spent']} for spender in top_spenders]

        return render(request, 'api/dashboard.html', {
            'order_data': json.dumps(order_list),
            'revenue_data': json.dumps(revenue_data_list),
            'total_accounts': total_accounts,
            'total_revenue': format_number(total_revenue),
            'top_spenders_data': json.dumps(top_spenders_data),
        })

def format_number(value):
    try:
        value = int(value)
        return '{:,.0f}'.format(value).replace(',', '.')
    except (ValueError, TypeError):
        return value
