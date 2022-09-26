from django import template
import datetime

from coffee_app.models import Table
# from coffee_app.models import Appointment


register = template.Library()

# @register.filter(name='is_time_available')
# def is_time_available(day, time):
#     hour = time.split(":")[0]
#     minute = time.split(":")[1]
#     time = datetime.time(hour=int(hour), minute=int(minute))
#     return Appointment.is_time_available(time, day)

@register.filter(name='table_booked_at_time')
def table_booked_at_time(day, time):
    table, created =  Table.objects.get_or_create(booking_time=time, day=day)
    if table.booked:
        return table
    return None

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 