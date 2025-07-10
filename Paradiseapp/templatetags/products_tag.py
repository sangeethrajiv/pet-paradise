from django import template
from Paradiseapp.models import *

register=template.Library()

@register.simple_tag
def progress_percentage(value,total):
    percent=(value/total)*100
    return percent

@register.simple_tag
def discount_money(original, discount):
    discounted_price = original - (original * discount / 100)
    return int(discounted_price)


@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return None


@register.simple_tag
def calculate_subtotal(cart_items):
    subtotal: int = sum(((item.product.price * (1 - item.product.discount/100)) * item.quantity) for item in cart_items)
    return subtotal


@register.simple_tag
def add_amount(subtotal, amount):
    return subtotal + amount


@register.simple_tag
def calculate_total(cart_items):
    total = sum(
        ((item.product.price * (1 - item.product.discount / 100)) * item.quantity)
        for item in cart_items
    )
    return "{:.2f}".format(total)


@register.simple_tag
def format_decimal(value):
    try:
        formatted_value = "{:.2f}".format(float(value))
        return formatted_value
    except ValueError:
        return value


@register.filter
def apply_discount(price, discount):
    if discount:
        discounted_price = price - (price * discount / 100)
        return f"₹{discounted_price:.2f}"
    else:
        return f"₹{price:.2f}"


@register.filter
def multiply(value, arg):
    return value * arg


@register.simple_tag
def format_cart_items(cart_items, subtotal):
    formatted_items = ""
    for item in cart_items:
        discounted_price = (
            item.product.price * (1 - item.discount / 100) * item.quantity
        )
        formatted_items += (
            f"<li>{item.product.title} x {item.quantity} = ₹{discounted_price:.2f}</li>"
        )
    formatted_items += f"<li><strong>Total: ₹{subtotal:.2f}</strong></li>"
    return formatted_items


@register.filter
def float_to_cents(value):
    return int(float(value) * 100)


@register.simple_tag
def display_quantity(cart_items):
    total_quantity = sum(item.quantity for item in cart_items)
    return total_quantity


# @register.simple_tag
# def total_pet_price(pet_id):
#     try:
#         pet = Pet.objects.get(id=pet_id)
#         total_price = pet.price  # Assuming each pet has a 'price' attribute
#         return total_price
#     except Pet.DoesNotExist:
#         return 0
