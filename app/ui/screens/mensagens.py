# app/ui/screens/mensagens.py
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from app.ui.widgets.limited_text_field import LimitedTextField


class FieldRow(MDBoxLayout):
    """Linha label + campo simples (TEXTO e TEMA)."""
    def __init__(self, label_text, field, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(80)
        self.spacing = dp(4)
        self.padding = [dp(4), dp(4), dp(4), dp(4)]

        lbl = MDLabel(
            text=label_text,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None,
            height=dp(18),
            bold=True,
        )
        self.add_widget(lbl)
        self.add_widget(field)


class SectionTitle(MDLabel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_style = "H6"
        self.theme_text_color = "Custom"
        self.text_color = (0.012, 0.133, 0.247, 1)
        self.size_hint_y = None
        self.height = dp(48)
        self.bold = True
        self.padding = [0, dp(12), 0, dp(8)]


class SubTitle(MDLabel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_style = "Subtitle1"
        self.theme_text_color = "Custom"
        self.text_color = (0.706, 0.098, 0.149, 1)
        self.size_hint_y = None
        self.height = dp(40)
        self.bold = True
        self.padding = [0, dp(12), 0, dp(4)]


class MensagensContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(16)
        self.padding = dp(16)
        self.adaptive_height = True
        self.fields = {}
        self.limited_fields = {}

        self.add_widget(SectionTitle("MENSAGENS REVELADAS"))

        # ═══════════════════════════════════════════════════
        # 1ª MENSAGEM
        # ═══════════════════════════════════════════════════
        self.add_widget(SubTitle(
            "1ª MENSAGEM - MENSAGEM RESUMIDA ALCANÇADA PELO OBREIRO"
        ))

        # TEXTO = referência bíblica (campo pequeno)
        self.fields["msg1_texto"] = MDTextField(
            hint_text="TEXTO (referência bíblica, ex: João 3:16):",
            mode="fill", size_hint_y=None, height=dp(56)
        )
        self.add_widget(FieldRow("TEXTO:", self.fields["msg1_texto"]))

        # TEMA (campo pequeno)
        self.fields["msg1_tema"] = MDTextField(
            hint_text="TEMA:", mode="fill", size_hint_y=None, height=dp(56)
        )
        self.add_widget(FieldRow("TEMA:", self.fields["msg1_tema"]))

        # ÁREA GRANDE DE DIGITAÇÃO (3000 chars) — abaixo do TEMA
        self.limited_fields["msg1_descricao"] = LimitedTextField(
            label_text="DESCREVA AQUI A MENSAGEM REVELADA:",
            hint_text="Descreva aqui a mensagem revelada...",
            max_chars=3000,
        )
        self.add_widget(self.limited_fields["msg1_descricao"])

        # ═══════════════════════════════════════════════════
        # 2ª MENSAGEM
        # ═══════════════════════════════════════════════════
        self.add_widget(SubTitle(
            "2ª MENSAGEM - MENSAGEM RESUMIDA"
        ))

        self.fields["msg2_texto"] = MDTextField(
            hint_text="TEXTO (referência bíblica, ex: João 3:16):",
            mode="fill", size_hint_y=None, height=dp(56)
        )
        self.add_widget(FieldRow("TEXTO:", self.fields["msg2_texto"]))

        self.fields["msg2_tema"] = MDTextField(
            hint_text="TEMA:", mode="fill", size_hint_y=None, height=dp(56)
        )
        self.add_widget(FieldRow("TEMA:", self.fields["msg2_tema"]))

        self.limited_fields["msg2_descricao"] = LimitedTextField(
            label_text="DESCREVA AQUI A MENSAGEM REVELADA:",
            hint_text="Descreva aqui a mensagem revelada...",
            max_chars=3000,
        )
        self.add_widget(self.limited_fields["msg2_descricao"])

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        for k, lf in self.limited_fields.items():
            d[k] = lf.get_text()
        return d