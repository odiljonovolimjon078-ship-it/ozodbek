from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
    
    context = {
        'products': products,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)