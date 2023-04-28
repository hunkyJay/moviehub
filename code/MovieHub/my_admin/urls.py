from django.urls import path

from my_admin.views import index
from my_admin.views import staff
from my_admin.views import room
from my_admin.views import movie
from my_admin.views import announcement
from my_admin.views import release
from my_admin.views import customer
from my_admin.views import order

urlpatterns = [
    # admin home page
    path('', index.index, name="admin_homepage"),

    # login logout
    path('loadLogin', index.loadLogin, name="admin_load_login"),
    path('login', index.login, name="admin_login"),
    path('logout', index.logout, name="admin_logout"),
    path('verify', index.verify, name="admin_verify"),

    # staff information management
    path('staff/<int:pIndex>', staff.index, name="admin_staff_index"),
    path('staff/add', staff.add, name="admin_staff_add"),
    path('staff/insert', staff.insert, name="admin_staff_insert"),
    path('staff/delete/<int:staffId>', staff.delete, name="admin_staff_delete"),
    path('staff/edit/<int:staffId>', staff.edit, name="admin_staff_edit"),
    path('staff/update/', staff.update, name="admin_staff_update"),

    # room management
    path('room/<int:pIndex>', room.index, name="admin_room_index"),
    path('room/add', room.add, name="admin_room_add"),
    path('room/insert', room.insert, name="admin_room_insert"),
    path('room/edit/<int:roomId>', room.edit, name="admin_room_edit"),
    path('room/update/', room.update, name="admin_room_update"),

    # movie info management
    path('movie/<int:pIndex>', movie.index, name="admin_movie_index"),
    path('movie/add', movie.add, name="admin_movie_add"),
    path('movie/insert', movie.insert, name="admin_movie_insert"),
    path('movie/edit/<int:movieId>', movie.edit, name="admin_movie_edit"),
    path('movie/update', movie.update, name="admin_movie_update"),
    path('movie/checkReleaseNum/<int:movieId>', movie.checkReleaseNum, name="admin_movie_check_release"),

    # announcement information management
    path('announcement/<int:pIndex>', announcement.index, name="admin_announcement_index"),
    path('announcement/add', announcement.add, name="admin_announcement_add"),
    path('announcement/insert', announcement.insert, name="admin_announcement_insert"),
    path('announcement/delete/<int:announcementId>', announcement.delete, name="admin_announcement_delete"),

    # release info management
    path('release/<int:pIndex>', release.index, name="admin_release_index"),
    path('release/edit/<int:releaseId>', release.edit, name="admin_release_edit"),
    path('release/update/', release.update, name="admin_release_update"),
    path('release/delete/<int:releaseId>', release.delete, name="admin_release_delete"),

    # customer info management
    path('customer/<int:pIndex>', customer.index, name="admin_customer_index"),

    # order info management
    path('order/<int:pIndex>', order.index, name="admin_order_index"),
]
