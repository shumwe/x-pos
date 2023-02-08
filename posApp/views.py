from pickle import FALSE
from django.urls import reverse
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from posApp.models import Category, Products, Sales, salesItems, ProductReturns, Notify, TrustedCustomerProfile
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json, sys
from datetime import date, datetime
from posApp.forms import ReturnsForm, AddCustomerForm
from django.views.generic import DeleteView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Login
def login_user(request):
    logout(request)
    resp = {"status":'failed','msg':''}
    username = ''
    password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp['status']='success'
            else:
                resp['msg'] = "Incorrect username or password"
        else:
            resp['msg'] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp),content_type='application/json')

#Logout
def logoutuser(request):
    logout(request)
    return redirect('/')

def customers(request):
    customers = TrustedCustomerProfile.objects.all()
    if request.method == "POST":
        add_form = AddCustomerForm(request.POST)
        if add_form.is_valid():
            add_form.save()
            messages.success(request, "Customer waas added")
            return HttpResponseRedirect("")
    else:
        add_form = AddCustomerForm()
    context = {
        "add_form": add_form,
        "customers": customers,
    }
    return render(request, "posApp/customers.html", context)

def edit_cusomer(request, slug):
    customer = TrustedCustomerProfile.objects.get(slug=slug)
    if request.method == "POST":
        edit_form = AddCustomerForm(request.POST, instance=customer)
        if edit_form.is_valid():
            edit_form.save()
            messages.success(request, "Customer updated")
            return redirect("customers")
    else:
        edit_form = AddCustomerForm(instance=customer)

    return render(request, "posApp/edit_customer.html", context={"edit_form": edit_form, "customer": customer})

def customer_history(request, slug):
    customer = TrustedCustomerProfile.objects.get(slug=slug)
    sales_history = Sales.objects.filter(customer__slug=customer.slug)
    sales_items_products = salesItems.objects.filter(sale_id__in=sales_history).distinct().order_by('-created')

    context = {
        "items_history": sales_items_products,
        "customer": customer
    }
    return render(request, "posApp/customer_history.html", context)


class CustomerDeleteView(DeleteView):
    model = TrustedCustomerProfile
    template_name = 'posApp/delete_customer.html'
    context_object_name = "customer"

    def get_success_url(self):
        return reverse("customers")

# Create your views here.
@login_required
def home(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")
    categories = len(Category.objects.all())
    products = len(Products.objects.all())
    transaction = len(Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ))
    today_sales = Sales.objects.filter(
        date_added__year=current_year,
        date_added__month = current_month,
        date_added__day = current_day
    ).all()
    total_sales = sum(today_sales.values_list('grand_total', flat=True))
    context = {
        'page_title':'Home',
        'categories' : categories,
        'products' : products,
        'transaction' : transaction,
        'total_sales' : total_sales,
    }
    return render(request, 'posApp/home.html',context)


#Categories
@login_required
def category(request):
    category_list = Category.objects.all()
    # category_list = {}
    context = {
        'page_title':'Category List',
        'category':category_list,
    }
    return render(request, 'posApp/category.html',context)

@login_required
def manage_category(request):
    category = {}
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id= data['id']
        if id.isnumeric() and int(id) > 0:
            category = Category.objects.filter(id=id).first()
    
    context = {
        'category' : category
    }
    return render(request, 'posApp/manage_category.html',context)

@login_required
def save_category(request):
    data =  request.POST
    resp = {'status':'failed'}
    try:
        if (data['id']).isnumeric() and int(data['id']) > 0 :
            save_category = Category.objects.filter(id = data['id']).update(name=data['name'], description = data['description'],status = data['status'])
        else:
            save_category = Category(name=data['name'], description = data['description'],status = data['status'])
            save_category.save()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully saved.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_category(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Category.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Category Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

# Products
@login_required
def products(request):
    product_list = Products.objects.all()
    context = {
        'page_title':'Product List',
        'products':product_list,
    }
    return render(request, 'posApp/products.html',context)
    
@login_required
def manage_products(request):
    product = {}
    categories = Category.objects.filter(status = 1).all()
    if request.method == 'GET':
        data =  request.GET
        id = ''
        if 'id' in data:
            id = data['id']
        if id.isnumeric() and int(id) > 0:
            product = Products.objects.filter(id=id).first()
    
    context = {
        'product' : product,
        'categories' : categories
    }
    return render(request, 'posApp/manage_product.html',context)

@login_required
def add_to_stock(request, product_id):
    prod = Products.objects.get(id=product_id)

    if request.method == "POST":
        data = request.POST
        number_to_add = int(request.POST["plus_number"])
        prod.product_count += number_to_add
        prod.save()
        messages.error(request, "Product count updated")
        return redirect("product-page")
   
    context = {
        "prod": prod
    }
    return render(request, "posApp/add_to_sock.html", context)


@login_required
def save_product(request):
    data =  request.POST

    if "product_image" in request.FILES:
        product_image = request.FILES['product_image']
        if product_image:
            fs = FileSystemStorage()
            filename = fs.save(product_image.name, product_image)
            uploaded_file_url = fs.url(filename)
    else:
        uploaded_file_url = "default-image.jpg"

    resp = {'status':'failed'}
    id= ''
    if 'id' in data:
        id = data['id']
    if id.isnumeric() and int(id) > 0:
        check = Products.objects.exclude(id=id).filter(code=data['code']).all()
    else:
        check = Products.objects.filter(code=data['code']).all()
    if len(check) > 0 :
        resp['msg'] = "Product Code Already Exists in the database"
    else:
        category = Category.objects.filter(id = data['category_id']).first()
        try:
            if (data['id']).isnumeric() and int(data['id']) > 0 :
                save_product = Products.objects.filter(id = data['id']).update(code=data['code'], 
                category_id=category, name=data['name'], description = data['description'], 
                buying_price = float(data['buying_price']), price = float(data['price']),status = data['status'], minimum_stock=data['minimum_stock'],
                product_count=data['product_count'], measurement_units=data['measurement_units'], bought_count=data['bought_count'], image=uploaded_file_url)
            else:
                save_product = Products(code=data['code'], category_id=category, name=data['name'], 
                description = data['description'], buying_price = float(data['buying_price']), price = float(data['price']),status = data['status'], minimum_stock=data['minimum_stock'],
                product_count=data['product_count'], measurement_units=data['measurement_units'], bought_count=data['bought_count'], image=uploaded_file_url)
                save_product.save()
            resp['status'] = 'success'
            messages.success(request, 'Product Successfully saved.')
        except:
            resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def delete_product(request):
    data =  request.POST
    resp = {'status':''}
    try:
        Products.objects.filter(id = data['id']).delete()
        resp['status'] = 'success'
        messages.success(request, 'Product Successfully deleted.')
    except:
        resp['status'] = 'failed'
    return HttpResponse(json.dumps(resp), content_type="application/json")

@login_required
def pos(request):
    _customers = TrustedCustomerProfile.objects.all()
    products = Products.objects.filter(status=1)
    product_json = []
    for product in products:
        product_json.append({'id':product.id, 'name':product.name, 'price':float(product.price)})
        
    context = {
        'page_title' : "Point of Sale",
        'products' : products,
        'customers': _customers,
        'product_json' : json.dumps(product_json)
    }
    return render(request, 'posApp/pos.html',context)

@login_required
def checkout_modal(request):
    grand_total = 0
    if 'grand_total' in request.GET:
        grand_total = request.GET['grand_total']

    context = {
        'grand_total' : grand_total,
    }
    return render(request, 'posApp/checkout.html', context)

@login_required
def save_pos(request):
    resp = {'status':'failed','msg':''}
    data = request.POST
    pref = datetime.now().year + datetime.now().year
    i = 1
    while True:
        code = '{:0>5}'.format(i)
        i += int(1)
        check = Sales.objects.filter(code = str(pref) + str(code)).all()
        if len(check) <= 0:
            break
    code = str(pref) + str(code)

    try:
        sales = Sales(code=code, sub_total = data['sub_total'], tax = data['tax'], tax_amount = data['tax_amount'], 
            grand_total = data['grand_total'], tendered_amount = data['tendered_amount'], 
            amount_change = data['amount_change'])
        try:
            customer_id = int(request.POST.get('customer'))
            customer = TrustedCustomerProfile.objects.get(id=customer_id)
            sales.customer = customer
            sales.save()
        except:
            sales.save()

        sale_id = Sales.objects.last().pk
        i = 0
        for prod in data.getlist('product_id[]'):
            product_id = prod 
            sale = Sales.objects.filter(id=sale_id).first()
            product = Products.objects.filter(id=product_id).first()
            qty = data.getlist('qty[]')[i] 

            if int(qty) <= product.product_count:
                product.product_count -= int(qty)
                product.save()

            price = data.getlist('price[]')[i]
            total = float(qty) * float(price)
            print({'sale_id' : sale, 'product_id' : product, 'qty' : qty, 'price' : price, 'total' : total})
            salesItems(sale_id = sale, product_id = product, qty = qty, price = price, total = total).save()
            i += int(1)
        resp['status'] = 'success'
        resp['sale_id'] = sale_id
        messages.success(request, "Sale Record has been saved.")
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp),content_type="application/json")

@login_required
def salesList(request):
    sales = Sales.objects.all()
    first_sale = Sales.objects.filter().first()
    last_sale = Sales.objects.filter().last()
    sale_data = []
    for sale in sales:
        data = {}
        for field in sale._meta.get_fields(include_parents=False):
            if field.related_model is None:
                data[field.name] = getattr(sale,field.name)
        data['items'] = salesItems.objects.filter(sale_id = sale).all()
        data['item_count'] = len(data['items'])
        if 'tax_amount' in data:
            data['tax_amount'] = format(float(data['tax_amount']),'.2f')
        # print(data)
        sale_data.append(data)
    # print(sale_data)
    context = {
        'page_title':'Sales Transactions',
        'sale_data':sale_data,
        'first_sale': first_sale,
        'last_sale': last_sale,
    }
    # return HttpResponse('')
    return render(request, 'posApp/sales.html',context)

@login_required
def receipt(request):
    id = request.GET.get('id')
    sales = Sales.objects.filter(id = id).first()
    transaction = {}
    for field in Sales._meta.get_fields():
        if field.related_model is None:
            transaction[field.name] = getattr(sales,field.name)
    if 'tax_amount' in transaction:
        transaction['tax_amount'] = format(float(transaction['tax_amount']))
    ItemList = salesItems.objects.filter(sale_id = sales).all()
    context = {
        "transaction" : transaction,
        "salesItems" : ItemList
    }

    return render(request, 'posApp/receipt.html',context)
    # return HttpResponse('')

@login_required
def delete_sale(request):
    resp = {'status':'failed', 'msg':''}
    id = request.POST.get('id')
    try:
        delete = Sales.objects.filter(id = id).delete()
        resp['status'] = 'success'
        messages.success(request, 'Sale Record has been deleted.')
    except:
        resp['msg'] = "An error occured"
        print("Unexpected error:", sys.exc_info()[0])
    return HttpResponse(json.dumps(resp), content_type='application/json')

@login_required
def returns(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")

    user_returns = ProductReturns.objects.filter(
        created__year=current_year,
        created__month = current_month,
        created__day = current_day
    )
    user_returns_total = len(user_returns)
    products = Products.objects.all()

    if request.method == "POST":
        return_form = ReturnsForm(request.POST)
        if return_form.is_valid():
            product = return_form.cleaned_data["product"]
            prod = Products.objects.get(id=product.id)
            prod.product_count += return_form.cleaned_data["return_quantity"]
            prod.save()
            return_form.save()
            messages.success(request, "Return completed!")
            return HttpResponseRedirect("#success-return")
    else:
        return_form = ReturnsForm()

    context = {
        "user_returns": user_returns,
        "user_returns_total": user_returns_total,
        "return_form": return_form,
        "products": products,
    }
    return render(request, "posApp/reconsile.html", context)

@login_required
def notify(request):
    products = Products.objects.all()
    low_stock_products = []
    nots = Notify.objects.filter(resolved=False)
    if products:
        for prod in products:
            if prod.is_low_stock:
                    low_stock_products.append(prod)
                    check_if_exists = Notify.objects.filter(product__code=prod.code, resolved=False)
                    if check_if_exists:
                        pass
                    else:
                        Notify.objects.create(
                            title=f"{prod.name} is out of stock", product=prod
                        )
                        messages.info(request, f"{prod.name}: is running low in stock")

    context = {
        "low_stock_products": low_stock_products,
        "nots": nots,
    }
    return render(request, "posApp/notify.html", context)

@login_required
def overall_profis_and_loss(request):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    current_day = now.strftime("%d")

    sold_items_year = salesItems.objects.filter(created__year=current_year)    
    # year
    total_sales_year = 0
    buying_cost_year = 0
    sold_product_count_year = 0
    profit_and_loss_year = 0

    if len(sold_items_year) > 0:
        for item in sold_items_year:
            product = Products.objects.get(id=item.product_id.id)
            total_sales_year += ((item.price)*(item.qty))
            sold_product_count_year += (item.qty)
            buying_cost_year += (product.buying_price)*(item.qty)
        profit_and_loss_year = (total_sales_year - buying_cost_year)

    # month
    sales_items_month = salesItems.objects.filter(created__year=current_year, created__month = current_month)
    total_sales_month = 0
    buying_cost_month = 0
    sold_product_count_month = 0
    profit_and_loss_month = 0

    if len(sales_items_month) > 0:
        for item in sales_items_month:
            product = Products.objects.get(id=item.product_id.id)
            total_sales_month += ((item.price)*(item.qty))
            sold_product_count_month += (item.qty)
            buying_cost_month += (product.buying_price)*(item.qty)
        profit_and_loss_month = (total_sales_month - buying_cost_month)

    # today
    sales_items_today = salesItems.objects.filter(created__year=current_year, created__month=current_month, created__day=current_day)
    total_sales_today = 0
    buying_cost_today = 0
    sold_product_count_today = 0
    profit_and_loss_today = 0

    if len(sales_items_today) > 0:
        for item in sales_items_month:
            product = Products.objects.get(id=item.product_id.id)
            total_sales_today += ((item.price)*(item.qty))
            sold_product_count_today += (item.qty)
            buying_cost_today += (product.buying_price)*(item.qty)
        profit_and_loss_today = (total_sales_today - buying_cost_today)

    context = {
        "profit_and_loss_year": profit_and_loss_year, "total_sales_year": total_sales_year, "sold_product_count_year": sold_product_count_year,
        "profit_and_loss_month": profit_and_loss_month, "total_sales_month": total_sales_month, "sold_product_count_month": sold_product_count_month,
        "profit_and_loss_today": profit_and_loss_today, "total_sales_today": total_sales_today, "sold_product_count_today": sold_product_count_today
    }
    return render(request, "posApp/overall_profit_margins.html", context)

@login_required
def product_profit_margins(request, product_id):
    now = datetime.now()
    current_year = now.strftime("%Y")
    current_month = now.strftime("%m")
    # current_day = now.strftime("%d")

    product = Products.objects.get(id=product_id)
    sold_items = salesItems.objects.filter(product_id__id=product.id,)
    total_sales = 0
    buying_cost = 0
    profit_margin = 0
    sold_products_count = 0

    if len(sold_items) > 0:
        for item in sold_items:
            total_sales += ((item.price)*(item.qty))
            sold_products_count += (item.qty)

        buying_cost = (product.buying_price * sold_products_count)
        profit_margin = (total_sales - buying_cost)
    else:
        pass

    context = {
        "product": product,
        "sold_items": sold_items,
        "total_sales": total_sales,
        "profit_margin": profit_margin,
        "sold_products_count": sold_products_count
    }
    return render(request, "posApp/profit_margins.html", context)