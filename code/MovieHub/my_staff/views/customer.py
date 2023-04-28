from django.shortcuts import render

# Create your views here.
from my_admin.models import Customer
from django.core.paginator import Paginator


# browse customer information
def index(request, pIndex=1):
    model = Customer.objects
    customerList = model.all()
    keyWord = request.GET.get("keyword", None)
    condition = []

    # keyword research
    if keyWord:
        customerList = customerList.filter(name__contains=keyWord)
        condition.append('keyword=' + keyWord)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(customerList, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    customerList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"customerList": customerList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for st in customerList:
        print(st.toDict())
    return render(request, 'my_staff/customer/index.html', context)
