from django.shortcuts import render, redirect,reverse
from carts.models import Cart, CartItem
from .forms import OrderForm
from .models import Payment, Order, OrderProduct
from django.contrib.auth.decorators import login_required
from store.models import Product
from django.http import JsonResponse
import datetime
import json

from django.template.loader import render_to_string
from django.shortcuts import HttpResponse
import uuid
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import requests
import socket
from accounts.models import Account
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from security.models import Qrcode





def payments(request):
    if request.method=='POST':
        order_number=request.POST['order_number']
        payment_id = uuid.uuid4()
        order = Order.objects.get(user=request.user, is_ordered=False, order_number=order_number)

        ordered_products = OrderProduct.objects.filter(order_id=order.id)
        total_product = 0
        for i in ordered_products:
            total_product += i.quantity

        ##ssl
        store_id='yourd637908d6ec03e'
        API_key='yourd637908d6ec03e@ssl'
        mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id,
                                sslc_store_pass=API_key)

        allurl = "http://127.0.0.1:8000/order/test/"+order_number+"/"+str(payment_id)+"/"
        mypayment.set_urls(success_url=allurl, fail_url=allurl,
                           cancel_url=allurl, ipn_url=allurl)

        mypayment.set_product_integration(total_amount=Decimal(order.order_total), currency='BDT', product_category='Mixed',
                                          product_name='demo-product', num_of_item=total_product, shipping_method='Courier',
                                          product_profile='None')

        mypayment.set_customer_info(name=order.first_name, email=order.email, address1=order.address_line_1,
                                    address2=order.address_line_2, city=order.city, postcode=order.pin_code, country='Bangladesh',
                                    phone=order.phone)

        mypayment.set_shipping_info(shipping_to=order.full_name, address=order.address_line_1, city=order.city, postcode=order.pin_code,
                                    country='Bangladesh')

        response_data = mypayment.init_payment()
        print(response_data)

        # Store transaction details inside Payment model
        payment = Payment(
            user=request.user,
            payment_id=payment_id,
            payment_method="sslcommerz",
            amount_paid=str(order.order_total),
            status='unpaid'
        )
        payment.save()

        order.payment = payment
        order.save()

       # Move cart_item to orderProduct.

        cart_items = CartItem.objects.filter(user=request.user)

        for item in cart_items:
            order_product = OrderProduct()
            order_product.order_id = order.id
            order_product.payment = payment
            order_product.user_id = request.user.id
            order_product.product_id = item.product_id
            order_product.quantity = item.quantity
            order_product.product_price = item.product.price
            order_product.ordered = True
            order_product.save()

            cart_item = CartItem.objects.get(id=item.id)
            product_variation = cart_item.variations.all()
            orderproduct = OrderProduct.objects.get(id=order_product.id)
            orderproduct.variations.set(product_variation)
            orderproduct.save()

            # Reduce the quantity of sold products.

            product = Product.objects.get(id=item.product.id)
            product.stock -= item.quantity
            product.save()

        # clear the user cart.

        CartItem.objects.filter(user=request.user).delete()



        return redirect(response_data['GatewayPageURL'])

    else:
        return redirect('store')



@csrf_exempt
def test(request,oid,pid):
    order_number=oid
    payment_id = pid
    order = Order.objects.get(order_number=order_number,is_ordered=False)
    payment=Payment.objects.get(payment_id=payment_id,status='unpaid')
    if request.method == 'POST' or request.method == 'post':
        payment_data=request.POST
        status=payment_data['status']

        if status == 'VALID':
            val_id=payment_data['val_id']
            tran_id=payment_data['tran_id']
            amount=payment_data['amount']
            card_type=payment_data['card_type']
            order.is_ordered = True
            order.save()
            payment.payment_id=tran_id
            payment.status=status
            payment.save()
            return redirect(reverse('order_complete') + '?order_number=' + order_number + '&'
                            + 'payment_id=' + tran_id +'&'+ 'amount=' + amount+'&'+ 'card_type=' + card_type)


        if status == 'FAILED':
            return redirect('ordernotdone')
    return HttpResponse("done")


def orderdone(request):
    # order = Order.objects.filter(user=request.user, is_ordered=False).order_by('-id')[0]
    # order.is_ordered = True
    # order.save()
    return render(request,'orders/order_done.html')

def ordernotdone(request):
    # order = Order.objects.filter(user=request.user, is_ordered=False).order_by('-id')[0]
    # order.delete()
    return render(request, 'orders/order_not_done.html')



def order_complete(request):
    order_number = request.GET.get('order_number')
    transID = request.GET.get('payment_id')
    amount = request.GET.get('amount')
    card_type = request.GET.get('card_type')

    try:
        order = Order.objects.get(order_number=order_number, is_ordered=True)
        ordered_products = OrderProduct.objects.filter(order_id=order.id)

        payment = Payment.objects.get(payment_id=transID)

        sub_total = 0
        for i in ordered_products:
            sub_total += i.product_price * i.quantity

        try:
            description=f"YOUR DAILY GROCERY SECURITY TOKEN FOR {request.user.email} : Order Number={order_number},Transaction id={transID},Amount={amount},Payment System={card_type},Status=VALID"
            qrcode=Qrcode(user=request.user,payment=payment,description=description)
            qrcode.save()
        except:
            pass
        qrc = Qrcode.objects.filter(payment=payment)[0]
        context = {
            'qrc':qrc,
            'order': order,
            'ordered_products': ordered_products,
            'order_number': order.order_number,
            'transID': payment.payment_id,
            'payment': payment,
            'sub_total': sub_total,

        }
        return render(request, 'orders/order_completed.html', context=context)

    except (Payment.DoesNotExist, Order.DoesNotExist):
        return redirect('store')








@login_required(login_url='login')
def place_order(request, total=0, quantity=0):
    current_user = request.user

    # Cart count <= 0, redirect to store.
    cart_items = CartItem.objects.filter(user=current_user)

    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    tax=50
    grand_total = 0


    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity


    grand_total = total + tax

    if request.method == 'POST':
        data = Order()
        data.user = current_user
        data.first_name = request.POST['first_name']
        data.last_name = request.POST['last_name']
        data.phone = request.POST['phone']
        data.email = request.POST['email']
        data.address_line_1 = request.POST['address_line_1']
        data.address_line_2 = request.POST['address_line_2']
        data.pin_code = request.POST['pin_code']
        data.state = request.POST['state']
        data.city = request.POST['city']
        data.order_note = request.POST['order_note']
        data.order_total = grand_total
        data.tax = 50
        data.ip = request.META.get('REMOTE_ADDR')

        data.save()

        # Generate Order Number
        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")  # 20210305
        order_number = current_date + str(data.id)
        data.order_number = order_number
        data.save()

        order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

        context = {
            'order': order,
            'cart_items': cart_items,
            'tax': tax,
            'total': total,
            'grand_total': grand_total,
        }

        return render(request, 'orders/payments.html', context=context)
    else:
        return redirect('checkout')


