from django.shortcuts import render,redirect
from  .models import MainItem
from  .form import MainItemForm
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage
# Create your views here.


def CreateMainItem(request):
    items=MainItem.objects.all()
    if request.method=='POST':
        form=MainItemForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_view')

    else:
        form=MainItemForm()
    return render(request,'admin-temp\create-item-main.html',{'form':form,'items':items})


def ListMainItemAdimn(reqeust):
    item=MainItem.objects.all()
    total_products = MainItem.objects.count()
    paginator=Paginator(item,3)
    page_number=reqeust.GET.get('page')
    try:
        page=paginator.get_page(page_number)
    except EmptyPage:
        page=paginator.get_page(page_number.num_pages)
    return render(reqeust,'admin-temp/product-list.html',{'items':item,'page':page,'total_products': total_products})



    
    
def UpdateMainItem(request,item_id):
    item=MainItem.objects.get(id=item_id)
    if request.method=='POST':
        form=MainItemForm(request.POST,request.FILES,instance=item)
        if form.is_valid():
            form.save()
            return redirect('item-list-admin')

    else:
        form=MainItemForm(instance=item)
    return render(request,'admin-temp/update-main-item.html',{'form':form})    



def DeleteMainItem(reqeust,item_id):
    item = MainItem.objects.get(id=item_id)
    if reqeust.method == 'POST':
        item.delete()
        return redirect('item-list-admin')
    return render(reqeust,'admin-temp/delete-main-item-confiom.html',{'item':item})


def DetailMainItem(reqeust,item_id):
    item=MainItem.objects.get(id=item_id)
    return render(reqeust,'admin-temp/detail-main-item.html',{'item':item})


def SerchMainItemAdmin(request):
    query=None
    items=None
    if 'q' in request.GET:
        query=request.GET.get('q')
        items=MainItem.objects.filter(Q(productName__icontains=query) | Q(price__icontains=query))
    else:
        items=[]
    context={'items':items,
             'query':query}
    return  render(request,'admin-temp/search-main-item-ad.html',context)