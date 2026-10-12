import json
import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore

store = JsonStore('config.json')

class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # LLM Settings
        layout.add_widget(Label(text="LLM Base URL:"))
        self.llm_url = TextInput(text=store.get('_default', 'llm_url', 'https://ollama.com/v1'), multiline=False)
        layout.add_widget(self.llm_url)
        
        layout.add_widget(Label(text="LLM Model:"))
        self.llm_model = TextInput(text=store.get('_default', 'llm_model', 'gemma4'), multiline=False)
        layout.add_widget(self.llm_model)
        
        layout.add_widget(Label(text="LLM API Key:"))
        self.llm_key = TextInput(text=store.get('_default', 'llm_key', ''), password=True, multiline=False)
        layout.add_widget(self.llm_key)
        
        # TTS Settings
        layout.add_widget(Label(text="TTS Base URL:"))
        self.tts_url = TextInput(text=store.get('_default', 'tts_url', 'https://api.fish.audio/v1/tts'), multiline=False)
        layout.add_widget(self.tts_url)
        
        layout.add_widget(Label(text="TTS Model:"))
        self.tts_model = TextInput(text=store.get('_default', 'tts_model', 's2.1-pro-free'), multiline=False)
        layout.add_widget(self.tts_model)
        
        layout.add_widget(Label(text="TTS API Key:"))
        self.tts_key = TextInput(text=store.get('_default', 'tts_key', ''), password=True, multiline=False)
        layout.add_widget(self.tts_key)
        
        save_btn = Button(text="Save Settings", background_color=(0, 1, 0, 1))
        save_btn.bind(on_press=self.save_settings)
        layout.add_widget(save_btn)
        
        self.add_widget(layout)

    def save_settings(self, instance):
        store.put('_default', 
                   llm_url=self.llm_url.text, 
                   llm_model=self.llm_model.text, 
                   llm_key=self.llm_key.text,
                   tts_url=self.tts_url.text,
                   tts_model=self.tts_model.text,
                   tts_key=self.tts_key.text)
        print("Settings Saved!")

class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        self.status_label = Label(text="Ready to talk...")
        layout.add_widget(self.status_label)
        
        self.mic_btn = Button(text="Press to Talk", size_hint=(1, 0.3))
        self.mic_btn.bind(on_press=self.start_recording)
        layout.add_widget(self.mic_btn)
        
        settings_btn = Button(text="Settings", size_hint=(1, 0.2))
        settings_btn.bind(on_press=self.go_to_settings)
        layout.add_widget(settings_btn)
        
        self.add_widget(layout)

    def start_recording(self, instance):
        self.status_label.text = "Listening... (Simulation)"
        # Integration for recording and API calls would go here
        
    def go_to_settings(self, instance):
        self.manager.current = 'settings'

class VoiceAIApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))
        return sm

if __name__ == '__main__':
    VoiceAIApp().run()
