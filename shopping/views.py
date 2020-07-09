from django.shortcuts import render, redirect
from .models import Category, Item, PurchasedItems

# Create your views here.
def shopping_page(request):

    items = Item.objects.filter(user=request.user).order_by('item')
    categories = Category.objects.filter(user=request.user)
    
    # Find the categories being used
    categories_used = []
    for item in items:
        if item.category not in categories_used:
            categories_used.append(item.category)

    # Get purchased items
    purchased_items = PurchasedItems.objects.filter(user=request.user).order_by('-item')
    
    # Create a list of favorite items
    favorites = []
    index_deductor = 1

    # Check each item in the database returning the quantity if already in the list or creating a new object if not.
    for index_item, item in enumerate(purchased_items):
        item_dict = {
            'item': item.item,
            'quantity': item.quantity,
        }
        
        try:
            if favorites[index_item - index_deductor]['item'] == item.item:
                favorites[index_item - index_deductor]['quantity'] += item.quantity
                index_deductor += 1
            else:
                favorites.append(item_dict)
        except:
            favorites.append(item_dict)
        
    # sort the favorites by quantity
    favorites = sorted(favorites, key= lambda x: x['quantity'], reverse=True)

    # top five chart data
    all_favorites = favorites
    chart_data_top_five = []
    chart_labels_top_five = []

    for favorite in range(5):
        chart_labels_top_five.append(all_favorites[favorite]['item'])
        chart_data_top_five.append(all_favorites[favorite]['quantity'])

    # all favorites for chart data
    all_favorites = favorites
    chart_data = []
    chart_labels = []

    for favorite in all_favorites:
        chart_labels.append(favorite['item'])
        chart_data.append(favorite['quantity'])
        
    context = {
        'items': items,
        'categories': categories,
        'categories_used': categories_used,
        'purchased_items': purchased_items,
        'favorites': favorites,
        'chart_data_top_five': chart_data_top_five,
        'chart_labels_top_five': chart_labels_top_five,
        'chart_data': chart_data,
        'chart_labels': chart_labels,
    }

    return render(request, 'shopping/shopping_page.html', context)

def update_item(request, operation):

    if request.method == 'POST':
        if operation == 'add':

            item_name = request.POST.get('item')
            quantity = int(request.POST.get('quantity'))
            category = Category.objects.get(category=request.POST.get('category'))

            # Get users items from the database.
            users_items = Item.objects.filter(user=request.user)
            new_item = True

            # If item in database add the quantity instead of creating a new object.
            for item in users_items:
                if item.item == item_name:
                    item_in_database = Item.objects.get(item=item_name)
                    item_in_database.quantity += quantity
                    item_in_database.save()
                    new_item = False
            
            # Add item if new
            if new_item:
                new_item = Item(
                    user = request.user,
                    item = item_name,
                    quantity = quantity,
                    category = category, 
                )
                new_item.save()

            purchase_item = PurchasedItems(
                user = request.user,
                item = item_name,
                quantity = quantity,
                category = category, 
            )
            purchase_item.save()
        
        # Remove items checked by the user
        if operation == 'remove':
            number_of_items = len(request.POST) - 1
            checked_items = 0
            item_pk = 0
            
            # if item has been checked, get the pk and remove the item from the database or add 1 to 
            # item_pk and try again until all checkboxs have been remove.
            while checked_items < number_of_items:
                requested_name = request.POST.get(str(item_pk))
  
                if not requested_name:
                    item_pk += 1
                else:
                    select_item = Item.objects.get(pk=item_pk)
                    select_item.delete()
                    item_pk += 1
                    checked_items += 1

    return redirect('shopping_page')

def quick_item(request, item, category):

    item_name = item
    quantity = 1
    category_selected = Category.objects.get(category=category)

    # Get users items from the database.
    users_items = Item.objects.filter(user=request.user)
    new_item = True

    # If item in database add the quantity instead of creating a new object.
    for item in users_items:
        if item.item == item_name:
            item_in_database = Item.objects.get(item=item_name)
            item_in_database.quantity += quantity
            item_in_database.save()
            new_item = False
    
    # Add item if new
    if new_item:
        new_item = Item(
            user = request.user,
            item = item_name,
            quantity = quantity,
            category = category_selected, 
        )
        new_item.save()

    purchase_item = PurchasedItems(
        user = request.user,
        item = item_name,
        quantity = quantity,
        category = category_selected, 
    )
    purchase_item.save()

    return redirect('shopping_page')

def update_category(request, operation, pk):
    
    if request.method == 'POST':
        if operation == 'add':
            new_category = Category(
                user = request.user,
                category = request.POST.get('category'),
            )
            new_category.save()
        if operation == 'remove':

            category = Category.objects.get(pk=pk)
            category.delete()

    return redirect('shopping_page')