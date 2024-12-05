from datetime import datetime
import random
from django.http import HttpResponse
from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView,DeleteView
from .forms import PetForm , ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import decorator_from_middleware
from django.views.decorators.cache import never_cache,cache_control
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from .forms import UpdateUserForm
from django.db.models import Q 
# Create your views here.

@never_cache
def index(request):
    category=Category.objects.all()
    if category:
       return render(request,'index.html',{'category':category})
    else:
       return render(request,'index.html')


def login_page(request):  
    if request.method == 'POST':
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        print("$$$$$$$$$$$$$$$", uname)
        print("&&&&&&&&&&&&7&", passw)
        user = User.objects.filter(username=uname, password=passw).first()
        print("%%%%%%%%%%%%%%%%%%%%%%%%", user)

        try: 
            if user.is_admin:
                return redirect('adm_home')
            elif user.is_shop:
                print("user id :-------------------------->", user.id)
                request.session['user_id'] = user.id
                return redirect('shop_home')
            else:
                messages.error(request, 'Invalid login credentials.')
                return render(request, 'administrator/login.html', {'username': uname})
        except:
            messages.error(request, 'Invalid login credentials.')
            return render(request, 'administrator/login.html', {'username': uname})
                
    return render(request, "administrator/login.html")

def logout(request):  
    request.session.flush()
    return redirect('index')

def view_pets_products(request,category_id):
    category = Category.objects.get(id=category_id)
    pets = Pet.objects.filter(category=category)
    products = Products.objects.filter(category=category)
    
    context = {
        'category': category,
        'pets': pets,
        'products': products
    }
    
    return render(request, 'user/view_pets_products.html', context)

# /////////////////////////// ADMIN ///////////////////////////////////

def adm_home(request):
    return render(request,'administrator/base.html')

def manage_users(request):
    user=User.objects.filter(is_user=True)
    return render(request, "administrator/manage_user.html",{'user': user})

def manage_sellers(request):
    user=User.objects.filter(is_seller=True)
    return render(request, "administrator/manage_user.html",{'user': user})

def manage_shop(request):
    user=User.objects.filter(is_shop=True)
    return render(request, "administrator/manage_user.html",{'user': user})

def manage_expert(request):
    user=User.objects.filter(is_expert=True)
    return render(request, "administrator/manage_user.html",{'user': user})

def delete_user(request,pk):
    user=User.objects.get(pk=pk)
    if user.is_expert:
        user.delete()
        messages.error(request, 'Delete Successfully Completed.')
        return redirect('manage_expert')
     
    elif user.is_shop:
        user.delete()
        messages.error(request, 'Delete Successfully Completed.')
        return redirect('manage_shop')
     
    elif user.is_user:
        user.delete()
        messages.error(request, 'Delete Successfully Completed.')
        return redirect('manage_users')
     
    elif user.is_seller:
        user.delete()
        messages.error(request, 'Delete Successfully Completed.')
        return redirect('manage_sellers')
    
def view_pets_category(request):
    category=Category.objects.all()

    return render(request,"user/view_pets_category.html",{"category":category})

def add_category(request): 
    cate=Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        if Category.objects.filter(name__iexact=name).exists():
            messages.error(request, f"The category '{name}' already exists.")
        else:
          category=Category.objects.create(
          
            name=name,
        
          )
          category.save()
          messages.success(request,'Successfully added')
          return redirect('add_category')
    context={
        'cate':cate
    }
    return render(request, "administrator/add_category.html",context)

def delete_category(request,pk):
    boys=Category.objects.get(pk=pk)
    boys.delete()
    messages.error(request, 'Delete Successfully Completed.')
    return redirect('add_category')

     
# ///////////////////////////////////////////// SHOP //////////////////////////////////////

def shop_register(request):
    if request.method == "POST":
        uname = request.POST.get("username")
        passw1 = request.POST.get("Password")
        passw2= request.POST.get("Password1")
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        address = request.POST.get("address")
        
        if passw1 ==passw2:
            if User.objects.filter(username=uname).exists():
                messages.error(request, 'Username already exists.')
                return render(request, 'shop/shop_register.html')
            else:
                user = User.objects.create(
                    username=uname,
                    password=passw1,
                    name=name,
                    mobile=phone,
                    email=email,
                    Address=address,
                    is_shop=True,
                )
                user.save()
                # Add a success message
                messages.success(request, 'Registration successful.')
                return redirect('index')
        else:
            messages.error(request, 'password not matching.')
            return render(request,"shop/shop_register.html", {
                'username': uname,
                'name':name,
                'email': email,
                'phone':phone,
                'address':address,
            })
    else:
        return render(request, "shop/shop_register.html")
    
def shop_home(request): #staff here adds pets stocks and details
    print(request.path)
    categories = list(Category.objects.all().values_list('name', flat=True) ) # Fetch all categories
    pets = Pet.objects.all()  # Fetch all pets from the database
    if request.method == "POST":
        form = PetForm(request.POST, request.FILES)  # Form for adding a new pet
        if form.is_valid():
            form.save()  # Save the pet to the database
            return redirect('shop_home')  # Redirect to the same page after saving
    else:
        form = PetForm()

    context = {
        'form': form,
        'pets': pets,
        'categories': categories
    }
    return render(request,'shop/home.html',context)

def add_product(request):
    products= Products.objects.filter(SHOP_id=request.session['user_id'])
    if request.method == 'POST':
       form = ProductForm(request.POST, request.FILES) 
       if form.is_valid():
            f=form.save(commit=False) 
            f.SHOP = User.objects.get(id=request.session['user_id']) 
            f.save()
            return redirect('add_product')
    else:
        form = PetForm()
    context = {
        'form': form,
        'products': products,
        
    }

    return render(request,'shop/add_product.html',context)


class ProductUpdateView(UpdateView):
    model = Products
    fields = ['name', 'category', 'pic', 'price', 'description', 'stock_level']
    template_name = 'shop/product_update.html'
    success_url = reverse_lazy('add_product')

class ProductDeleteView(DeleteView):
    model = Products
    template_name = 'shop/product_confirm_delete.html'
    success_url = reverse_lazy('add_product')

def view_pets(request):
    view_pets=Pet.objects.all()

    return render(request,'user/view_pets.html',{'view_pets': view_pets}) 

def view_products(request):
    view_products=Products.objects.all()

    return render(request,'user/view_products.html',{'view_products':view_products})   

def view_product_order(request):
    obj = BookingDetails.objects.filter(PRODUCT__SHOP_id=request.session['user_id'])
    return render(request, "shop/view_product_order.html", {'orders': obj})

def delete_order(request, order_id):
    obj = BookingDetails.objects.get(id=order_id)
    obj.delete()
    return HttpResponse('''<script>alert("order removed successfully"); window.location="/view_product_order"</script>''')

def deliver_order(request, order_id):
    obj = BookingDetails.objects.get(id=order_id)
    obj.Status = "Delivered"
    obj.save()
    return HttpResponse('''<script>alert("order Delivered successfully"); window.location="/view_product_order"</script>''')

# /////////////////////////////////// ///////////////////////////////////////////


def search(request):
    query = request.GET.get('query', '')  # Get the search term from the request
    print(query)
    categorys =Category.objects.all()
    c_query=query
    for i in categorys:
        # print(i)
        i=i.name
        no_spaces = ''.join(i.split())
        if no_spaces.lower() == ''.join(query.split()).lower():
           c_query=i
        # print("hello",c_query)
        # print(no_spaces.lower())
    category=Category.objects.filter(name__iexact=c_query).first()
    print(category)
    product_results = []
    pet_results = []
    error_message = "" 
    if query:
        # Search in the Product model (e.g., name or description)
        pet_results = Pet.objects.filter(
            Q(name__iexact=query) | Q(category=category.id if category else None)
        )
        
        if not pet_results.exists():  # Search in the Category model (e.g., title)
            product_results = Products.objects.filter(
                              Q(name__iexact=query) | Q(category=category.id if category else None)
                            )
        if not product_results and not pet_results:
               error_message = "No pets or products found for your search."

    context = {
        'product_results': product_results,
        'pet_results': pet_results,
        'query': query,
        'error_message': error_message,
    }
    print(pet_results)
    return render(request, 'user/search.html', context)



def search1(request):
    query = request.GET.get('query', '')  # Get the search term from the request
    print(query)
    categorys =Category.objects.all()
    c_query=query
    for i in categorys:
        # print(i)
        i=i.name
        no_spaces = ''.join(i.split())
        if no_spaces.lower() == ''.join(query.split()).lower():
           c_query=i
        # print("hello",c_query)
        # print(no_spaces.lower())
    category=Category.objects.filter(name__iexact=c_query).first()
    print(category)
    product_results = []
    pet_results = []
    error_message = "" 
    if query:
        # Search in the Product model (e.g., name or description)
        pet_results = Pet.objects.filter(
            Q(name__iexact=query) | Q(category=category.id if category else None)
        )
        
        if not pet_results.exists():  # Search in the Category model (e.g., title)
            product_results = Products.objects.filter(
                              Q(name__iexact=query) | Q(category=category.id if category else None)
                            )
        if not product_results and not pet_results:
               error_message = "No pets or products found for your search."

    context = {
        'product_results': product_results,
        'pet_results': pet_results,
        'query': query,
        'error_message': error_message,
    }
    print(pet_results)
    return render(request, 'staff/search1.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType


@login_required
def add_to_cart(request, item_type, item_id):
    # Determine whether the item is a Product or a Pet
    if item_type == 'product':
        content_type = ContentType.objects.get_for_model(Products)
        item = get_object_or_404(Products, id=item_id)
    elif item_type == 'pet':
        content_type = ContentType.objects.get_for_model(Pet)
        item = get_object_or_404(Pet, id=item_id)
    else:
        return redirect('view_cart')  # Invalid type

    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        content_type=content_type,
        object_id=item.id
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('view_cart')

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {
        'cart': cart,
        'cart_items': cart.cart_items.all(),
        'total_price': cart.total_price(),
    }
    return render(request, 'user/cart.html', context)
   

def increment_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

def decrement_cart_item(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect('view_cart')   

def checkout_view(request):
    if request.method == "POST":
        # Handle your payment processing logic here
        cart = Cart.objects.get(user=request.user)  # Assuming each user has one cart
        print(cart)
        # Clear all cart items for the user's cart
        CartItem.objects.filter(cart=cart).delete()
        messages.success(request, "Checkout successful! Your cart has been cleared.")
        return redirect('view_cart')  # Redirect to cart or a success page

    return render(request, 'user/checkout.html')


def pet_booking(request, pet_id):
    pet_obj = Pet.objects.get(id=pet_id)
    print("&&&&&&&&&&&&&&&&&&&&", pet_obj)
    return render(request, "user/pet_booking.html", {'pet': pet_obj})

def manage_booking(request):
    booking_details = BookingDetails.objects.all()
    return render(request, "administrator/manage_booking.html", {'bookings': booking_details})

def cancel_booking(request, booking_id):
    booking_obj = BookingDetails.objects.get(id=booking_id)
    booking_obj.Status = "cancelled"
    booking_obj.save()
    return HttpResponse('''<script>alert("Cancelled"); window.location="/manage_booking"</script>''')


def assign_booking(request, booking_id):
    booking_obj = BookingDetails.objects.get(id=booking_id)
    request.session['booking_id'] = booking_id
    boy = User.objects.filter(is_boy=True)
    return render(request, "administrator/assign_delivery.html", {'booking': booking_obj, 'delivery_boys': boy})


def assign_delivery(request):
    boy_id = request.POST['delivery_boy']
    booking_id = request.POST['booking_id']
    booking_obj = BookingDetails.objects.get(id=booking_id)
    booking_obj.Status = "Assigned"
    booking_obj.save()
    asssign_obj = AssignTable()
    asssign_obj.BOY = User.objects.get(id=boy_id)
    asssign_obj.BOOKING = BookingDetails.objects.get(id=booking_id)
    asssign_obj.Status = "Assigned"
    asssign_obj.Comments = "Nill"
    asssign_obj.save()
    return HttpResponse('''<script>alert("Assigned"); window.location="/manage_booking"</script>''')



# ////////////////////////////////////// delivery boy ///////////////////////////////////////


def deliveryboy_home(request):
    return render(request, "deliveryboy/home.html")

def view_order(request):
    obj = AssignTable.objects.all()
    return render(request, "deliveryboy/view_order.html",{'orders': obj})

def update_delivery(request, assign_id):
    request.session['assign_id']=assign_id
    return render(request, "deliveryboy/update_delivery.html")

def update_order_status(request):
    status = request.POST['status']
    delivery_comments = request.POST['delivery_comments']
    assign_obj = AssignTable.objects.get(id=request.session['assign_id'])
    assign_obj.Status = status
    assign_obj.Comments = delivery_comments
    assign_obj.save()
    return HttpResponse('''<script>alert("Status updated"); window.location="/view_order"</script>''')

def generate_account_details(request):
    accntnumber = ""
    key = ""
    ifsc = ""
    list_of_chars = "1234567890"
    accntnumber_length = 11
    key_length = 3
    for i in range(accntnumber_length):
        accntnumber += random.choice(list_of_chars)
    for i in range(key_length):
        key += random.choice(list_of_chars)
    ifsc = "SBTR000055"
    amt = "500000"
    account_details = {
        'account_number': accntnumber,
        'key': key,
        'IFSC': ifsc,
        'amount': amt,
    }
    account_obj = memberaccount()
    account_obj.member = User.objects.get(id=request.session['u_id'])
    account_obj.account_number = accntnumber
    account_obj.key = key
    account_obj.IFSC = ifsc
    account_obj.amount = amt
    account_obj.save()
    messages.success(request, 'Registration successful.')
    return HttpResponse('''<script>alert("Registration successful."); window.location="/cus_login"</script>''')


def payment_page(request):
    request.session['total_price'] = request.POST['total_price']
    request.session['product_id'] = request.POST['product_id']
    request.session['quantity'] = request.POST['quantity']
    total = request.POST['total_price']
    print("^^^^^^^^^^^^^^^6", request.POST)
    print("$$$$$$$$$$$$$$$", total)
    account_obj = memberaccount.objects.get(member_id=request.session['user_id'])
    return render(request, "user/payment.html", {'account_obj': account_obj, 'total': total})


def booking(request):
    print("%%%%%%%%%%",request.POST)
    user_lid = request.session['user_id']
    product_id = request.session['product_id']
    quantity = request.session['quantity']
    print(request.POST, "=================================")
    print(product_id, "PPPPPPPPPPPPPPPPPPPPPPP")
    print(quantity, "qqqqqqqqqqqqqqqqqqqqqqq")
    print(user_lid, "lllllllllllllllllllllllll")
    p_ob = Pet.objects.get(id=product_id)
    quant = 0
    if quantity.strip():  # Check if the string is not empty after stripping whitespace
        quant = int(quantity)
    else:
        # Handle the case where quantity is empty, e.g., set a default value or show an error message
        print("Error: Quantity is empty.")
        # You may also want to return or raise an exception depending on your application's logic.
    tt = int(p_ob.price) * quant
    print(tt, "price=====================tt========")
    stock = p_ob.stock_level
    print(stock, "SSSSSSSSSSSSSSSSSSSSSSSSS")
    quant = 0
    if quantity.strip():  # Check if the string is not empty after stripping whitespace
        quant = int(quantity)
    else:
        # Handle the case where quantity is empty, e.g., set a default value or show an error message
        print("Error: Quantity is empty.")
        # You may also want to return or raise an exception depending on your application's logic.

    no_stock = int(stock) - int(quant)
    print(no_stock, "OOOOOOOOOOOOOOOOOOOO")
    if stock >= quant:
        up = Pet.objects.get(id=product_id)
        up.stock_level = no_stock
        up.save()
        q = BookingTable.objects.filter(USER_id=user_lid, Status='booked')

        if len(q) == 0:
            print("%%%%%%%%%%%%%%%%%%%%%$444444444444444")
            obe = BookingTable()
            obe.Total = tt
            obe.Status = 'Paid'
            obe.Date = datetime.now().strftime("%Y-%m-%d")
            obe.USER = User.objects.get(id=user_lid)
            obe.save()
            obe1 = BookingDetails()
            obe1.Quantity = quantity
            obe1.BOOK = obe
            obe1.Status = 'booked'
            obe1.PET = up
            obe1.save()
            return HttpResponse('''<script>alert("Booked"); window.location="/cus_home"</script>''')
        else:
            total = int(p_ob.price) + int(tt)
            print(total, "KKKKKKKKKKKKKKKK")

            obr = BookingTable.objects.get(id=q[0].id)
            obr1 = BookingDetails()
            obr1.Quantity = quantity
            obr1.BOOK = obr
            obr1.PET = up
            obr1.Status = "booked"
            obr1.save()
            return HttpResponse('''<script>alert("Booked"); window.location="/cus_home"</script>''')
    else:
        return HttpResponse('''<script>alert("out of stock"); window.location="/cus_home"</script>''')


def view_account(request):
    return render(request, "user/view_account.html")

def payment(request):
    user_id = request.session['user_id']
    accountdetails = memberaccount.objects.filter(member=user_id).first()
    key1=accountdetails.key
    amount = request.POST['amount']
    account_balane=accountdetails.amount
    if request.method == 'POST':
        if accountdetails:
            key=request.POST['key']
            if key==key1:
                amount = request.POST['amount']
                if float(account_balane) >= float(amount):
                    new_balance = float(account_balane) - float(amount)  # Convert amount to float
                    accountdetails.amount = new_balance
                    accountdetails.save()
                    # Use the correct parameter name when redirecting
                    return HttpResponse('''<script>alert("Paid successfully."); window.location="/booking"</script>''')
                else:
                    return HttpResponse("Insufficient balance")
            else:
                    return HttpResponse('''<script>alert("PIN number incorrect"); window.location="/cus_home"</script>''')
        else:
            return HttpResponse("Account details not found")    
    return HttpResponse('''<script>alert("Value error"); window.location="/cus_home"</script>''')


def view_payments(request):
    booking_obj = BookingDetails.objects.filter(BOOK__Status="Paid")
    print("&&&&&&&&&&&&&&&&", booking_obj)
    return render(request, "administrator/view_payments.html", {'payments': booking_obj})


def view_bookings(request):
    booking_obj = BookingDetails.objects.filter(BOOK__USER_id=request.session['user_id'])
    print("^^^^^^^^^^^^^^", booking_obj)
    return render(request, "user/view_bookings.html",{'bookings': booking_obj })