from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Category
from .forms import CategoryForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category-list.html', {'categories': categories})

# Create a new category
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category:list')
    else:
        form = CategoryForm()
    return render(request, 'category-create.html', {'form': form})

# Update an existing category
def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return redirect('category:list')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category:list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category-update.html', {'form': form, 'category': category})

# Delete a category
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return redirect('category:list')

    if request.method == 'POST':
        category.delete()
        return redirect('category:list')
    return render(request, 'category-delete.html', {'category': category})