from django.urls import path
from movie_web.views import customer, index, movie, order, announcement

urlpatterns = [
    # movie web home page
    path('', index.index, name="welcome"),

    # register, login, and logout
    path('register', index.register, name = "customer_register"),
    path('doRegister', index.doRegister, name = "customer_do_register"),
    path('loadLogin', index.loadLogin, name="customer_load_login"),
    path('login', index.login, name="customer_login"),
    path('logout', index.logout, name="customer_logout"),
    path('verify', index.verify, name="customer_verify"),
    path('home', index.home, name="customer_home"),

    # Profile management
    path('customer', customer.edit, name="customer_edit"),
    path('customer/update', customer.update, name="customer_update"),

    # announcement information
    path('announcement/<int:pIndex>', announcement.index, name="customer_announcement_index"),
    path('announcement/view/<int:announcementId>', announcement.view, name="customer_announcement_view"),

    # Movie page
    path('movie/<int:pIndex>', movie.index, name="customer_movie_index"),
    path('releaseList/<int:pIndex>', movie.releaseList, name="customer_release_list"),
    path('loadBooking/<int:release_id>', movie.loadBooking, name="customer_load_booking"),
    path('movie/book', movie.bookMovie, name="customer_book_movie"),

    # order
    path('order/<int:pIndex>', order.index, name="customer_order_index"),
    path('order/cancel', order.cancel, name="customer_order_cancel"),
]