from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

class SatChannelEditorApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        self.channels_data = []
        self.selected_index = None

        screen = MDScreen()
        main_layout = BoxLayout(orientation='vertical')

        self.toolbar = MDTopAppBar(title="Sat Channel Editor Pro")
        self.toolbar.anchor_title = "center"
        self.toolbar.right_action_items = [
            ["file-import", lambda x: self.simulate_import(), "استيراد"],
            ["file-export", lambda x: self.simulate_export(), "تصدير"]
        ]
        main_layout.add_widget(self.toolbar)

        edit_layout = BoxLayout(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height="80dp")
        self.channel_input = MDTextField(hint_text="اسم القناة المحددة", size_hint_x=0.7)
        save_btn = MDRaisedButton(text="حفظ", on_release=self.save_channel_name, size_hint_x=0.3, pos_hint={"center_y": 0.5})
        edit_layout.add_widget(self.channel_input)
        edit_layout.add_widget(save_btn)
        main_layout.add_widget(edit_layout)

        scroll = ScrollView()
        self.list_container = MDList()
        scroll.add_widget(self.list_container)
        main_layout.add_widget(scroll)

        bottom_layout = BoxLayout(orientation='horizontal', padding=10, spacing=20, size_hint_y=None, height="60dp")
        delete_btn = MDRaisedButton(text="حذف", md_bg_color=(0.7, 0.1, 0.1, 1), on_release=self.delete_channel, size_hint_x=0.5)
        clear_btn = MDRaisedButton(text="مسح الكل", md_bg_color=(0.4, 0.4, 0.4, 1), on_release=self.clear_all, size_hint_x=0.5)
        bottom_layout.add_widget(clear_btn)
        bottom_layout.add_widget(delete_btn)
        main_layout.add_widget(bottom_layout)

        screen.add_widget(main_layout)
        return screen

    def simulate_import(self):
        self.channels_data = [
            {"name": "Algerie Terrestre", "freq": "11680 H 27500"},
            {"name": "BeIN Sports 1 HD", "freq": "11013 H 27500"},
            {"name": "Canal+ France", "freq": "12012 V 29700"}
        ]
        self.refresh_ui_list()
        self.show_dialog("نجاح", f"تم استيراد {len(self.channels_data)} قنوات!")

    def refresh_ui_list(self):
        self.list_container.clear_widgets()
        for index, ch in enumerate(self.channels_data):
            display_text = f"{ch['name']}   |   ({ch['freq']})"
            item = OneLineListItem(text=display_text, on_release=lambda x, i=index: self.on_item_select(i))
            self.list_container.add_widget(item)

    def on_item_select(self, index):
        self.selected_index = index
        self.channel_input.text = self.channels_data[index]['name']

    def save_channel_name(self, instance):
        if self.selected_index is not None and self.channel_input.text.strip():
            self.channels_data[self.selected_index]['name'] = self.channel_input.text.strip()
            self.refresh_ui_list()
            self.channel_input.text = ""
            self.selected_index = None

    def delete_channel(self, instance):
        if self.selected_index is not None:
            self.channels_data.pop(self.selected_index)
            self.refresh_ui_list()
            self.channel_input.text = ""
            self.selected_index = None

    def clear_all(self, instance):
        self.channels_data.clear()
        self.refresh_ui_list()
        self.channel_input.text = ""

    def simulate_export(self):
        if self.channels_data:
            self.show_dialog("نجاح التصدير", "تم حفظ وتوليد ملف القنوات بنجاح.")

    def show_dialog(self, title, text):
        MDDialog(title=title, text=text, size_hint=(0.8, None)).open()

if __name__ == "__main__":
    SatChannelEditorApp().run()
