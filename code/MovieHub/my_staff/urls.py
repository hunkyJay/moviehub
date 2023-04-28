from django.urls import path

from my_staff.views import index
from my_staff.views import staff
from my_staff.views import room
from my_staff.views import movie
from my_staff.views import release
from my_staff.views import manage
from my_staff.views import announcement
from my_staff.views import order
from my_staff.views import customer

urlpatterns = [
    # staff home page
    path('', index.index, name="staff_index"),

    # login logout
    path('loadLogin', index.loadLogin, name="staff_load_login"),
    path('login', index.login, name="staff_login"),
    path('logout', index.logout, name="staff_logout"),
    path('verify', index.verify, name="staff_verify"),

    # staff information management
    path('staff/<int:pIndex>', staff.index, name="staff_staff_index"),

    # room management
    path('room/<int:pIndex>', room.index, name="staff_room_index"),
    path('room/add', room.add, name="staff_room_add"),
    path('room/insert', room.insert, name="staff_room_insert"),
    path('room/edit/<int:roomId>', room.edit, name="staff_room_edit"),
    path('room/update/', room.update, name="staff_room_update"),

    # movie info management
    path('movie/<int:pIndex>', movie.index, name="staff_movie_index"),
    path('movie/add', movie.add, name="staff_movie_add"),
    path('movie/insert', movie.insert, name="staff_movie_insert"),
    path('movie/edit/<int:movieId>', movie.edit, name="staff_movie_edit"),
    path('movie/update/', movie.update, name="staff_movie_update"),

    #release movie
    path('release/<int:pIndex>', release.index, name="staff_release_index"),
    path('release/insert', release.insert, name="staff_release_insert"),
    path('release/edit/<int:movieId>', release.edit, name="staff_release_edit"),
    path('release/update/', release.update, name="staff_release_update"),
    path('release/checkOrderNum/<int:releaseId>', release.checkOrderNum, name="staff_release_check_order"),

    #manage released movie
    path('manage/<int:pIndex>', manage.index, name="staff_manage_index"),
    path('manage/edit/<int:releaseId>', manage.edit, name="staff_manage_edit"),
    path('manage/update/', manage.update, name="staff_manage_update"),
    path('manage/delete/<int:releaseId>', manage.delete, name="staff_manage_delete"),

    # announcement information management
    path('announcement/<int:pIndex>', announcement.index, name="staff_announcement_index"),
    path('announcement/add', announcement.add, name="staff_announcement_add"),
    path('announcement/insert', announcement.insert, name="staff_announcement_insert"),
    path('announcement/delete/<int:announcementId>', announcement.delete, name="staff_announcement_delete"),

    # room management
    path('room/<int:pIndex>', room.index, name="staff_room_index"),
    path('room/add', room.add, name="staff_room_add"),
    path('room/insert', room.insert, name="staff_room_insert"),
    path('room/edit/<int:roomId>', room.edit, name="staff_room_edit"),
    path('room/update/', room.update, name="staff_room_update"),

    # customer info management
    path('customer/<int:pIndex>', customer.index, name="staff_customer_index"),

    # order info management
    path('order/<int:pIndex>', order.index, name="staff_order_index"),
]
