from django.shortcuts import redirect
from django.urls import reverse

import re


class AdminMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("AdminMiddleware")

    def __call__(self, request):

        # get current url
        path = request.path
        print("url:" + path)

        # url judgement
        urllist = ['/my_admin/loadLogin', '/my_admin/login', '/my_admin/logout', '/my_admin/verify']
        # whether the url is going to admin
        if re.match(r"^/my_admin", path) and (path not in urllist):
            # judge whether the staff is logged in
            if "adminuser" not in request.session:
                # go to the login interface
                return redirect(reverse('admin_load_login'))

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
