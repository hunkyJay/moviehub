import random

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from my_admin.models import Release
from my_admin.models import Movie
from django.core.paginator import Paginator
from datetime import datetime


# browse release information
def index(request, pIndex=1):
    model = Release.objects
    releaseList = model.all()
    keyWord = request.GET.get("keyword", None)
    condition = []
    releaseMovies = []

    # keyword research
    if keyWord:
        condition.append('keyword=' + keyWord)

    for vo in releaseList:
        movieName = Movie.objects.filter(movie_id=vo.movie_id).get().movie_name
        print(movieName)
        if keyWord:
            if movieName != keyWord:
                continue
        if vo.is_delete == 0:
            is_delete = 'no'
        else:
            is_delete = 'yes'
        releaseMovie = {'release_id': vo.release_id, 'movie_id': vo.movie_id, 'movie_name': movieName,
                        'room_id': vo.room_id, 'release_time': vo.release_time,'price':vo.price, 'is_delete': is_delete}
        releaseMovies.append(releaseMovie)

    # In page by 10 record
    pIndex = int(pIndex)
    page = Paginator(releaseMovies, 10)
    maxPages = page.num_pages
    if pIndex > maxPages:
        pIndex = maxPages
    if pIndex < 1:
        pIndex = 1
    releaseMovies = page.page(pIndex)  # acquire current page info
    pageNum = page.page_range  # acquire num of page
    context = {"releaseList": releaseMovies, 'pageNum': pageNum, 'pIndex': pIndex, 'maxPages': maxPages,
               'condition': condition}
    for st in releaseList:
        print(st.toDict())
    return render(request, 'my_admin/release/index.html', context)


# delete release action
def delete(request, releaseId=0):
    try:
        ob = Release.objects.get(release_id=releaseId)
        ob.is_delete = 1
        ob.save()
        context = {'info': 'Successfully cancel this release'}
    except Exception as err:
        context = {'info': 'Cancel fails'}
    return render(request, 'my_admin/info.html', context)


# load release information edit form
def edit(request, releaseId=0):
    try:
        ob = Release.objects.get(release_id=releaseId)
        context = {'release': ob}
        return render(request, 'my_admin/release/edit.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Cannot find the information of edited release'}
    return render(request, 'my_admin/info.html', context)


# update release information action
def update(request):
    try:
        releaseId = request.POST["releaseId"]
        ob = Release.objects.get(release_id=releaseId)
        newTime = request.POST['releaseTime']
        if newTime:
            ob.release_time = newTime
        ob.price = request.POST['price']
        ob.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {'info': "Update Successfully"}
        return render(request, 'my_admin/info.html', context)
    except Exception as err:
        print(err)
        context = {'info': 'Update Failed'}
    return render(request, 'my_admin/info.html', context)
