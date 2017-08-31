from controller.user import views

url_map = [
    {'url': '/user', 'view': views.UserList, 'endpoint': 'user_list'},
    {'url': '/api/get_friends', 'view': views.GetFriends, 'endpoint': 'get_friends'}
]
