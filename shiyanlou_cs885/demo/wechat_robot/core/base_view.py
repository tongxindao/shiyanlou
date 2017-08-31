#!/usr/bin/env python
# encoding: utf-8

from pyflk import redirect
from pyflk.view import View
from pyflk.session import AuthSession, session, get_session_id

from core.wechat_manager import WeChat
import pyflk.exceptions as exceptions

class BaseView(View):

    # define support request method, default support GET and POST method
    methods = ['GET, POST']
    request = None
    session_id = None
    session_map = None
    wechat = None

    # POST request handle function
    def post(self):
        pass

    # GET request handle function
    def get(self):
        pass

    # view handle function call entrance
    def dispatch_request(self, request, *args, **options):

        # define request method and handle function mapping
        methods_meta = {
            'GET': self.get,
            'POST': self.post,
        }

        self.request = request
        self.session_id = get_session_id(request)
        self.session_map = session.map(request)

        if 'wechat' not in self.session_map:
            session.push(request, 'wechat', WeChat())
            # session.push(request, 'wechat', WeChat(), is_save=False)
            self.wechat = session.get(request, 'wechat')

        self.wechat = session.get(request, 'wechat')

        if request.method in methods_meta:
            return methods_meta[request.method]()
        else:
            raise exceptions.InvalidRequestMethodError

class AuthLogin(AuthSession):
    '''
    login verification class
    '''

    @staticmethod
    def auth_fail_callback(request, *args, **options):
        ''' if auth fail, then return a lick, click it skip to login page '''

        return redirect("/login")

    @staticmethod
    def auth_logic(request, *args, **options):
        ''' verification logic, if user key not in Session, then auth fail, if not be success '''

        if 'user' in session.map(request):
            return True
        return False

class SessionView(BaseView):
    '''
    Session view base class
    '''

    @AuthLogin.auth_session
    def dispatch_request(self, request, *args, **options):
        ''' verification class decorator '''

        # combination decorator internal logic, call inherit subclass dispatch_request method
        return super(SessionView, self).dispatch_request(request, *args, **options) 
