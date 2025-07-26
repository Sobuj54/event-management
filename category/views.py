from django.shortcuts import render, redirect
from .models import Category
from .forms import CategoryForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.views.generic import ListView
from django.utils.decorators import method_decorator


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()

@user_passes_test(is_organizer)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category-list.html', {'categories': categories})


@method_decorator(user_passes_test(is_organizer), name='dispatch')
class CategoryListView(ListView):
    model = Category
    template_name = "category-list.html"
    context_object_name = "categories"


# Create a new category
@user_passes_test(is_organizer)
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully.")
            return redirect('category:list')
    else:
        form = CategoryForm()
    return render(request, 'category-create.html', {'form': form})

# Update an existing category
@user_passes_test(is_organizer)
def category_update(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return redirect('category:list')

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('category:list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category-update.html', {'form': form, 'category': category})

# Delete a category
@user_passes_test(is_organizer)
def category_delete(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return redirect('category:list')

    if request.method == 'POST':
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('category:list')
    return render(request, 'category-delete.html', {'category': category})