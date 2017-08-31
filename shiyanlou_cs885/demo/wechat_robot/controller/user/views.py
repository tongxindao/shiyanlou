from pyflk import simple_template, render_json

from core.base_view import SessionView

class UserList(SessionView):
    def get(self):
        return simple_template('user/list.html', value=self.wechat.message_map.get('auto_replay', ''))

class GetFriends(SessionView):
    def get(self):
        return render_json(self.wechat.get_friend_list())
