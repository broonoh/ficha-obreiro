# app/ui/screens/experiencias.py
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
        # Width 0 acontece no primeiro frame, antes do layout do pai
        # definir o tamanho real — calcular o texto nesse momento dá uma
        # altura (texture_size) sem sentido (ex.: cada caractere numa
        # linha), e como o MDExpansionPanel só lê a altura do conteúdo no
        # instante em que abre, esse valor errado podia "grudar" e deixar
        # um espaço vazio enorme antes do título.
        if self.width <= 0:
            return
        self.text_size = (self.width, None)
        self.texture_update()
        self.height = max(dp(48), self.texture_size[1] + self.padding[1] + self.padding[3])


class ExperienciasGracaContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(16)
        self.padding = dp(16)
        self.adaptive_height = True
        self.fields = {}
        self.limited_fields = {}

        self.add_widget(SectionTitle("EXPERIÊNCIAS COM RECURSOS DA GRAÇA (MEIOS DE GRAÇA)"))

        temas = [
            ("experiencia_clamor", "EXPERIÊNCIA COM CLAMOR PELO SANGUE DE JESUS/ ORAÇÃO"),
            ("experiencia_jejum", "EXPERIÊNCIA COM JEJUM"),
            ("experiencia_madrugada", "EXPERIÊNCIA COM MADRUGADA"),
            ("experiencia_palavra", "EXPERIÊNCIA COM CONSULTA A PALAVRA OU A PALAVRA"),
            ("experiencia_louvor", "EXPERIÊNCIA COM LOUVOR"),
        ]
        for key, label in temas:
            ltf = LimitedTextField(
                label_text=label,
                hint_text="Descreva a experiência...",
                max_chars=1000,
            )
            self.limited_fields[key] = ltf
            self.add_widget(ltf)

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        for k, lf in self.limited_fields.items():
            d[k] = lf.get_text()
        return d


class ExperienciasObreiroContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(16)
        self.padding = dp(16)
        self.adaptive_height = True
        self.fields = {}
        self.limited_fields = {}

        self.add_widget(SectionTitle("EXPERIÊNCIAS DO OBREIRO"))

        temas = [
            ("dons_cumpridos", "DONS (ENTREGUES PELO OBREIRO) QUE SE CUMPRIRAM"),
            ("provas_vividas", "PROVAS VIVIDAS PELO OBREIRO"),
            ("experiencias_vividas", "EXPERIÊNCIAS VIVIDAS PELO OBREIRO"),
        ]
        for key, label in temas:
            ltf = LimitedTextField(
                label_text=label,
                hint_text="Descreva...",
                max_chars=1000,
            )
            self.limited_fields[key] = ltf
            self.add_widget(ltf)

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        for k, lf in self.limited_fields.items():
            d[k] = lf.get_text()
        return d