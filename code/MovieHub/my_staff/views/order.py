from django.shortcuts import render

# Create your views here.
from my_admin.models import Order
from django.core.paginator import Paginator


# browse order information
def index(request, pIndex=1):
    model = Order.objects
    orderList = model.all()
    keyWord = request.GET.get("keyword", None)
    condition = []

    # keyword research
    if keyWord:
        orderList = orderList.filter(movie_name__contains=keyWord)
        condition.append('keyword=' + keyWord)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(orderList, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    orderList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"orderList": orderList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for st in orderList:
        print(st.toDict())
    return render(request, 'my_staff/order/index.html', context)
