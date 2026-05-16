# -*- coding: utf-8 -*-
import sys

class AntiCrashAbsolute:
    def __getattr__(self, name):
        if name == 'bind':
            return lambda *args, **kwargs: None
        # إرجاع نص فارغ أو كائن فارغ في حال طلب id أو أي خاصية أخرى
        if name == 'id':
            return "dynamic_safe_id"
        return None
    def __bool__(self):
        return False

sys.modules['NoneType'] = AntiCrashAbsolute


# Système de sécurité pour empêcher les plantages d'objets non définis
import sys




from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
import os

class SatChannelEditorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.channels_data = []      
        self.filtered_channels = []  
        self.selected_index = None    

        screen = MDScreen()
        main_layout = BoxLayout(orientation='vertical')

        self.toolbar = MDTopAppBar(title="Sat Channel Editor Pro")
        self.toolbar.anchor_title = "center"
        self.toolbar.right_action_items = [
            ["file-upload", lambda x: self.open_file_selector(), "Import File"],
            ["file-export", lambda x: self.show_export_options(), "Export Options"]
        ]
        main_layout.add_widget(self.toolbar)

        search_layout = BoxLayout(orientation='horizontal', padding=(10, 5), size_hint_y=None, height="60dp")
        self.search_input = MDTextField(hint_text="Quick Search Channel...", size_hint_x=1.0)
        self.search_input.bind(text=self.filter_channels_by_search)
        search_layout.add_widget(self.search_input)
        main_layout.add_widget(search_layout)

        filter_layout = BoxLayout(orientation='horizontal', padding=(10, 2), spacing=5, size_hint_y=None, height="45dp")
        dz_btn = MDRaisedButton(text="Algerian Channels 🇩🇿", on_release=self.isolate_algerian_channels, font_size="10sp", md_bg_color=(0.1, 0.5, 0.2, 1))
        sport_btn = MDRaisedButton(text="Sports Channels ⚽", on_release=self.isolate_sports_channels, font_size="10sp", md_bg_color=(0.9, 0.4, 0.0, 1))
        sort_btn = MDRaisedButton(text="Sort A-Z", on_release=self.sort_channels_alphabetically, font_size="10sp")
        filter_layout.add_widget(dz_btn)
        filter_layout.add_widget(sport_btn)
        filter_layout.add_widget(sort_btn)
        main_layout.add_widget(filter_layout)

        clean_layout = BoxLayout(orientation='horizontal', padding=(10, 2), spacing=5, size_hint_y=None, height="45dp")
        clean_radio_btn = MDRaisedButton(text="Clean Radio", on_release=self.remove_radio_channels, font_size="10sp", size_hint_x=0.5)
        clean_crypto_btn = MDRaisedButton(text="Clean Encrypted", on_release=self.remove_encrypted_channels, font_size="10sp", size_hint_x=0.5)
        clean_layout.add_widget(clean_radio_btn)
        clean_layout.add_widget(clean_crypto_btn)
        main_layout.add_widget(clean_layout)

        edit_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height="70dp")
        self.channel_input = MDTextField(hint_text="Modify Target Channel Name", size_hint_x=0.7)
        save_btn = MDRaisedButton(text="Apply", on_release=self.save_channel_name, size_hint_x=0.3, pos_hint={"center_y": 0.5})
        edit_layout.add_widget(self.channel_input)
        edit_layout.add_widget(save_btn)
        main_layout.add_widget(edit_layout)

        scroll = ScrollView()
        self.list_container = MDList()
        scroll.add_widget(self.list_container)
        main_layout.add_widget(scroll)

        bottom_layout = BoxLayout(orientation='horizontal', padding=10, spacing=20, size_hint_y=None, height="60dp")
        delete_btn = MDRaisedButton(text="Remove Item", md_bg_color=(0.7, 0.1, 0.1, 1), on_release=self.delete_channel, size_hint_x=0.5)
        clear_btn = MDRaisedButton(text="Flush Dataset", md_bg_color=(0.4, 0.4, 0.4, 1), on_release=self.clear_all, size_hint_x=0.5)
        bottom_layout.add_widget(clear_btn)
        bottom_layout.add_widget(delete_btn)
        main_layout.add_widget(bottom_layout)

        screen.add_widget(main_layout)
        return screen

    def isolate_algerian_channels(self, instance):
        if not self.channels_data: return
        keywords = ["algerie", "dz", "entv", "echorouk", "el bilad", "samira", "beur", "tv3", "tamazight", "الجزائر"]
        self.filtered_channels = [ch for ch in self.channels_data if any(key in ch['name'].lower() for key in keywords)]
        self.refresh_ui_list()

    def isolate_sports_channels(self, instance):
        if not self.channels_data: return
        keywords = ["sport", "bein", "ssc", "alkass", "abu dhabi", "eurosport", "eleven", "arena", "كأس", "رياضية"]
        self.filtered_channels = [ch for ch in self.channels_data if any(key in ch['name'].lower() for key in keywords)]
        self.refresh_ui_list()

    def filter_channels_by_search(self, instance, value):
        query = self.search_input.text.lower().strip()
        if not query: self.filtered_channels = list(self.channels_data)
        else: self.filtered_channels = [ch for ch in self.channels_data if query in ch['name'].lower()]
        self.refresh_ui_list()

    def sort_channels_alphabetically(self, instance):
        if not self.channels_data: return
        self.channels_data.sort(key=lambda x: x['name'].lower())
        self.filter_channels_by_search(None, None)

    def remove_radio_channels(self, instance):
        self.channels_data = [ch for ch in self.channels_data if "radio" not in ch['name'].lower()]
        self.filter_channels_by_search(None, None)

    def remove_encrypted_channels(self, instance):
        self.channels_data = [ch for ch in self.channels_data if "$" not in ch['name']]
        self.filter_channels_by_search(None, None)

    def open_file_selector(self):
        try:
            from plyer import filechooser
            filechooser.open_file(on_selection=self.auto_parse_handler)
        except Exception:
            pass

    def auto_parse_handler(self, selection):
        if not selection or not selection[0]: return
        file_path = selection[0]
        self.channels_data.clear()
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            current_channel = {}
            for line in lines:
                line = line.strip()
                if not line: continue
                if line.startswith("#EXTINF:"):
                    parts = line.split(",")
                    current_channel['name'] = parts[-1].strip() if len(parts) > 1 else "Unknown"
                elif line.startswith("http") or line.startswith("rtmp") or "FREQ" in line:
                    current_channel['source'] = line
                    if 'name' not in current_channel: current_channel['name'] = f"Channel_{len(self.channels_data) + 1}"
                    self.channels_data.append(current_channel)
                    current_channel = {}
            self.filter_channels_by_search(None, None)
        except Exception:
            pass

    def refresh_ui_list(self):
        self.list_container.clear_widgets()
        for index, ch in enumerate(self.filtered_channels):
            actual_idx = self.channels_data.index(ch)
            item = OneLineListItem(text=f"{ch['name']} ({ch.get('source', '')[:15]}...)", on_release=lambda x, i=actual_idx: self.on_item_select(i))
            self.list_container.add_widget(item)

    def on_item_select(self, index):
        self.selected_index = index
        self.channel_input.text = self.channels_data[index]['name']

    def save_channel_name(self, instance):
        if self.selected_index is not None and self.channel_input.text.strip():
            self.channels_data[self.selected_index]['name'] = self.channel_input.text.strip()
            self.filter_channels_by_search(None, None)

    def delete_channel(self, instance):
        if self.selected_index is not None:
            self.channels_data.pop(self.selected_index)
            self.filter_channels_by_search(None, None)

    def clear_all(self, instance):
        self.channels_data.clear()
        self.filter_channels_by_search(None, None)

    def show_export_options(self):
        if not self.channels_data: return
        self.export_dialog = MDDialog(
            title="Convert Options",
            buttons=[
                MDFlatButton(text="M3U", on_release=lambda x: self.execute_export("m3")),
                MDFlatButton(text="CFG", on_release=lambda x: self.execute_export("cfg"))
            ]
        )
        self.export_dialog.open()

    def execute_export(self, mode):
        self.export_dialog.dismiss()
        try:
            if mode == "m3":
                file_name = "Smart_Output.m3u"
                with open(file_name, 'w', encoding='utf-8') as f:
                    f.write("#EXTM3U\n")
                    for ch in self.channels_data: f.write(f"#EXTINF:-1,{ch['name']}\n{ch.get('source', '')}\n")
            else:
                file_name = "Receiver_Output.cfg"
                with open(file_name, 'w', encoding='utf-8') as f:
                    for idx, ch in enumerate(self.channels_data): f.write(f"CH:{idx+1} | NAME:{ch['name']}\n")
        except Exception:
            pass

if __name__ == "__main__":
    SatChannelEditorApp().run()
