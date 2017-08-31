from controller.index import views

url_map = [
    {'url': '/', 'view': views.Index, 'endpoint': 'index'}
]
