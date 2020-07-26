from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
import datetime, json


sizeChoices = [("Small and large", "Small and large"), ("Small", "Small"), ("Large", "Large")]



# ----------------------------------- Admin items -----------------------------------



class Crust(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name



# Instances that the restaurant owners can edit from the Admin UI
class PizzaCreationTopping(models.Model):
    name = models.CharField(max_length=64, primary_key=True)

    def __str__(self):
        return self.name

# Instances used to add a new pizza to the menu (includes "None" and "Any")
class OrderTopping(PizzaCreationTopping):
    pass

# Instances used to let users order a pizza of less than 4 toppings (includes "None")
class Topping(OrderTopping):
    pass



# Instances that the restaurant owners can edit from the Admin UI
class SubCreationExtra(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    price = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        if self.name == "None" or self.name == "Any":
            return self.name
        else:
            return f"{self.name} for ${format(self.price,'.2f')}"

# Instances used to add a new sub to the menu (includes "None" and "Any")
class OrderExtra(SubCreationExtra):
    pass

# Instances used to let users order a sub of less than 4 extras (includes "None")
class Extra(OrderExtra):
    pass



import django.dispatch
unsave = django.dispatch.Signal(providing_args=["id"])

class Pizza(models.Model):
    name = models.CharField(max_length=64)
    selectable_size = models.CharField(max_length=64, choices = sizeChoices)
    # crust = models.ManyToManyField(Crust, related_name="pizzas")
    crust = models.ForeignKey(Crust, on_delete=models.CASCADE, related_name="pizzas")
    topping_1 = models.ForeignKey(PizzaCreationTopping, on_delete=models.CASCADE, related_name="topping_1_pizzas", null=True, default=None)
    topping_2 = models.ForeignKey(PizzaCreationTopping, on_delete=models.CASCADE, related_name="topping_2_pizzas", null=True, default=None)
    topping_3 = models.ForeignKey(PizzaCreationTopping, on_delete=models.CASCADE, related_name="topping_3_pizzas", null=True, default=None)
    topping_4 = models.ForeignKey(PizzaCreationTopping, on_delete=models.CASCADE, related_name="topping_4_pizzas", null=True, default=None)
    small_price = models.FloatField(null=True, default=0)
    large_price = models.FloatField(null=True, default=0)

    def __str__(self):
        return f"{self.name} {self.crust} pizza (ID: {self.id}); contains {self.topping_1}, {self.topping_2}, {self.topping_3}, {self.topping_4}; exists in {self.selectable_size}; small (if exists) costs ${format(self.small_price,'.2f')}; large (if exists) costs ${format(self.large_price,'.2f')}"

    def save(self, *args, **kwargs):

        # Pizza.objects.filter(name=self.name).filter(crust=self.crust)[0]
        # print("\nA pizza with the same name already exists for that same crust.\n")
        # unsave.send(sender=self.__class__)
        # print("\nFLAG 3\n")

        # Check wether a different ID pizza already has the same name and same crust
        try: 
            p = Pizza.objects.filter(name=self.name).filter(crust=self.crust)[0]
            # Exclude the case of the pizza being edited:
            if p.id == self.id:
                p == Pizza.objects.filter(name=self.name).filter(crust=self.crust)[1]
            print("\n-------The pizza wasn't added because one with the same name already exists for that same crust.-------\n")
            try: 
                unsave.send(sender=self.__class__)
            except:
                print("\n-------The ERROR message couldn't be displayed to the admin user because the request variable of the admin page is not defined-------\n")

        # Pizza doesn't already exist: save it
        except:
            super().save(*args, **kwargs)  
            print("\nPizza created\n")



class Sub(models.Model):
    name = models.CharField(max_length=64, unique=True)
    selectable_size = models.CharField(max_length=64, choices = sizeChoices)
    selectable_extra_1 = models.ForeignKey(SubCreationExtra, on_delete=models.CASCADE, related_name="extra_1_subs", null=True)
    selectable_extra_2 = models.ForeignKey(SubCreationExtra, on_delete=models.CASCADE, related_name="extra_2_subs", null=True)
    selectable_extra_3 = models.ForeignKey(SubCreationExtra, on_delete=models.CASCADE, related_name="extra_3_subs", null=True)
    selectable_extra_4 = models.ForeignKey(SubCreationExtra, on_delete=models.CASCADE, related_name="extra_4_subs", null=True)
    small_price = models.FloatField(default=0, null=True)
    large_price = models.FloatField(default=0, null=True)

    def __str__(self):
        return f"{self.name}; selectable extras: {self.selectable_extra_1}, {self.selectable_extra_2}, {self.selectable_extra_3}, {self.selectable_extra_4}; exists in {self.selectable_size}; small (if exists) costs ${format(self.small_price,'.2f')}; large (if exists) costs ${format(self.large_price,'.2f')}"



class Pasta(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} for ${format(self.price,'.2f')}"



class Salad(models.Model):
    name = models.CharField(max_length=64, unique=True)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} for ${format(self.price,'.2f')}"



class Dinner_platter(models.Model):
    name = models.CharField(max_length=64, unique=True)
    selectable_size = models.CharField(max_length=64, choices = sizeChoices)
    small_price = models.FloatField(null=True, default=0)
    large_price = models.FloatField(null=True, default=0)

    def __str__(self):
        return f"{self.name}; exists in {self.selectable_size}; small (if exists) costs ${format(self.small_price,'.2f')}; large (if exists) costs ${format(self.large_price,'.2f')}"



# ----------------------------------- Cart items -----------------------------------
        


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    msg = models.BooleanField(default=False)

    # Items for which the placement is pending when the user starts the checkout process
    checkout_items = models.CharField(max_length=64, null=True) # Django has no field for dictionaries so we turn them into a string instead

    # Following allows to detect any change in the cart between the moment the user started checkout process and the moment he submitted payment.
    cart_version = models.FloatField(null=True, default=0) 

    def total(self):
        total = 0

        for pizza in self.pizzas.all():
            if pizza.size == "Small":
                total += pizza.pizza.small_price
            else:
                total += pizza.pizza.large_price

        for sub in self.subs.all():
            if sub.size == "Small":
                total += sub.sub.small_price
            else:
                total += sub.sub.large_price
            if sub.extra_1 != "None":
                total += sub.extra_1.price
            if sub.extra_2 != "None":
                total += sub.extra_2.price
            if sub.extra_3 != "None":
                total += sub.extra_3.price
            if sub.extra_4 != "None":
                total += sub.extra_4.price

        for pasta in self.pasta.all():
            total += pasta.pasta.price
            
        for salad in self.salads.all():
            total += salad.salad.price

        for dinner_platter in self.dinner_platters.all():
            if dinner_platter.size == "Small":
                total += dinner_platter.dinner_platter.small_price
            else:
                total += dinner_platter.dinner_platter.large_price

        return total

    def __str__(self):
        return self.user.username

# Create a profile everytime a user instance is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Update the profile everytime its related user instance is edited
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Cart_pizza(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="pizzas")
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE, related_name="cart_pizzas")
    size = models.CharField(max_length=64)
    topping_1 = models.ForeignKey(OrderTopping, on_delete=models.CASCADE, related_name="topping_1_cart_pizzas")
    topping_2 = models.ForeignKey(OrderTopping, on_delete=models.CASCADE, related_name="topping_2_cart_pizzas")
    topping_3 = models.ForeignKey(OrderTopping, on_delete=models.CASCADE, related_name="topping_3_cart_pizzas")
    topping_4 = models.ForeignKey(OrderTopping, on_delete=models.CASCADE, related_name="topping_4_cart_pizzas")

    def __str__(self):
        return f"{self.profile.user.username} added to his cart a {self.size} pizza of ID {self.pizza.id}; contains {self.topping_1} + {self.topping_2} + {self.topping_3} + {self.topping_4}"

def remove_pizza(sender, **kwargs):
    for p in Cart_pizza.objects.all():
        if p.pizza.id == kwargs['instance'].id:
            p.profile.msg = True
            p.delete()
            print(f"\n{p.id} pizza is deleted and the message is ongoing.\n")
            break
        else:
            continue

# Everytime an item is removed from the menu, it is also removed from the cart. Same when it is simply modified (for cart items that may have a size, topping or extra that is not supposed to be selectable anymore)
post_save.connect(remove_pizza, sender=Pizza)
pre_delete.connect(remove_pizza, sender=Pizza)





class Cart_sub(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="subs", null=True)
    sub = models.ForeignKey(Sub, on_delete=models.CASCADE, related_name="cart_subs", null=True)
    extra_1 = models.ForeignKey(OrderExtra, on_delete=models.CASCADE, related_name="extra_1_cart_subs", null=True)
    extra_2 = models.ForeignKey(OrderExtra, on_delete=models.CASCADE, related_name="extra_2_cart_subs", null=True)
    extra_3 = models.ForeignKey(OrderExtra, on_delete=models.CASCADE, related_name="extra_3_cart_subs", null=True)
    extra_4 = models.ForeignKey(OrderExtra, on_delete=models.CASCADE, related_name="extra_4_cart_subs", null=True)
    size = models.CharField(max_length=64)

    def __str__(self):
        return f"\n{self.profile.user.username} added to his cart a {self.size} {self.sub.name} sub; includes {self.extra_1} + {self.extra_2} + {self.extra_3} + {self.extra_4}\n"

def remove_sub(sender, **kwargs):
    for s in Cart_sub.objects.all():
        if s.name == kwargs['instance'].name:
            s.profile.msg = True
            s.delete()
            print(f"\nThe message is ongoing and {s.id} sub is deleted\n")
            break
        else:
            continue

# Everytime an item is removed from the menu, it is also removed from the cart. Same when it is simply modified (for cart items that may have a size, topping or extra that is not supposed to be selectable anymore)
post_save.connect(remove_sub, sender=Sub)
pre_delete.connect(remove_sub, sender=Sub)



class Cart_pasta(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="pasta", null=True)
    pasta = models.ForeignKey(Pasta, on_delete=models.CASCADE, related_name="cart_pastas", null=True)

    def __str__(self):
        return f"{self.profile.user.username} added to his cart a pasta ({self.pasta.name})"

def remove_pasta(sender, **kwargs):
    for p in Cart_pasta.objects.all():
        if p.name == kwargs['instance'].name:
            p.profile.msg = True
            p.delete()
            print(f"The message is ongoing and {p.name} is deleted")
            break
        else:
            continue

# Everytime an item is removed from the menu, it is also removed from the cart. Same when it is simply modified (for cart items that may have a size, topping or extra that is not supposed to be selectable anymore)
post_save.connect(remove_pasta, sender=Pasta)
pre_delete.connect(remove_pasta, sender=Pasta)



class Cart_salad(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="salads", null=True)
    salad = models.ForeignKey(Salad, on_delete=models.CASCADE, related_name="cart_salads", null=True)

    def __str__(self):
        return f"{self.profile.user.username} added to his cart a salad ({self.salad.name})"

def remove_salad(sender, **kwargs):
    for s in Cart_salad.objects.all():
        if s.name == kwargs['instance'].name:
            s.profile.msg = True
            s.delete()
            print(f"\nThe message is ongoing and {s.name} is deleted\n")
            break
        else:
            continue

# Everytime an item is removed from the menu, it is also removed from the cart. Same when it is simply modified (for cart items that may have a size, topping or extra that is not supposed to be selectable anymore)
post_save.connect(remove_salad, sender=Salad)
pre_delete.connect(remove_salad, sender=Salad)



class Cart_dinner_platter(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="dinner_platters", null=True)
    dinner_platter = models.ForeignKey(Dinner_platter, on_delete=models.CASCADE, related_name="cart_dinner_platters", null=True)
    size = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.profile.user.username} added to his cart a {self.size} {self.dinner_platter.name} dinner platter"

def remove_dinner_platter(sender, **kwargs):
    for d in Cart_dinner_platter.objects.all():
        if d.name == kwargs['instance'].name:
            d.profile.msg = True
            d.delete()
            print(f"\nThe message is ongoing and {d.name} is deleted\n")
            break
        else:
            continue

# Everytime an item is removed from the menu, it is also removed from the cart. Same when it is simply modified (for cart items that may have a size, topping or extra that is not supposed to be selectable anymore)
post_save.connect(remove_dinner_platter, sender=Dinner_platter)
pre_delete.connect(remove_dinner_platter, sender=Dinner_platter)



# ----------------------------------- Orders -----------------------------------



class Order(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    timestamp = models.IntegerField()
    price = models.FloatField()
    items = models.CharField(max_length=64) # Django has no field for dictionaries so we turn them into a string instead

    def __str__(self):
        items = json.loads(self.items) # string ---> JSON object
        display = f"Order from {self.first_name} {self.last_name}"
        display += f"\nPlaced on {datetime.datetime.fromtimestamp(self.timestamp).strftime('%B %d, %Y at %H:%M')};"
        display += f"\nPaid amount: ${self.price}\n"
        display += f"\n ------------ "
        display += f"\nOrdered items:"
        for pizza in items["pizzas"]:
            display += f"\n{pizza['size']} {pizza['crust']} {pizza['name']} pizza"
            display += f"\nContains {pizza['topping_1']} + {pizza['topping_2']} + {pizza['topping_3']} + {pizza['topping_4']};\n"
        for sub in items["subs"]:
            display += f"\n{sub['size']} {sub['name']} sub"
            display += f"\nIncludes following extras: {sub['extra_1']} + {sub['extra_2']} + {sub['extra_3']} + {sub['extra_4']};\n"
        for pasta in items['pasta']:
            display += f"\n{pasta['name']};\n"
        for salad in items['salads']:
            display += f"\n{salad['name']};\n"
        for dinner_platter in items['dinner_platters']:
            display += f"\n{dinner_platter['size']} {dinner_platter['name']} dinner platter;"
        return display
