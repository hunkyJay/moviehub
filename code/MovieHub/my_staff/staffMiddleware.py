from django.shortcuts import redirect
from django.urls import reverse

import re


class StaffMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("staffMiddleware")

    def __call__(self, request):

        # get current url
        path = request.path
        print("url:" + path)

        # url judgement
        urllist = ['/my_staff/loadLogin', '/my_staff/login', '/my_staff/logout', '/my_staff/verify']
        # whether the url is going to staff
        if re.match(r"^/my_staff", path) and (path not in urllist):
            # judge whether the staff is logged in
            if "staffuser" not in request.session:
                # go to the login interface
                return redirect(reverse('staff_load_login'))

        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response
