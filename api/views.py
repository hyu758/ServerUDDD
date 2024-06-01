from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
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
        for order in orders:
            date_str = order.orderLabel[:8]  # Get the YYYYMMDD part of the string
            date_obj = datetime.strptime(date_str, '%Y%m%d').date()
            if date_obj in order_data:
                order_data[date_obj] += 1
            else:
                order_data[date_obj] = 1
        
        # Convert order_data to a list of dictionaries
        order_list = [{'date': str(date), 'count': count} for date, count in order_data.items()]
        
        total_accounts = Account.objects.count()
        
        total_revenue = Order.objects.filter(token__isnull=False).exclude(token='').aggregate(Sum('totalAmount'))['totalAmount__sum'] or 0
        
        return render(request, 'api/dashboard.html', {
            'order_data': json.dumps(order_list),
            'total_accounts': total_accounts,
            'total_revenue': format_number(total_revenue)
        })

def format_number(value):
    try:
        value = int(value)
        return '{:,.0f}'.format(value).replace(',', '.')
    except (ValueError, TypeError):
        return value