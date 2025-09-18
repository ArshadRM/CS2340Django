from django import template

register = template.Library()

@register.filter(name='get_quantity')
def get_cart_quantity(cart, movie_id):
    return cart.get(str(movie_id), 0) if cart else 0

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)