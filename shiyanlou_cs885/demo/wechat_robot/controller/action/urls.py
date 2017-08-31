from controller.action import views

url_map = [
    {'url': '/ctrl/change_text', 'view': views.ChangeText, 'endpoint': 'change_text'}
]
