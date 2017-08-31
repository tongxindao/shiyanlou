from pyflk.view import Controller

from controller.index.urls import url_map

controller = Controller('index_controller', url_map)
