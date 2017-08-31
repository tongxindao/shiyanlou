from pyflk import render_json

from core.base_view import SessionView

class ChangeText(SessionView):
    def get(self):
        self.wechat.message_map['auto_replay'] = self.request.args.get('msg', 'test auto replay')
        self.wechat.save_message_config()
        return render_json({'ok': 1})
