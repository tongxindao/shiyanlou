import kivy

from kivy.app import App
from kivy.uix.button import Button

def callback(instance):
    print('The button <%s> is being pressed' % instance.text)

bt1 = Button(text = 'Hello World')
bt1.bind(on_press = callback)

class TestApp(App):
    def build(self):
        return bt1

TestApp().run()
