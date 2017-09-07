import kivy

from kivy.app import App
from kivy.uix.button import Label

class MyApp(App):
    ''' docstring for MyApp '''
    def build(self):
        return Label(text='Hello World')

if __name__ == '__main__':
    MyApp().run()
