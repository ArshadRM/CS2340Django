from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from movies.models import Movie
from cart.models import Order, Item
from .utils import calculate_cart_total
from django.contrib.auth.decorators import login_required

def index(request):
    active_cart_selection = request.session.get('active_cart', '1')
    cart_name = f'cart_{active_cart_selection}'
    cart = request.session.get(cart_name, {})
    movie_ids = list(cart.keys())

    movies_in_cart = []
    cart_total = 0
    if movie_ids:
        movies_in_cart = Movie.objects.filter(id__in=movie_ids)
        cart_total = calculate_cart_total(cart, movies_in_cart)

    template_data = {
        'title': 'Cart',
        'movies_in_cart': movies_in_cart,
        'cart_total': cart_total,
        'active_cart': int(active_cart_selection),
    }
    return render(request, 'cart/index.html', {'template_data': template_data})

def add(request, id):
    get_object_or_404(Movie, id=id)
    cart_selection = request.POST.get('cart_selection', '1')
    cart_name = f'cart_{cart_selection}'
    cart = request.session.get(cart_name, {})
    cart[id] = request.POST['quantity']
    request.session[cart_name] = cart

    # Set the active cart
    request.session['active_cart'] = cart_selection
    return redirect('cart.index')

def view_cart(request, cart_id):
    request.session['active_cart'] = str(cart_id)
    return redirect('cart.index')

def clear(request):
    active_cart_selection = request.session.get('active_cart', '1')
    cart_name = f'cart_{active_cart_selection}'
    request.session[cart_name] = {}
    return redirect('cart.index')

@login_required
def purchase(request):
    active_cart_selection = request.session.get('active_cart', '1')
    cart_name = f'cart_{active_cart_selection}'
    cart = request.session.get(cart_name, {})
    movie_ids = list(cart.keys())

    if (movie_ids == []):
        return redirect('cart.index')
    
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    order = Order()
    order.user = request.user
    order.total = cart_total
    order.save()

    for movie in movies_in_cart:
        item = Item()
        item.movie = movie
        item.price = movie.price
        item.order = order
        item.quantity = cart[str(movie.id)]
        item.save()

    request.session[cart_name] = {}
    template_data = {}
    template_data['title'] = 'Purchase confirmation'
    template_data['order_id'] = order.id
    return render(request, 'cart/purchase.html', {'template_data': template_data})