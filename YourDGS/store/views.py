from django.shortcuts import render
from django.shortcuts import render,get_object_or_404, redirect
from .models import  Product,ReviewRating
from category.models import Category,SubCategory
from django.db.models import Count
from carts.views import _cart_id
from carts.models import CartItem
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from django.http import HttpResponse
from django.db.models import Q
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def store(request,category_slug=None,subcategory_slug=None):
    products=None
    categories=None
    subcatagoriesname=None
    subcatagories=None

    if request.method=='post' or request.method=='POST':
        value=request.POST['materialExampleRadios']
        start=0
        end=0
        if int(value) == 1:
            start = 0
            end = 1000
        elif int(value)== 2:
            start = 1001
            end = 5000
        elif int(value) == 3:
            start = 5001
            end = 20000
        elif int(value) == 4:
            start = 20001
            end = 100000
        elif int(value) == 5:
            start = 100001
            end = 1000000

        if (category_slug != None) and (subcategory_slug == None):
            categories = get_object_or_404(Category, slug=category_slug)
            subcatagoriesname = SubCategory.objects.filter(category=categories).annotate(product_count=Count('product'))
            products = Product.objects.filter(category=categories, is_available=True,price__range=(start,end)).order_by('?')
            paginator = Paginator(products, 21)
            page = request.GET.get('page')
            products = paginator.get_page(page)

        elif subcategory_slug != None:
            subcatagories = get_object_or_404(SubCategory, slug=subcategory_slug)
            products = Product.objects.filter(subcategory=subcatagories, is_available=True ,price__range=(start,end)).order_by('?')
            categories = get_object_or_404(Category, slug=category_slug)
            subcatagoriesname = SubCategory.objects.filter(category=categories).annotate(product_count=Count('product'))
            paginator = Paginator(products, 21)
            page = request.GET.get('page')
            products = paginator.get_page(page)
        else:
            products = Product.objects.all().filter(is_available=True,price__range=(start,end)).order_by('?')
            paginator = Paginator(products, 21)
            page = request.GET.get('page')
            products = paginator.get_page(page)

        context = {
            'products': products,
            'subcatagoriesname': subcatagoriesname
        }
        return render(request, 'store/home.html', context)
##get
    if(category_slug != None) and (subcategory_slug==None):
        categories=get_object_or_404(Category,slug=category_slug)
        subcatagoriesname=SubCategory.objects.filter(category=categories).annotate(product_count=Count('product'))
        products = Product.objects.filter(category=categories,is_available=True).order_by('?')
        paginator=Paginator(products,21)
        page=request.GET.get('page')
        products=paginator.get_page(page)

    elif subcategory_slug!= None:
        subcatagories = get_object_or_404(SubCategory,slug=subcategory_slug)
        products = Product.objects.filter(subcategory=subcatagories,is_available=True).order_by('?')
        categories=get_object_or_404(Category,slug=category_slug)
        subcatagoriesname=SubCategory.objects.filter(category=categories).annotate(product_count=Count('product'))
        paginator=Paginator(products,21)
        page=request.GET.get('page')
        products=paginator.get_page(page)
    else:
        products=Product.objects.all().filter(is_available=True).order_by('?')
        paginator=Paginator(products,21)
        page=request.GET.get('page')
        products=paginator.get_page(page)

    context={
        'products':products,
        'subcatagoriesname':subcatagoriesname
    }
    return render(request,'store/home.html',context)




def product_detail(request,category_slug=None,subcategory_slug=None,product_id=None):
    try:
        single_product=Product.objects.get(category__slug=category_slug,subcategory__slug=subcategory_slug,id=product_id)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()

    except Exception as e:
        raise e

    reviews = ReviewRating.objects.filter(product_id=single_product.id, status=True)

    context={
        'single_product':single_product,
        'in_cart':in_cart,
        'reviews': reviews,
    }

    return render(request, 'store/product_detail.html',context)


def search(request):
    products = None
    product_count=0

    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('-created_date').filter(Q(product_name__icontains=keyword)) #| Q(description__icontains=keyword)
            product_count=products.count()
            paginator = Paginator(products, 21)
            page = request.GET.get('page')
            products = paginator.get_page(page)
    context={
        'products':products,
        'product_count':product_count

    }

    return render(request,'store/home.html',context)










@login_required(login_url='login')
def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
         #   messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.review = form.cleaned_data['review']
                data.rating = form.cleaned_data['rating']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
            #    messages.success(request, 'Thank you! Your review is live now.')
                return redirect(url)