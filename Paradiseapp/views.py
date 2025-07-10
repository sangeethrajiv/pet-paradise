import json
import logging
import random

import razorpay
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_GET, require_POST

from .forms import *
from .forms import CustomPasswordChangeForm
from .models import *
from .models import Cart, CartItem, Order, OrderItem, Product, Profile


def home(request):
    if request.user.is_authenticated:
        unread_message_count = Message.objects.filter(
            user=request.user, read=False
        ).count()
        cart_items = CartItem.objects.filter(user=request.user)
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        userprofile = Profile.objects.filter(user=request.user).first()
    else:
        cart_items = []
        subtotal = 0
        unread_message_count = 0
        userprofile = None

    maincategory = MainCategory.objects.all()

    context = {
        "categories": maincategory,
        "subtotal": subtotal,
        "cart_items": cart_items,
        "userprofile": userprofile,
        "unread_message_count": unread_message_count,
    }
    return render(request, "home/home.html", context)


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password = request.POST.get("password1")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        elif userAddress.objects.filter(phone=phone).exists():
            messages.error(request, "Phone number already exists")
        else:
            # Create the user object
            user = User(username=username, email=email)
            user.set_password(password)
            user.save()

            # Create userAddress object
            useradd = userAddress(user=user, phone=phone)
            useradd.save()

            # Success message
            messages.success(
                request,
                f"Welcome, {user.username.upper()} Registered Successfully Please login.",
            )

    return render(request, "user/login.html")  # Adjust your template name accordingly


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(
                request, f" Login Successful  Welcome,{user.username.upper()}"
            )
            return redirect("login")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "user/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successfully.")
    return redirect("home")


def login_required_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "user/login_req.html")


def fetch_unread_count(request):
    if request.user.is_authenticated:
        unread_count = Message.objects.filter(user=request.user, read=False).count()
        return JsonResponse({"unread_count": unread_count})
    return JsonResponse({"unread_count": 0})


@login_required
def messages_page(request):
    if request.user.is_authenticated:
        messages = Message.objects.filter(user=request.user)
        return render(request, "home/messages.html", {"messages": messages})
    else:
        return redirect("login")


def user_validate(request, value, type):
    if type == "phone":
        exists = User.objects.filter(username=value).exists()
    elif type == "email":
        exists = User.objects.filter(email=value).exists()
    else:
        exists = False
    return JsonResponse({"exists": exists})


def about(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/about.html", context)


def contact(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/contact.html", context)


def shop(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)
    else:
        cart_items = []
        total_items = 0

    categories = Category.objects.all()
    products = Product.objects.all()

    context = {
        "products": products,
        "categories": categories,
        "cart_items": cart_items,
        "total_items": total_items,
    }
    return render(request, "shop/shop.html", context)


def pro_details(request, slug):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    context: dict = {"cart_items": cart_items}
    product = get_object_or_404(Product, slug=slug)
    additional_info = Addtional_information.objects.filter(product=product)
    amount_in_cents = int(product.price * 100)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY)
    )
    razorpay_order = client.order.create(
        {"amount": amount_in_cents, "currency": "INR", "payment_capture": "1"}
    )

    context = {
        "product": product,
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount_in_cents": amount_in_cents,
        "razorpay_order_id": razorpay_order["id"],
        "csrf_token": get_token(request),
        "additional_info": additional_info,
        "cart_items": cart_items,
    }

    return render(request, "shop/product_view.html", context)


# @require_POST
# @csrf_exempt  # Temporarily bypass CSRF for demonstration; not recommended for production
# def category_products(request):
#     try:
#         # Parse the JSON data from the request body
#         jsondata = json.loads(request.body.decode("utf-8"))
#         categories = jsondata.get("categories", [])

#         # Fetch products based on the categories
#         if categories:
#             products = Product.objects.filter(category__id__in=categories).distinct()
#         else:
#             products = Product.objects.all()

#         # Determine if there are no products
#         is_error = products.count() == 0

#         # Prepare context for rendering
#         render_context = {
#             "products": products,
#             "is_error": is_error,
#         }

#         # Render the HTML content for the response
#         data = render_to_string("ajax/product-filter.html", render_context)

#         response_data = {"status": "Success", "data": data}

#     except json.JSONDecodeError:
#         # Handle JSON decoding errors
#         response_data = {"status": "Error", "message": "Invalid JSON data"}
#     except Product.DoesNotExist:
#         # Handle cases where no products are found
#         response_data = {"status": "Error", "message": "Products not found"}
#     except Exception as e:
#         # Handle any other unexpected errors
#         response_data = {"status": "Error", "message": str(e)}

#     return JsonResponse(response_data)


@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 1)
        # Debug print statement to check values
        # print(f"Product ID: {product_id}, Quantity: {quantity}")

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return redirect("cart")
    return redirect("shop")


@login_required
def shop_add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 1)
        # Debug print statement to check values
        # print(f"Product ID: {product_id}, Quantity: {quantity}")

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return redirect("shop")
    return redirect("shop")


@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = request.POST.get("quantity", 1)
        # Debug print statement to check values
        # print(f"Product ID: {product_id}, Quantity: {quantity}")

        product = get_object_or_404(Product, id=product_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, defaults={"quantity": quantity}
        )
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()

        return redirect("cart")
    return redirect("shop")


@login_required
def carty(request):
    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = 0
    for item in cart_items:
        subtotal += item.product.price * item.quantity

    quantity = sum(item.quantity for item in cart_items)
    return render(
        request,
        "cart/cart.html",
        {"cart_items": cart_items, "subtotal": subtotal, "quantity": quantity},
    )


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(
        user=request.user, purchased=False
    )  # Adjust filtering as per your model structure
    total_items = cart_items.count()
    context = {
        "cart_items": cart_items,
        "total_items": total_items,
    }
    return render(request, "cart/cart.html", context)


@csrf_exempt
@login_required
def update_cart_item(request, item_id):
    if request.method == "POST":
        data = json.loads(request.body)
        quantity = data.get("quantity", 1)
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


@csrf_exempt
@login_required
def remove_from_cart(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
        cart_item.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def cart_count(request):
    if request.user.is_authenticated:
        cart_count = CartItem.objects.filter(user=request.user).count()
    else:
        cart_count = 0
    return {"cart_count": cart_count}


@login_required
def cart_data(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        subtotal = sum(item.product.price * item.quantity for item in cart_items)
        cart_items_data = [
            {
                "product": {"name": item.product.name, "price": item.product.price},
                "quantity": item.quantity,
            }
            for item in cart_items
        ]
        response = {
            "cart_count": len(cart_items),
            "cart_items": cart_items_data,
            "subtotal": subtotal,
        }
    else:
        response = {
            "cart_count": 0,
            "cart_items": [],
            "subtotal": 0,
        }
    return JsonResponse(response)


@login_required
def checkout(request):
    if request.user.is_authenticated:
        cart_itemss = CartItem.objects.filter(user=request.user)
    else:
        cart_itemss = []

    cart_items = CartItem.objects.filter(user=request.user)
    subtotal = sum(
        ((item.product.price * (1 - item.product.discount / 100)) * item.quantity)
        for item in cart_items
    )
    quantity = sum(item.quantity for item in cart_items)
    return render(
        request,
        "cart/check.html",
        {
            "cart_items": cart_items,
            "subtotal": subtotal,
            "quantity": quantity,
            "cart_itemss": cart_itemss,
        },
    )
    # Retrieve all cart items for the logged-in user


@login_required
def checkoutpet(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    if request.method == "POST":
        pet_id = request.POST.get("pet_id")
        pet_type = request.POST.get("pet_type")
        pet = get_object_or_404(Pet, id=pet_id)
        pets = Pet.objects.all()

        # Process the selected payment type or other logic here
        # For demonstration, let's assume you are redirecting to a success page
        return render(
            request,
            "cart/checkoutpet.html",  # Replace with your success template
            {
                "pet": pet,
                "pet_type": pet_type,
                "pets": pets,
                "cart_items": cart_items,
            },  # Pass necessary data to success page
        )

    # Redirect to petshop if the request method is not POST
    return redirect("petshop")


@login_required
def checkbuy(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))
        product = get_object_or_404(Product, id=product_id)

        total_amounts = product.price

        return render(
            request,
            "cart/checkbuy.html",
            {
                "product": product,
                "quantity": quantity,
                "total_price": total_amounts,
                "cart_items": cart_items,
            },
        )
    return redirect("shop")


# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))


@csrf_exempt
@login_required
def place_order_checkout(request):
    if request.method == "POST":
        try:
            current_user = request.user

            # Retrieve user details (if not already available)
            if not current_user.first_name:
                current_user.first_name = request.POST.get("fname")
                current_user.last_name = request.POST.get("lname")
                current_user.save()

            # Create an order instance
            new_order = Order(
                user=current_user,
                fname=request.POST.get("fname"),
                lname=request.POST.get("lname"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                address=request.POST.get("address"),
                state=request.POST.get("state"),
                city=request.POST.get("city"),
                pincode=request.POST.get("pincode"),
                payment_mode=request.POST.get("payment_mode"),
                payment_status="Success",
                status="Ready For Shipment",
                razorpay_order_id=request.POST.get("order_id"),
                razorpay_payment_id=request.POST.get("razorpay_payment_id"),
                payment_id=request.POST.get("razorpay_payment_id"),
            )

            # Retrieve the user's cart items
            cart_items = CartItem.objects.filter(user=current_user)
            if not cart_items.exists():
                messages.error(request, "No items in the cart.")
                return redirect("/checkout/")

            # Calculate total price of items in the cart
            cart_total_price = sum(
                (
                    (item.product.price * (1 - item.product.discount / 100))
                    * item.quantity
                )
                for item in cart_items
            )

            # Assign total price and amount to the new order
            new_order.total_price = cart_total_price
            new_order.amount = cart_total_price

            # Generate a unique tracking number for the order
            trackno = "petparadise" + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = "petparadise" + str(random.randint(1111111, 9999999))
            new_order.tracking_no = trackno

            # Save the new order instance
            new_order.save()

            # Create OrderItem instances for each item in the cart
            for item in cart_items:
                discounted_price = item.product.price * (
                    1 - (item.product.discount / 100)
                )
                OrderItem.objects.create(
                    order=new_order,
                    product=item.product,
                    price=discounted_price,
                    quantity=item.quantity,
                )

                # Decrease quantity from available stock
            new_order.update_product_availability()

            # Clear the user's cart items
            cart_items.delete()

            # Display success message and redirect to homepage
            messages.success(request, "Your Order has been placed successfully")
            return redirect("/")

        except Exception as e:
            # Print the error for debugging purposes
            print(f"Error placing order: {e}")
            messages.error(
                request, "There was an issue placing your order. Please try again."
            )
            return redirect("/checkout/")

    # If the request method is not POST, redirect to checkout
    return redirect("/checkout/")


@login_required
@csrf_exempt
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()
            messages.success(request, "Your appointment has been booked successfully!")
            return redirect("home")
    else:
        form = AppointmentForm()
    return render(request, "home/home.html", {"form": form})


@login_required
def razorpaycheck(request):
    cart = CartItem.objects.filter(user=request.user)
    total_price = sum(
        ((item.product.price * (1 - item.product.discount / 100)) * item.quantity)
        for item in cart
    )

    return JsonResponse({"total_price": total_price})


# Utility function to calculate total price
def calculate_total_price(user):
    cart = CartItem.objects.filter(user=user)
    total_price = sum(
        ((item.product.price * (1 - item.product.discount / 100)) * item.quantity)
        for item in cart
    )
    return total_price


# View to proceed to pay
@login_required
def proceed_to_pay(request):
    if request.method == "GET":
        total_price = calculate_total_price(request.user)
        return JsonResponse({"total_price": total_price})
    else:
        return JsonResponse({"error": "Invalid request method"})


def calculate_total_prices(user):
    products = Product.objects.filter(user=user)
    total_price = sum(product.price for product in products)
    return total_price


@require_GET
def proceed_to_pay_view(request):
    if request.method == "GET":
        # Fetch a single product, for example, the first product in the database
        product = Product.objects.first()
        if product:
            effective_price = product.price - (product.price * product.discount / 100)
            response_data = {"total_prices": effective_price}
        else:
            response_data = {"error": "No product found"}
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})


@csrf_exempt
def order_success(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        address = request.POST.get("address")
        state = request.POST.get("state")
        city = request.POST.get("city")
        pincode = request.POST.get("pincode")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        razorpay_payment_id = request.POST.get("razorpay_payment_id")

        try:
            # Update order status or create a new order
            order = Order.objects.create(
                fname=fname,
                lname=lname,
                address=address,
                state=state,
                city=city,
                pincode=pincode,
                phone=phone,
                email=email,
                payment_id=razorpay_payment_id,
                status="Ready For Shipment",
            )

            # Redirect to the success page
            return redirect("order-success")
        except Exception as e:
            print(f"Error creating order: {e}")
            messages.error(
                request, "There was an issue processing your order. Please try again."
            )
            return redirect("checkout")
    else:
        return render(request, "cart/ordersuccess.html")


@csrf_exempt
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("order_id")
        razorpay_signature = request.POST.get("razorpay_signature")

        # Verify the payment signature
        # Implement Razorpay's signature verification

        # Update the order status
        order = Order.objects.get(id=order_id)
        order.status = "Ready For Shipment"
        order.save()

        return redirect("/order-success/")
    else:
        return redirect("/checkout/")


@login_required
def myorders(request, t_no):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    # Retrieve the specific order using the tracking number and the authenticated user
    order = Order.objects.filter(tracking_no=t_no, user=request.user).first()
    # Retrieve the order items for the specified order
    order_items = OrderItem.objects.filter(order=order)

    # Calculate the total price of the order
    total_price = sum(item.price * item.quantity for item in order_items)

    context = {
        "order": order,
        "order_items": order_items,
        "total_price": total_price,
        "cart_items": cart_items,
    }

    return render(request, "shop/myorders.html", context)


@login_required
def order_list(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    # Get a specific order by ID
    products = Product.objects.all()
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    context = {
        "orders": orders,
        "product": products,
        "cart_items": cart_items,
    }
    # Render the order details page
    return render(request, "shop/orderslist.html", context)


def petbreed(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/petbreed.html", context)


def petadopt(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/petadopt.html", context)


logger = logging.getLogger(__name__)


def search_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)
        cart_count = cart_items.count()
    else:
        cart_items = []
        total_items = 0
        cart_count = 0

    query = request.GET.get("q", "").strip()
    logger.debug(f"Search query: '{query}'")  # Use logging for debugging

    if query:
        # Adjust the query to filter by title and tags
        products = Product.objects.filter(
            Q(title__icontains=query) | Q(tags__icontains=query)
        ).distinct()
    else:
        products = Product.objects.none()

    context = {
        "products": products,
        "query": query,
        "cart_count": cart_count,
        "cart_items": cart_items,
        "total_items": total_items,
    }

    return render(request, "shop/search.html", context)


def shophome(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)
        cart_count = cart_items.count()
    else:
        cart_items = []
        total_items = 0
        cart_count = 0

    context = {
        "cart_count": cart_count,
        "cart_items": cart_items,
        "total_items": total_items,
    }

    return render(request, "shop/shophome.html", context)


# def petshop(request):
#     if request.user.is_authenticated:
#         cart_items = CartItem.objects.filter(user=request.user)
#         total_items = sum(item.quantity for item in cart_items)
#         cart_count = cart_items.count()
#     else:
#         cart_items = []
#         total_items = 0
#         cart_count = 0

#     # Assign pets a default value outside the if-else block
#     pets = Pet.objects.all()

#     context = {
#         "cart_count": cart_count,
#         "cart_items": cart_items,
#         "total_items": total_items,
#         "pets": pets,
#     }
#     return render(request, "shop/pets/petshop.html", context)


def petsdetails(request, pet_id):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    pet = get_object_or_404(Pet, id=pet_id)
    pet_images = pets_additional_image.objects.filter(pet=pet)
    pets_additional_images = pets_additional_image.objects.all()
    petz = Pet.objects.all()

    context = {
        "pet": pet,
        "pet_images": pet_images,
        "additional_images": pets_additional_images,
        "petz": petz,
        "cart_items": cart_items,
    }
    return render(request, "shop/pets/petsdetails.html", context)


logger = logging.getLogger(__name__)


@login_required
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Calculate total price for the product
    total_price = product.price

    # Initialize Razorpay client
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY)
    )

    try:
        # Create a Razorpay order
        razorpay_order = client.order.create(
            {
                "amount": int(total_price * 100),
                "currency": "INR",
                "payment_capture": "1",
            }
        )

        # Create an order instance
        new_order = Order(
            user=request.user,
            product=product,
            total_price=total_price,
            amount=total_price,
            payment_mode="Razorpay",
            status="Pending",
            razorpay_order_id=razorpay_order["id"],
        )
        # Generate a unique tracking number for the order
        trackno = "petparadise" + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = "petparadise" + str(random.randint(1111111, 9999999))
        new_order.tracking_no = trackno

        # Save the new order instance
        new_order.save()

        # Create OrderItem instance for the product
        OrderItem.objects.create(
            order=new_order,
            product=product,
            price=total_price,
            quantity=1,  # Since it's a buy now, quantity is 1
        )

        # Display success message and redirect to orders list
        messages.success(
            request, f"Your order for {product.name} has been placed successfully!"
        )
        return redirect("order-success")  # Adjust this to your order success URL

    except Exception as e:
        # Handle any errors during order creation
        messages.error(request, f"There was an error processing your order: {str(e)}")
        return redirect("shop")


@login_required
def place_order_buynow(request, product_id):
    if request.method == "POST":
        try:
            # Get the current user
            current_user = request.user

            # Retrieve user details (if not already available)
            if not current_user.first_name:
                current_user.first_name = request.POST.get("fname")
                current_user.last_name = request.POST.get("lname")
                current_user.save()

            # Retrieve product and quantity from POST request
            product = get_object_or_404(Product, id=product_id)
            quantity = int(request.POST.get("quantity", 1))

            # Calculate total price of the product after discount
            total_price = (
                product.price - (product.price * product.discount / 100)
            ) * quantity

            # Initialize Razorpay client
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY)
            )

            # Create a Razorpay order
            razorpay_order = client.order.create(
                {
                    "amount": int(total_price * 100),
                    "currency": "INR",
                    "payment_capture": "1",
                }
            )

            # Create an order instance
            new_order = Order(
                user=current_user,
                fname=request.POST.get("fname"),
                lname=request.POST.get("lname"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                address=request.POST.get("address"),
                state=request.POST.get("state"),
                city=request.POST.get("city"),
                pincode=request.POST.get("pincode"),
                payment_mode=request.POST.get("payment_mode"),
                payment_status="Success",
                status="Ready For Shipment",
                razorpay_order_id=razorpay_order["id"],
                razorpay_payment_id=request.POST.get("razorpay_payment_id"),
                payment_id=request.POST.get("razorpay_payment_id"),
                total_price=total_price,
                amount=total_price,
            )

            # Generate a unique tracking number for the order
            trackno = "petparadise" + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = "petparadise" + str(random.randint(1111111, 9999999))
            new_order.tracking_no = trackno

            # Save the new order instance
            new_order.save()

            # Create an OrderItem instance
            OrderItem.objects.create(
                order=new_order,
                product=product,
                price=product.price,
                quantity=quantity,
            )

            # Decrease quantity from available stock
            new_order.update_product_availability()

            # Display success message and redirect to order success page
            messages.success(request, "Your order has been placed successfully")
            return redirect("order-success")

        except Exception as e:
            # Handle exceptions and errors
            print(f"Error placing order: {e}")
            messages.error(
                request, "There was an issue placing your order. Please try again."
            )
            return redirect("checkbuy")

    # Handle GET requests or unexpected cases with a redirect
    return redirect("checkbuy")


@login_required
def place_order_petbuy(request, pet_id):
    if request.method == "POST":
        try:
            # Get the current user
            current_user = request.user

            # Retrieve user details (if not already available)
            if not current_user.first_name:
                current_user.first_name = request.POST.get("fname")
                current_user.last_name = request.POST.get("lname")
                current_user.save()

            # Retrieve pet and quantity from POST request
            pet = get_object_or_404(Pet, id=pet_id)
            quantity = int(request.POST.get("quantity", 1))

            total_price = pet.price * quantity

            # Initialize Razorpay client
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY)
            )

            # Create a Razorpay order
            razorpay_order = client.order.create(
                {
                    "amount": int(total_price * 100),
                    "currency": "INR",
                    "payment_capture": "1",
                }
            )

            # Create an order instance
            new_order = Order(
                user=current_user,
                fname=request.POST.get("fname"),
                lname=request.POST.get("lname"),
                email=request.POST.get("email"),
                phone=request.POST.get("phone"),
                address=request.POST.get("address"),
                state=request.POST.get("state"),
                city=request.POST.get("city"),
                pincode=request.POST.get("pincode"),
                payment_mode=request.POST.get("payment_mode"),
                payment_status="Success",
                status="Ready For Shipment",
                razorpay_order_id=razorpay_order["id"],
                razorpay_payment_id=request.POST.get("razorpay_payment_id"),
                payment_id=request.POST.get("razorpay_payment_id"),
                total_price=total_price,
                amount=total_price,
            )

            # Generate a unique tracking number for the order
            trackno = "petparadise" + str(random.randint(1111111, 9999999))
            while Order.objects.filter(tracking_no=trackno).exists():
                trackno = "petparadise" + str(random.randint(1111111, 9999999))
            new_order.tracking_no = trackno

            # Save the new order instance
            new_order.save()

            # Create an OrderItem instance
            OrderItem.objects.create(
                order=new_order,
                pet=pet,
                price=pet.price,
                quantity=quantity,
            )

            # Decrease quantity from available stock
            pet.quantity -= quantity
            pet.save()

            # Display success message and redirect to order success page
            messages.success(request, "Your order has been placed successfully")
            return redirect("order-success")

        except Exception as e:
            # Handle exceptions and errors
            print(f"Error placing order: {e}")
            return redirect("checkpet")

    # Handle GET requests or unexpected cases with a redirect
    return redirect("checkpet")


def check(request):
    return render(request, "cart/check.html")


@login_required
def checkpet(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []

    if request.method == "POST":
        pet_id = request.POST.get("pet_id")
        pet_type = request.POST.get("pet_type")
        pet = get_object_or_404(Pet, id=pet_id)
        pets = Pet.objects.all()

        # Process the selected payment type or other logic here
        # For demonstration, let's assume you are redirecting to a success page
        return render(
            request,
            "cart/checkoutpet.html",  # Replace with your success template
            {
                "pet": pet,
                "pet_type": pet_type,
                "pets": pets,
                "cart_items": cart_items,
            },  # Pass necessary data to success page
        )

    # Redirect to petshop if the request method is not POST
    return redirect("petshop")


def proceed_to_paypetbuy(request):
    if request.method == "GET" and request.is_ajax():
        try:
            pet_id = request.GET.get("pet_id")
            quantity = int(request.GET.get("quantity", 1))

            pet = get_object_or_404(Pet, id=pet_id)
            total_price = pet.price * quantity

            return JsonResponse({"total_pricee": total_price})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    related_products = Product.objects.filter(category=product.category).exclude(
        id=product.id
    )[
        :5
    ]  # Example logic for related products
    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "related_products": related_products,
        },
    )


def petshop(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)
        cart_count = cart_items.count()
    else:
        cart_items = []
        total_items = 0
        cart_count = 0

    query = request.GET.get("q", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    categories = request.GET.getlist("species")
    breeds = request.GET.getlist("breeds")
    genders = request.GET.getlist("genders")
    locations = request.GET.getlist("locations")
    petss = Pet.objects.all()
    logger.debug(f"Search query: '{query}'")  # Use logging for debugging

    # Base query
    filter_conditions = Q()
    if query:
        filter_conditions &= Q(name__icontains=query) | Q(tags__icontains=query)

    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            filter_conditions &= Q(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass  # Handle invalid price inputs gracefully

    if categories:
        filter_conditions &= Q(category__in=categories)
    if breeds:
        filter_conditions &= Q(breed__in=breeds)
    if genders:
        filter_conditions &= Q(gender__in=genders)
    if locations:
        filter_conditions &= Q(location__in=locations)

    pets = Pet.objects.filter(filter_conditions).distinct()

    context = {
        "pets": pets,
        "query": query,
        "cart_count": cart_count,
        "cart_items": cart_items,
        "total_items": total_items,
        "min_price": min_price,
        "max_price": max_price,
        "selected_categories": categories,
        "selected_breeds": breeds,
        "selected_genders": genders,
        "selected_locations": locations,
        "petss": petss,
    }

    return render(request, "shop/pets/petshop.html", context)


def search_pet(request):
    query = request.GET.get("q", "")
    min_price = request.GET.get("min_price", 0)
    max_price = request.GET.get("max_price", 1000)
    categories = request.GET.getlist("category")
    breeds = request.GET.getlist("breed")
    genders = request.GET.getlist("gender")
    locations = request.GET.getlist("location")

    # Filtering logic
    pets = Pet.objects.filter(
        name__icontains=query,
        price__gte=min_price,
        price__lte=max_price,
        category__in=categories,
        breed__in=breeds,
        gender__in=genders,
        location__in=locations,
    )

    context = {"pets": pets, "query": query}
    return render(request, "shop/petshop.html", context)


def petadoption(request):

    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        total_items = sum(item.quantity for item in cart_items)
        cart_count = cart_items.count()
    else:
        cart_items = []
        total_items = 0
        cart_count = 0

    # Assign pets a default value outside the if-else block
    pets = Petadopt.objects.all()

    context = {
        "cart_count": cart_count,
        "cart_items": cart_items,
        "total_items": total_items,
        "pets": pets,
    }
    return render(request, "shop/pets/petadoption.html", context)


def adoption_view(request, slug):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    pet = get_object_or_404(Petadopt, slug=slug)
    pet_images = petsadopt_additional_image.objects.filter(pet=pet)
    pets_additional_images = petsadopt_additional_image.objects.all()
    petz = Petadopt.objects.all()

    context = {
        "pet": pet,
        "pet_images": pet_images,
        "additional_images": pets_additional_images,
        "petz": petz,
        "cart_items": cart_items,
    }
    return render(request, "shop/pets/adoptionview.html", context)


@csrf_exempt
def adoption_request_send(request, pet_id):
    if request.method == "POST":
        try:
            # Extract form data from request
            fullname = request.POST.get("fullname")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            appointment_date = request.POST.get("appointment_date")
            species = request.POST.get("species")
            breed = request.POST.get("breeds")
            pet_id = request.POST.get("pet_id")
            comment = request.POST.get("comment")

            # Create a new AdoptionRequest object
            adoption_request = AdoptionRequest(
                fullname=fullname,
                email=email,
                phone=phone,
                appointment_date=appointment_date,
                species=species,
                breed=breed,
                pet_id=pet_id,
                comment=comment,
            )
            # Save the object to the database
            adoption_request.save()

            # Return success response
            return JsonResponse({"success": True, "redirect_url": "/"})
        except ValidationError as e:
            # Handle validation errors
            return JsonResponse(
                {"success": False, "errors": {"form": [{"message": str(e)}]}}
            )
        except Exception as e:
            # Handle other unexpected errors
            return JsonResponse(
                {
                    "success": False,
                    "errors": {"form": [{"message": "An unexpected error occurred"}]},
                }
            )


def adoptionrequest(request, slug):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    pet = get_object_or_404(Petadopt, slug=slug)
    return render(
        request, "shop/pets/adoptionreq.html", {"pet": pet, "cart_items": cart_items}
    )


def blog(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/pages/blog.html", context)


def faq(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/pages/faq.html", context)


def teamdetails(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/pages/teamdetails.html", context)


def ourteam(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/pages/ourteam.html", context)


def gallery(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/pages/gallery.html", context)


def ourblog(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        cart_items = []
    context: dict = {"cart_items": cart_items}
    return render(request, "home/pages/ourblog.html", context)


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(
                request, user
            )  # Important: Keeps the user logged in after changing the password
            messages.success(request, "Your password was successfully updated!")
            return redirect("home")  # Redirect to home or another appropriate page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "home/pages/changepassword.html", {"form": form})


def complete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.status == Order.SUCCESS:
        with transaction.atomic():
            for item in order.orderitem_set.all():
                product = item.product
                if product:
                    product.available -= item.quantity
                    product.save()
