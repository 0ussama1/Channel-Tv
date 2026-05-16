# -*- coding: utf-8 -*-
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

class MainScreen(Screen):
    pass

class SatChannelEditorPro(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        
        # إنشاء مدير الشاشات وإرجاع شاشة رئيسية فارغة وآمنة للفحص
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    SatChannelEditorPro().run()
