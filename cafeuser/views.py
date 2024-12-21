from django.shortcuts import render, redirect,get_object_or_404
from django.urls import reverse


from cafeapp.models import MainItem
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from  .models import Cart, CartItem
from django.contrib import messages
from django.http import Http404
from cafeproject import settings
import stripe
# Create your views here.


def ListMainItem(reqeust):
    item=MainItem.objects.all()
    paginator=Paginator(item,3)
    page_number=reqeust.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.get_page(page_number.num_pages)
    return render(reqeust,'user-temp/product-card.html',{'items':item,'page':page})

def SerchMainItem(request):
    query=None
    items=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        items=MainItem.objects.filter(Q(productName__icontains=query) | Q(price__icontains=query))
    else:
        items=[]
    context={'items':items,
             'query':query
             }
    return  render(request,'user-temp/search-main-item.html',context)





def AddToCart(request,pro_id):
    item=MainItem.objects.get(id=pro_id)
    if item.quantity>0:
        cart,created =Cart.objects.get_or_create(user=request.user)
        cart_item,item_created=CartItem.objects.get_or_create(cart=cart,item=item)
        if not item_created:
            cart_item.quantity+=1
            cart_item.save()
        return redirect('view-cart')



from django.shortcuts import render

def ViewCartUser(request):
    # Get or create the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Fetch all cart items
    cart_items = cart.cartitem_set.select_related('item')  # Optimized query with select_related
    
    # Calculate total price and prepare details
    total_price = 0
    product_details = []
    for cart_item in cart_items:
        item = cart_item.item
        product_details.append({
            'productName': item.productName,
            'id': item.id,
            'description': item.Discription,
            'image': item.image,
            'quantity': cart_item.quantity,
            'price': item.price,
            'subtotal': item.price * cart_item.quantity,  # Subtotal for each item
        })
        total_price += item.price * cart_item.quantity  # Add to total price
    
    total_items = cart_items.count()
    
    # Prepare context
    context = {
        'product_details': product_details,
        'total_price': total_price,
        'total_items': total_items
    }
    return render(request, 'user-temp/cart-user.html', context)







# def IncreaseQuantity(request, item_id):
#     cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)  
#     if cart_item.quantity < cart_item.item.stock: 
#         cart_item.quantity += 1
#         cart_item.save()
#         messages.success(request, "Quantity increased successfully.")
#     else:
#         messages.error(request, "Cannot increase quantity beyond available stock.")
#     return redirect('view-cart')  # Redirect to the cart page


# def DecreaseQuantity(request, item_id):
#     cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
#     if cart_item.quantity > 1: 
#         cart_item.quantity -= 1
#         cart_item.save()
#         messages.success(request, "Quantity decreased successfully.")
#     else:
#         messages.error(request, "Minimum quantity is 1.")
#     return redirect('view-cart')


# def RemoveFromCart(request, pro_id):
#     try:
#         cart_item = CartItem.objects.get(id=pro_id) 
#         print(cart_item)
#         cart_item.delete()
#     except CartItem.DoesNotExist:
#         pass
#     return redirect('view-cart')


# def IncreaseQty(request,item_id):
#     cart_item=CartItem.objects.get(id=item_id)

#     if cart_item.quantity < cart_item.item.quantity:
#         cart_item.quantity += 1
#         cart_item.save()

#     return redirect('view-cart')

# def DecreaseQty(request,item_id):
#     cart_item=CartItem.objects.get(id=item_id)

#     if cart_item.quantity > 1:
#         cart_item.quantity -= 1
#         cart_item.save()

#     return redirect('view-cart')



# def RemoveItem(request, item_id):
#     try:
#         cart_item = CartItem.objects.get(id=item_id)
#         cart_item.delete() 
#     except CartItem.DoesNotExist:
#         raise Http404("Cart item does not exist")


def IncreaseQty(request, product_name):
    try:
        # Find the MainItem using productName
        main_item = MainItem.objects.get(productName=product_name)
        
        # Find the CartItem associated with the user's cart and the MainItem
        cart_item = CartItem.objects.get(cart__user=request.user, item=main_item)
        
        # Check stock limit and increase quantity
        if cart_item.quantity < main_item.quantity:  # Assuming `MainItem.quantity` is the stock count
            cart_item.quantity += 1
            cart_item.save()
        else:
            messages.error(request, "Stock limit reached for this item.")
    except (MainItem.DoesNotExist, CartItem.DoesNotExist):
        raise Http404("Cart item does not exist or is not associated with your cart.")
    return redirect('view-cart')


def DecreaseQty(request, product_name):
    try:
        # Find the MainItem using productName
        main_item = MainItem.objects.get(productName=product_name)
        
        # Find the CartItem associated with the user's cart and the MainItem
        cart_item = CartItem.objects.get(cart__user=request.user, item=main_item)
        
        # Ensure quantity doesn't drop below 1
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            messages.error(request, "Minimum quantity is 1.")
    except (MainItem.DoesNotExist, CartItem.DoesNotExist):
        raise Http404("Cart item does not exist or is not associated with your cart.")
    return redirect('view-cart')



def RemoveItem(request, product_name):
    try:
        # Find the MainItem with the given productName
        main_item = MainItem.objects.get(productName=product_name)

        # Find the CartItem associated with the current user's cart and the MainItem
        cart_item = CartItem.objects.get(cart__user=request.user, item=main_item)
        
        # Delete the CartItem
        cart_item.delete()
        messages.success(request, f"'{product_name}' removed from the cart successfully.")
    except (MainItem.DoesNotExist, CartItem.DoesNotExist):
        raise Http404("Cart item does not exist or is not associated with your cart.")
    return redirect('view-cart')



import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

def CreateCheckout(request):
    cart_items = CartItem.objects.all()
    
    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        if request.method == 'POST':
            line_items = []
            exchange_rate = 0.012  # Example exchange rate (₹1 = $0.012)
            minimum_amount_usd = 0.50  # Minimum amount in USD
            
            for cart_item in cart_items:
                if cart_item.item:
                    # Convert the item price from INR to USD
                    price_in_inr = cart_item.item.price
                    price_in_usd = price_in_inr * exchange_rate
                    
                    # Ensure the price is at least $0.50
                    if price_in_usd < minimum_amount_usd:
                        price_in_usd = minimum_amount_usd
                    
                    # Convert USD to cents (Stripe works in smallest unit, which is cents for USD)
                    price_in_cents = int(price_in_usd * 100)

                    line_item = {
                        'price_data': {
                            'currency': 'inr',  # Keep INR for the actual payment
                            'unit_amount': int(price_in_inr * 100),  # Use INR for unit amount (cents)
                            'product_data': {
                                'name': cart_item.item.productName
                            },
                        },
                        'quantity': 1
                    }
                    line_items.append(line_item)
            
            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('sucsess-url')),
                    cancel_url=request.build_absolute_uri(reverse('cancel'))
                )
                
                return redirect(checkout_session.url, code=303)
  
                    
                    
def Success(request):
    cart_items=CartItem.objects.all()  
    for cart_item in cart_items:
        product=cart_item.item
        if product.quantity>=cart_item.quantity:
            product.quantity-=cart_item.quantity
            product.save()
    cart_items.delete()        
    return render(request,'user-temp/success.html')                
                    
                    
def cancel(request):
    return render(request,'ser-temp/cancel.html') 
                        