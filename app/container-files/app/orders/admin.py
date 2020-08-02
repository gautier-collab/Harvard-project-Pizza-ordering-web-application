from django.contrib import admin, messages

from .models import Crust, Topping, Pizza, Extra, Sub, Pasta, Salad, Dinner_platter, Order, unsave

admin.site.register(Pizza)
admin.site.register(Crust)
admin.site.register(Topping)
admin.site.register(Extra)
admin.site.register(Sub)
admin.site.register(Pasta)
admin.site.register(Salad)
admin.site.register(Dinner_platter)
admin.site.register(Order)

def sendmsg(sender, **kwargs):
    messages.info(request, "The pizza wasn't added because one with the same name already exists for that same crust.")
unsave.connect(sendmsg, sender=Pizza)
