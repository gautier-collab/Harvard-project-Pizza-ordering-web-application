# Harvard-project-Restaurant-online-ordering-platform

Screencast presenting my website: https://youtu.be/wWuUHRiklnw

This is a web application for handling a restaurant’s online orders, built as my Project 3 of the Harvard course CS50's Web Programming with Python and JavaScript (2018 version). Users can browse the restaurant’s menu, add items to their cart, and submit their orders. Meanwhile, the restaurant owners are able to add and update menu items, and view orders that have been placed.

Here are the credentials of the superuser account created for restaurant owners:

- Username: pizzastaff

- Password: ilovepizza

To make the website go live, enter your Stripe live keys at the beginning of app/container-files/app/pizza/settings.py and switch STRIPE_TEST_MODE to False.

You can modify the time zone in app/container-files/app/pizza/settings.py : TIME_ZONE = timezone_of_your_choice

To launch and access the web application, open the pulled repository in your UNIX terminal and run the following command (without "sudo" unless the terminal asks it):
# bash app/run-me.sh
