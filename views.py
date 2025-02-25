from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib import messages
from .forms import RegistrationForm
from .models import Account
from django.shortcuts import render, get_object_or_404
from .models import MedicationInfo, Category,Cart, CartItem,Order,OrderItem
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful! You can now log in.")
            return render(request,'login.html')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegistrationForm()

    return render(request, 'reg.html', {'form': form})

def ulogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            request.session['password'] = user.password
            return redirect('myapp:profile')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'login.html')

def ulogout(request):
    request.session.flush()
    messages.success(request, "You have successfully logged out.")
    return render(request,'logout.html')


def home(request):
    username = request.session.get('username', 'Guest')
    return render (request, 'home.html', {'username': username})

def profile(request):
    if 'user_id' not in request.session:  
        messages.warning(request, "You need to log in to view your profile.")
        return redirect('myapp:login')

    user_id = request.session['user_id'] 
    try:
        user = Account.objects.get(id=user_id)  
    except Account.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('myapp:login') 
    return render(request, 'profile.html', {'user': user})

def category_list(request):
    categories = Category.objects.all()  
    return render(request, 'category_list.html', {'categories': categories})

def medication_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    medications = MedicationInfo.objects.filter(category=category) 
    return render(request, 'medication_list.html', {'category': category, 'medications': medications})

def medication_detail(request, medication_id):
    medication = get_object_or_404(MedicationInfo, id=medication_id)
    return render(request, 'medication_details.html', {'medication': medication})

def search_category(request):
    query=request.GET.get('r','')
    data=Category.objects.filter(name__icontains=query) if query else None
    return render(request,'search.html',{'data':data})

@login_required
def add_to_cart(request, medication_id):
    product = get_object_or_404(MedicationInfo, id=medication_id)
    
    # Get or create the cart for the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Get or create the cart item
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Updated quantity of {product.name} in your cart.")
    else:
        messages.success(request, f"Added {product.name} to your cart.")
    
    return redirect('myapp:view_cart')

@login_required
def view_cart(request):
    cart = Cart.objects.filter(user=request.user).first()
    total_quantity = 0
    if cart:
        total_quantity = sum(item.quantity for item in cart.items.all())
    
    return render(request, 'cart.html', {
        'cart': cart,
        'total_quantity': total_quantity,
    })

@login_required(login_url='login')
def create_order(request):
    cart = CartItem.object.filter(user=request.user)
    
    if cart:
        total_price = sum(item.menu.item_price * item.quantity for item in cart)
        order = Order.objects.create(user=request.user,total_price=total_price)
        
        for item in cart:
            OrderItem.objects.create(order=order,product=item.menu,quantity=item.quantity)
        
        cart.delete()
    else:
        return redirect('/medication_list/')
    return redirect('order_detail',order_id=order.id)


@login_required
def order_detail(request, order_id):
    # Retrieve the order for the logged-in user
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Render the order details page with the order
    return render(request, 'order_detail.html', {'order': order})


@login_required(login_url='login')
def order_list(request):
    orders = Order.objects.filter(user=request.user)  # Filter orders for the logged-in user
    return render(request, 'order_list.html', {'orders': orders})
