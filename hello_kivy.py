from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class HelloApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=12)
        self.message = Label(text="Hello, Kuromi Library!")
        button = Button(text="Click me ♡")
        button.bind(on_press=self.clicked)
        layout.add_widget(self.message)
        layout.add_widget(button)
        return layout

    def clicked(self, instance):
        self.message.text = "Button clicked! ✨"

HelloApp().run()
