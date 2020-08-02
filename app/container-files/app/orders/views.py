import re, datetime, json, stripe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import View
from django.conf import settings
from .models import Profile, Crust, Topping, OrderTopping, Extra, OrderExtra, Pizza, Sub, Pasta, Salad, Dinner_platter, Cart_pizza, Cart_sub, Cart_pasta, Cart_salad, Cart_dinner_platter, Order



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "orders/login.html", {"error": "Invalid credentials."})
    return render(request, "orders/login.html")



def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "")
        last_name = request.POST.get("last_name", "")
        email = request.POST.get("email", "")
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        # Check that fields are valid:
        fields =[first_name, last_name, email, username, password]
        for field in fields:
            counter = 0
            for char in field:
                counter +=1
            if counter == 0:
                return render(request, "orders/signup.html", {"error": "Don't leave any field empty please", "first_name":first_name, "last_name":last_name, "email":email, "username":username, "password":password})
        if not re.search(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$", first_name):
            return render(request, "orders/signup.html", {"error": "Invalid character(s) in first name", "first_name":first_name, "last_name":last_name, "email":email, "username":username, "password":password})
        if not re.search(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$", last_name):
            return render(request, "orders/signup.html", {"error": "Invalid character(s) in last name", "first_name":first_name, "last_name":last_name, "email":email, "username":username, "password":password})            
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return render(request, "orders/signup.html", {"error": "Invalid email address", "first_name":first_name, "last_name":last_name, "email":email, "username":username, "password":password})
        if User.objects.filter(username=username).exists():
            return render(request, "orders/signup.html", {"error": "This username already exists. Please choose another one.", "first_name":first_name, "last_name":last_name, "email":email, "username":username, "password":password})

        if len(username) < 3: 
            return render(request, "orders/signup.html", {"error": "Your username must be at least three characters long.", "first_name":first_name, "last_name":last_name, "email":email, "username":username, "password":password})
        if len(password) < 5: 
            return render(request, "orders/signup.html", {"error": "Your password must be at least five characters long.", "first_name":first_name, "last_name":last_name, "email":email, "username":username, "password":password})

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, "orders/login.html", {"success": "Your account is succesfully created. You can sign in."})
    return render(request, "orders/signup.html", {"success": None})



def logout_view(request):
    logout(request)
    return render(request, "orders/login.html", {"error": "Logged out."})



def index(request):
    return menu(request, "", "")



def menu(request, success, error):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"success": None})

    # Include only crusts that are already associated with pizza(s)
    crusts = []
    for crust in Crust.objects.all():
        try: 
            temp = crust.pizzas.all()[0]
            crusts.append(crust)
        except:
            pass

    context = {
        "user": request.user,
        "crusts": crusts,
        "toppings": Topping.objects.all(),
        "extras": Extra.objects.all(),
        "pizzas": Pizza.objects.all(),
        "subs": Sub.objects.all(),
        "pastas": Pasta.objects.all(),
        "salads": Salad.objects.all(),
        "platters": Dinner_platter.objects.all(),
        "success": success,
        "error": error
    }
    return render(request, "orders/index.html", context)



def cart(request):
    if not request.user.is_authenticated:
        return render(request, "orders/login.html", {"success": None})

    profile = Profile.objects.all().get(user=request.user)

    items = {'pizzas':[], 'subs':[], 'pasta':[], 'salads':[], 'dinner_platters':[]}
    for pizza in profile.pizzas.all():
        items['pizzas'].append({'id':pizza.id, 'name':pizza.pizza.name, 'crust':pizza.pizza.crust.name, 'size':pizza.size, 'topping_1':pizza.topping_1.name, 'topping_2':pizza.topping_2.name, 'topping_3':pizza.topping_3.name, 'topping_4':pizza.topping_4.name})
    for sub in profile.subs.all():
        items['subs'].append({'id':sub.id, 'name':sub.sub.name, 'size': sub.size, 'extra_1': sub.extra_1.name, 'extra_2': sub.extra_2.name, 'extra_3': sub.extra_3.name, 'extra_4': sub.extra_4.name})
    for pasta in profile.pasta.all():
        items['pasta'].append({'id':pasta.id, 'name':pasta.pasta.name})
    for salad in profile.salads.all():
        items['salads'].append({"id":salad.id, 'name':salad.salad.name})
    for dinner_platter in profile.dinner_platters.all():
        items['dinner_platters'].append({'id': dinner_platter.id, 'name': dinner_platter.dinner_platter.name, 'size': dinner_platter.size})

    profile.checkout_items = json.dumps(items) # JSON ---> string because Django has no field for dict
    profile.save()

    error = None
    if profile.msg == True:
        error = "Elements of your cart have been removed because they were modified in the menu of the restaurant."
        profile.msg = False
        profile.save()

    context = {
        "profile": profile,
        "cart_version" : profile.cart_version,
        "error" : error
        }
    return render(request, "orders/cart.html", context)



def remove(request):

    profile = Profile.objects.all().get(user=request.user)

    if request.method == "POST":
        
        itemType = request.POST.get("type")
        itemID = request.POST.get("ID")
        
        if itemType == "pizza":
            Cart_pizza.objects.all().get(id=itemID).delete()
            print("\nThe pizza was succesfully removed from the cart.\n")
        elif itemType == "sub":
            Cart_sub.objects.all().get(id=itemID).delete()
            print("\nThe sub was succesfully removed from the cart.\n")
        elif itemType == "pasta":
            Cart_pasta.objects.all().get(id=itemID).delete()
            print("\nThe pasta was succesfully removed from the cart.\n")
        elif itemType == "salad":
            Cart_salad.objects.all().get(id=itemID).delete()
            print("\nThe salad was succesfully removed from the cart.\n")
        elif itemType == "dinner_platter":
            Cart_dinner_platter.objects.all().get(id=itemID).delete()
            print("\nThe dinner_platter was succesfully removed from the cart.\n")

        # Update cart version (to detect changes if payment process is ongoing)
        profile.cart_version += 1
        profile.save()

    return cart(request)



def checkout1(request):
    variables = {
        "cart_version": float(request.POST.get("cart_version")),
        "amount": float(request.POST.get("total")),
        "error": False
    }
    return checkout2(request, variables)


def checkout2(request, variables):

    context = {
        "cart_version": variables["cart_version"],
        "amount": variables["amount"],
        "error": variables["error"],
        "profile": Profile.objects.all().get(user=request.user),
        "publishable_key" : settings.STRIPE_PUBLISHABLE_KEY
    };
    return render(request, "orders/checkout.html", context)



def place(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY
    token = request.POST.get("stripeToken")
    profile = Profile.objects.all().get(user=request.user)

    # Check that the cart hasn't been updated since the checkout process was started:
    if profile.cart_version != float(request.POST.get("cart_version")):
        return render(request, "orders/cart.html", {"error": "Sorry, your order couldn't be placed because your cart was edited during the checkout process."})
    else:

        # Stripe error handling:
        try:
            # Perform transaction
            cent_amount = int(100 * float(request.POST.get("amount")))
            stripe.Charge.create(
                amount = cent_amount, # value is in cents
                currency="usd",
                source=token,
                description="Pinnochio’s Pizza & Subs purchase",
            )

            # Place orders
            amount = request.POST.get("amount")
            items = profile.checkout_items
            order = Order(first_name = profile.user.first_name, last_name = profile.user.last_name, price = amount, timestamp = datetime.datetime.now().timestamp() , items = profile.checkout_items)
            order.save()

            # Placed items are now removed from user's cart
            items = json.loads(profile.checkout_items)
            for pizza in items["pizzas"]:
                Cart_pizza.objects.all().get(id=pizza["id"]).delete()
            for sub in items["subs"]:
                Cart_sub.objects.all().get(id=sub["id"]).delete()
            for pasta in items["pasta"]:
                Cart_pasta.objects.all().get(id=pasta["id"]).delete()
            for salad in items["salads"]:
                Cart_salad.objects.all().get(id=salad["id"]).delete()
            for dinner_platter in items["dinner_platters"]:
                Cart_dinner_platter.objects.all().get(id=dinner_platter["id"]).delete()

            return menu(request, success = "Your payment has been made and your order is placed. Thank you !", error = "")

        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            print('Status is: %s' % e.http_status)
            print('Type is: %s' % e.error.type)
            print('Code is: %s' % e.error.code)
            # param is '' in this case
            print('Param is: %s' % e.error.param)
            print('Message is: %s' % e.error.message)
        except stripe.error.RateLimitError as e:
            print("Too many requests made to the API too quickly")
            pass
        except stripe.error.InvalidRequestError as e:
            print("Invalid parameters were supplied to Stripe's API")
            pass
        except stripe.error.AuthenticationError as e:
            print("Authentication with Stripe's API failed. Maybe you changed API keys recently")
            pass
        except stripe.error.APIConnectionError as e:
            print("Network communication with Stripe failed")
            pass
        except stripe.error.StripeError as e:
            print("Display a very generic error to the user, and maybe send yourself an email")
            pass
        except Exception as e:
            print("Error unrelated to Stripe")
            pass

        variables = {
            "cart_version": float(request.POST.get("cart_version")),
            "amount": float(request.POST.get("amount")),
            "error": True
        }
        return checkout2(request, variables)



def orders(request):

    if request.method == "POST":

        orders = []
        for order in Order.objects.all():
            date = datetime.datetime.fromtimestamp(order.timestamp).strftime('%B %d, %Y at %H:%M')
            items = json.loads(order.items) # string ---> JSON object
            orders.append({"order": order, "date": date, "items": items})

        context = {
            "orders": orders
        };
        return render(request, "orders/orders.html", context)

    else:
        return menu(request, success = "", error = "Accessing this page requires clicking the 'Orders' button with a superuser account.")



# ---------------------------------------- Ajax requests data ----------------------------------------



# Processing data of pizza that needs to be added to cart
class AjaxPizza(View):

    def get(self, request):
        # Assign attributes to data retrieved from the clientside JS
        user = User.objects.all().get(id=request.GET.get("user"))
        profile = Profile.objects.all().get(user=user)
        pizza = Pizza.objects.all().get(id=request.GET.get("pizza_id"))
        size = request.GET.get("size")
        quantity = int(request.GET.get("quantity"))

        # Assign toppings if they exist
        if request.GET.get("topping_1") != "None 1" :
            topping_1 = OrderTopping.objects.all().get(name=request.GET.get("topping_1"))
        else:
            topping_1 = OrderTopping.objects.all().get(name="None")
        if request.GET.get("topping_2") != "None 2" :
            topping_2 = OrderTopping.objects.all().get(name=request.GET.get("topping_2"))
        else:
            topping_2 = OrderTopping.objects.all().get(name="None")
        if request.GET.get("topping_3") != "None 3" :
            topping_3 = OrderTopping.objects.all().get(name=request.GET.get("topping_3"))
        else:
            topping_3 = OrderTopping.objects.all().get(name="None")
        if request.GET.get("topping_4") != "None 4" :
            topping_4 = OrderTopping.objects.all().get(name=request.GET.get("topping_4"))
        else:
            topping_4 = OrderTopping.objects.all().get(name="None")

        # Create as many pizzas as requested
        d = {}
        for i in range(quantity):
            d["pizza{0}".format(i)] = Cart_pizza(pizza=pizza, size=size, profile=profile, topping_1=topping_1, topping_2=topping_2, topping_3=topping_3, topping_4=topping_4)

            print('\n', d["pizza{0}".format(i)], '\n')
            d["pizza{0}".format(i)].save()
        
        # Update cart version (to detect changes if payment process is ongoing)
        profile.cart_version += 1
        profile.save()

        return render(request, "orders/index.html")



# Processing data of sub that needs to be added to cart
class AjaxSub(View):

    def get(self, request):
        # Assign attributes to data retrieved from the clientside JS
        user = User.objects.all().get(id=request.GET.get("user"))
        profile = Profile.objects.all().get(user=user)
        sub = Sub.objects.all().get(name=request.GET.get("name"))
        size = request.GET.get("size")
        quantity = int(request.GET.get("quantity"))

        # Assign extras if they exist
        if request.GET.get("extra_1") != "None 1" :
            extra_1 = OrderExtra.objects.all().get(name=request.GET.get("extra_1"))
        else:
            extra_1 = OrderExtra.objects.all().get(name="None")
        if request.GET.get("extra_2") != "None 2" :
            extra_2 = OrderExtra.objects.all().get(name=request.GET.get("extra_2"))
        else:
            extra_2 = OrderExtra.objects.all().get(name="None")
        if request.GET.get("extra_3") != "None 3" :
            extra_3 = OrderExtra.objects.all().get(name=request.GET.get("extra_3"))
        else:
            extra_3 = OrderExtra.objects.all().get(name="None")
        if request.GET.get("extra_4") != "None 4" :
            extra_4 = OrderExtra.objects.all().get(name=request.GET.get("extra_4"))
        else:
            extra_4 = OrderExtra.objects.all().get(name="None")

        print('\n', sub, size, profile.user.username, quantity, "extra 1: ", extra_1, ", extra 2: ", extra_2, ", extra 3: ", extra_3, ", extra 4: ", extra_4, '\n')

        # Create as many subs as requested
        d = {}
        for i in range(quantity):
            d["sub{0}".format(i)] = Cart_sub(sub=sub, size=size, profile=profile, extra_1=extra_1, extra_2=extra_2, extra_3=extra_3, extra_4=extra_4)

            print('\n', d["sub{0}".format(i)], '\n')
            d["sub{0}".format(i)].save()

        # Update cart version (to detect changes if payment process is ongoing)
        profile.cart_version += 1
        profile.save()

        return render(request, "orders/index.html")



# Processing data of pasta that needs to be added to cart
class AjaxPasta(View):

    def get(self, request):
        # Assign attributes to data retrieved from the clientside JS
        user = User.objects.all().get(id=request.GET.get("user"))
        profile = Profile.objects.all().get(user=user)
        pasta = Pasta.objects.all().get(name=request.GET.get("name"))
        quantity = int(request.GET.get("quantity"))
        print('\n', pasta, profile.user.username, quantity, '\n')

        # Create as many pasta as requested
        d = {}
        for i in range(quantity):
            d["pasta{0}".format(i)] = Cart_pasta(pasta=pasta, profile=profile)

            print('\n', d["pasta{0}".format(i)], '\n')
            d["pasta{0}".format(i)].save()

        # Update cart version (to detect changes if payment process is ongoing)
        profile.cart_version += 1
        profile.save()

        return render(request, "orders/index.html")



# Processing data of salad that needs to be added to cart
class AjaxSalad(View):

    def get(self, request):
        # Assign attributes to data retrieved from the clientside JS
        user = User.objects.all().get(id=request.GET.get("user"))
        profile = Profile.objects.all().get(user=user)
        salad = Salad.objects.all().get(name=request.GET.get("name"))
        quantity = int(request.GET.get("quantity"))
        print('\n', salad, profile.user.username, quantity, '\n')

        # Create as many salad as requested
        d = {}
        for i in range(quantity):
            d["salad{0}".format(i)] = Cart_salad(salad=salad, profile=profile)

            print('\n', d["salad{0}".format(i)], '\n')
            d["salad{0}".format(i)].save()

        # Update cart version (to detect changes if payment process is ongoing)
        profile.cart_version += 1
        profile.save()

        return render(request, "orders/index.html")



# Processing data of dinner plater that needs to be added to cart
class AjaxDinner_platter(View):

    def get(self, request):
        # Assign attributes to data retrieved from the clientside JS
        user = User.objects.all().get(id=request.GET.get("user"))
        profile = Profile.objects.all().get(user=user)
        dinner_platter = Dinner_platter.objects.all().get(name=request.GET.get("name"))
        size = request.GET.get("size")
        quantity = int(request.GET.get("quantity"))
        print('\n', dinner_platter, profile.user.username, quantity, '\n')

        # Create as many dinner platters as requested
        d = {}
        for i in range(quantity):
            d["dinner_platter{0}".format(i)] = Cart_dinner_platter(dinner_platter=dinner_platter, profile=profile, size=size)

            print('\n', d["dinner_platter{0}".format(i)], '\n')
            d["dinner_platter{0}".format(i)].save()

        # Update cart version (to detect changes if payment process is ongoing)
        profile.cart_version += 1
        profile.save()

        return render(request, "orders/index.html")
