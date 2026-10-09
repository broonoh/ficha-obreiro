# app/ui/widgets/limited_text_field.py
"""Campo de texto com limite de caracteres e contador em tempo real."""
from kivy.metrics import dp
from kivy.properties import NumericProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard


class LimitedTextField(MDBoxLayout):
    """
    Campo de texto com limite de caracteres.
    Mostra contador "X/MAX" em tempo real.
    """

    MAX_CHARS = NumericProperty(3000)
    current_count = NumericProperty(0)
    current_text = StringProperty("")

    def __init__(self, label_text, hint_text="Digite...", max_chars=3000, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(200)
        self.spacing = dp(8)
        self.padding = [dp(4), dp(12), dp(4), dp(8)]
        self.MAX_CHARS = max_chars
        self._label_text = label_text
        self._hint_text = hint_text

        # Label do campo (título)
        self.title_label = MDLabel(
            text=label_text,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None,
            height=dp(22),
            bold=True,
        )
        self.add_widget(self.title_label)

        # Container: campo + contador
        row = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(160),
            spacing=dp(4),
        )

        # CORREÇÃO: Usar MDCard como container visual + MDTextField
        # elevation=0: a sombra do MDCard (CommonElevationBehavior) fica
        # "fantasma" dentro do MDExpansionPanel/ScrollView — especialmente
        # feio ao abrir/fechar outro painel — e vira uma barra preta enorme.
        card = MDCard(
            size_hint_y=None,
            height=dp(130),
            radius=[8],
            elevation=0,
            md_bg_color=(0.97, 0.97, 0.97, 1),
            padding=[dp(12), dp(12), dp(12), dp(12)],
        )

        # Campo de texto multiline — CORREÇÃO: removido line_color_disabled
        self.text_field = MDTextField(
            hint_text=hint_text,
            mode="rectangle",
            multiline=True,
            font_size="14sp",
            size_hint_y=1,
            line_color_normal=(0, 0, 0, 0),
            line_color_focus=(0, 0, 0, 0),
            # line_color_disabled removido — não existe no KivyMD 1.1.1
        )
        self.text_field.bind(text=self._on_text_changed)
        card.add_widget(self.text_field)

        row.add_widget(card)

        # Contador
        self.counter_label = MDLabel(
            text=f"0/{max_chars}",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.29, 0.33, 0.42, 1),
            halign="right",
            size_hint_y=None,
            height=dp(18),
        )
        row.add_widget(self.counter_label)

        self.add_widget(row)

    def _on_text_changed(self, instance, value):
        """Atualiza contador e limita caracteres em tempo real."""
        if len(value) > self.MAX_CHARS:
            self.text_field.text = value[:self.MAX_CHARS]
            self.current_text = value[:self.MAX_CHARS]
        else:
            self.current_text = value

        self.current_count = len(self.current_text)
        self.counter_label.text = f"{self.current_count}/{self.MAX_CHARS}"

        # Muda cor quando接近 do limite
        if self.current_count >= self.MAX_CHARS:
            self.counter_label.text_color = (0.706, 0.098, 0.149, 1)
        elif self.current_count > self.MAX_CHARS * 0.9:
            self.counter_label.text_color = (0.831, 0.627, 0.090, 1)
        else:
            self.counter_label.text_color = (0.29, 0.33, 0.42, 1)

    def get_text(self):
        return self.current_text