# app/ui/screens/questionario.py
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from app.ui.widgets.limited_text_field import LimitedTextField


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
        self.bind(width=self._resize_to_text, texture_size=self._resize_to_text)

    def _resize_to_text(self, *_args):
        if self.width <= 0:
            return
        self.text_size = (self.width, None)
        self.texture_update()
        self.height = max(dp(48), self.texture_size[1] + self.padding[1] + self.padding[3])


class QuestionarioContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(16)
        self.padding = dp(16)
        self.adaptive_height = True
        self.fields = {}
        self.limited_fields = {}

        self.add_widget(SectionTitle("QUESTIONÁRIO — FAZER BREVE COMENTÁRIO SOBRE TEMAS ABAIXO"))

        temas = [
            ("palavra_revelada", "PALAVRA REVELADA"),
            ("clamor_sangue_jesus", "CLAMOR PELO PODER DO SANGUE DE JESUS"),
            ("igreja_corpo_cristo", "IGREJA CORPO DE CRISTO"),
            ("salvacao", "SALVAÇÃO"),
            ("origens_fe", "ORIGENS DA FÉ OU FÉ HISTÓRICA E PROFÉTICA"),
            ("sacerdocio_universal", "SACERDÓCIO UNIVERSAL DO CRENTE"),
            ("objetivo_satelite", "OBJETIVO DAS TRANSMISSÕES VIA SATÉLITE ÀS IGREJAS"),
        ]
        for key, label in temas:
            ltf = LimitedTextField(
                label_text=label,
                hint_text="Comentário...",
                max_chars=1000,
            )
            self.limited_fields[key] = ltf
            self.add_widget(ltf)

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        for k, lf in self.limited_fields.items():
            d[k] = lf.get_text()
        return d