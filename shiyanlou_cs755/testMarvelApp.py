#_*_ coding:utf-8 _*_

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scatter import Scatter
from kivy.uix.carousel import Carousel
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.uix.scrollview import ScrollView

class Marvel(BoxLayout):
    def hulk_smash(self):
        self.ids.hulk.text = "hulk: puny god!"
        self.ids["loki"].text = "loki: >_<!!!"

class testMarvelApp(App):
    def build(self):
        return Marvel()

if __name__ == '__main__':
    testMarvelApp().run()
