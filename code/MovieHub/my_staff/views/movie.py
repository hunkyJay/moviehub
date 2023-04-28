import random

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from my_admin.models import Movie
from django.core.paginator import Paginator
from datetime import datetime
import hashlib
import string


# browse staff information
def index(request, pIndex=1):
    model = Movie.objects
    movieList = model.all()
    keyWord = request.GET.get("keyword", None)
    condition = []

    # keyword research
    if keyWord:
        movieList = movieList.filter(Q(movie_name__contains=keyWord) | Q(cast__contains=keyWord) |
                                     Q(introduction__contains=keyWord) | Q(type__contains=keyWord))
        condition.append('keyword=' + keyWord)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(movieList, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    movieList2 = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"movieList": movieList2, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for movie in movieList:
        print(movie.toDict())
    return render(request, 'my_staff/movie/index.html', context)


# load employee information addition form
def add(request):
    return render(request, 'my_staff/movie/add.html')


# insert new staff action
def insert(request):
    try:
        ob = Movie()
        while True:
            movie_id = random.randint(10000000, 99999999)
            try:
                movie = Movie.objects.get(movie_id=movie_id)
            except Exception as err:
                ob.movie_id = movie_id
                break
            else:
                continue

        posterFile = request.FILES.get("poster", None)
        if not posterFile:
            context = {'info': "Add new movie fails,no poster upload"}
            return render(request, 'my_staff/info.html', context)
        poster = datetime.now().strftime("%Y-%m-%d %H-%M-%S") + "." + posterFile.name.split('.').pop()

        ob.movie_name = request.POST['name']
        ob.poster = poster
        ob.type = request.POST['type']
        ob.cast = request.POST['cast']
        ob.introduction = request.POST['introduction']
        ob.duration = request.POST['duration']
        ob.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        context = {'info': "Add new movie successfully, movie_id is %s" % ob.movie_id}
        ob.save()
        destination = open("./static/uploads/movie_pic/" + poster, "wb+")
        for chunk in posterFile.chunks():
            destination.write(chunk)
        destination.close()
    except Exception as err:
        print(err)
        context = {'info': "Add new movie fails"}
    return render(request, 'my_staff/info.html', context)


# load employee information edit form
def edit(request, movieId=0):
    try:
        ob = Movie.objects.get(movie_id=movieId)
        context = {'movie': ob}
        return render(request, 'my_staff/movie/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Cannot find the information of edited movie'}
    return render(request, 'my_staff/info.html', context)


# update staff information action
def update(request):
    try:
        movieId = request.POST["movieId"]
        ob = Movie.objects.get(movie_id=movieId)
        ob.movie_name = request.POST['name']
        ob.type = request.POST['type']
        ob.cast = request.POST['cast']
        ob.introduction = request.POST['introduction']
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "Update Successfully"}
        return render(request, 'my_staff/info.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Update Failed'}
    return render(request, 'my_staff/info.html', context)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
