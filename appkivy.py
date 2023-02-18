from kivy.app import App
from kivy.lang import Builder

class app(App):
    gui = Builder.load_file("tela.kv")
    def build(sf): return sf.gui

    def on_start(self):
        self.root.ids["dolar"].text="dolar:5,00"
        self.root.ids["euro"].text="euro:5,12"
        self.root.ids["ouro"].text="ouro:300,00"

if __name__=="__main__": app().run()