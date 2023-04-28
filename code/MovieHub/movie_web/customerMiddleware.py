from django.urls import reverse
from django.shortcuts import redirect
import re


class CustomerMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("CustomerMiddleware")

    def __call__(self, request):

        # get current url
        path = request.path
        print("url:" + path)

        # url judgement
        urllist = ['/movie_web/loadLogin', '/movie_web/login', '/movie_logout/logout', '/movie_web/verify','/movie_web/register','/movie_web/doRegister','/movie_web/']
        # whether the url is going to customer
        if re.match(r"^/movie_web", path) and (path not in urllist):
            # judge whether the user is logged in
            if "logineduser" not in request.session:
                # go to the login interface
                return redirect(reverse('customer_load_login'))

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response