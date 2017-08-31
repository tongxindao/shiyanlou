from pyflk.view import Controller

from controller.user.urls import url_map

controller = Controller('user_controller', url_map)
