# app/ui/widgets/dropdown_field.py
"""Dropdown compatível com KivyMD 1.1.1 — crash corrigido e funcional."""
from kivy.metrics import dp
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel


class DropdownField(MDBoxLayout):
    """Campo dropdown reutilizável — KivyMD 1.1.1."""

    def __init__(self, label_text, items, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(85)
        self.spacing = dp(4)
        self.selected_value = None

        # Label
        lbl = MDLabel(
            text=label_text,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None,
            height=dp(22),
            bold=True,
        )
        self.add_widget(lbl)

        # Botão
        # MDFlatButton (em vez de MDRaisedButton) não usa o
        # CommonElevationBehavior/sombra — ver nota em limited_text_field.py
        # e photo_field.py sobre o bug sistêmico de sombra "fantasma" dentro
        # do MDExpansionPanel/ScrollView.
        self.button = MDFlatButton(
            text="  Selecione...",
            md_bg_color=(0.012, 0.133, 0.247, 1),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(44),
        )
        self.add_widget(self.button)

        # Menu — CORREÇÃO: usar Clock.schedule_once para garantir posicionamento
        # "viewclass" é obrigatório: sem ele o RecycleView do menu não
        # renderiza nenhuma linha (menu abre em branco). MDDropdownMenu não
        # tem um evento "on_release" próprio — o callback de cada item tem
        # que vir no próprio dict do item.
        menu_items = [
            {
                "text": item,
                "viewclass": "OneLineListItem",
                "height": dp(48),
                "on_release": lambda x=item: self.on_menu_release(x),
            }
            for item in items
        ]
        self.menu = MDDropdownMenu(
            caller=self.button,
            items=menu_items,
            width_mult=4,
        )
        # CORREÇÃO: usar Clock para abrir após layout estar pronto
        self.button.bind(on_release=self._open_menu_safe)

    def _open_menu_safe(self, *args):
        """Abre o menu de forma segura, após o layout estar pronto."""
        Clock.schedule_once(lambda dt: self.menu.open(), 0)

    def on_menu_release(self, value):
        self.selected_value = value
        self.button.text = f"  {value}"
        self.menu.dismiss()

    def get_value(self):
        return self.selected_value