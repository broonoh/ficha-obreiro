# app/ui/widgets/field_row.py
"""Rótulo + campo, com o rótulo quebrando linha normalmente quando o
texto é longo (ex.: "29) Estado civil do candidato antes do casamento
atual") em vez de cortar.

Importante: não basta deixar o MDLabel quebrar linha sozinho (ele já
amarra text_size à própria largura por padrão) — o container (este
FieldRow/CheckRow) também precisa de altura DINÂMICA pra não cortar o
texto quando ele ocupa mais de uma linha, e esse recálculo só funciona
de forma confiável escutando tanto `width` quanto `texture_size` (igual
ao padrão já usado em SectionTitle nas telas) — escutar só texture_size
cria uma corrida: no primeiro frame a largura ainda é 0, o texto quebra
"errado" (uma letra por linha) calculando uma altura gigante, e se a
viewport mudar a largura depois sem um nova leitura de texture_size
nesse meio tempo, essa altura errada "gruda" e sobra um espaço vazio
enorme antes do conteúdo seguinte.

Era duplicado (com pequenas diferenças) em quase toda tela de
app/ui/screens/ — centralizado aqui pra evitar repetir a mesma correção
em vários lugares toda vez que aparecer um bug nela."""
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


def _normaliza(txt):
    return (txt or "").strip().rstrip(":").strip().lower()


class FieldRow(MDBoxLayout):
    """Rótulo (quebra linha) acima do campo. Se o hint_text do campo for
    idêntico ao rótulo, o hint é zerado pra não repetir o mesmo texto
    duas vezes (uma vez em cima, outra dentro do campo)."""

    def __init__(self, label_text, field, cor_rotulo=(0.012, 0.133, 0.247, 1), **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.spacing = dp(4)
        self.padding = [dp(4), dp(8), dp(4), dp(4)]

        self.lbl = MDLabel(
            text=label_text,
            font_style="Caption",
            theme_text_color="Custom",
            text_color=cor_rotulo,
            size_hint_y=None,
            height=dp(18),
            bold=True,
        )
        self.lbl.bind(width=self._resize_label, texture_size=self._resize_label)
        self.add_widget(self.lbl)

        hint = getattr(field, "hint_text", None)
        if hint and _normaliza(hint) == _normaliza(label_text):
            field.hint_text = ""
        self.field = field
        self.field.bind(height=self._resize_self)
        self.add_widget(field)

    def _resize_label(self, *_args):
        if self.lbl.width <= 0:
            return
        self.lbl.text_size = (self.lbl.width, None)
        self.lbl.texture_update()
        self.lbl.height = max(dp(18), self.lbl.texture_size[1])
        self._resize_self()

    def _resize_self(self, *_args):
        self.height = (
            self.padding[1]
            + self.lbl.height
            + self.spacing
            + self.field.height
            + self.padding[3]
        )


class CheckRow(MDBoxLayout):
    """Checkbox + pergunta, com a pergunta quebrando linha normalmente
    quando é longa — mesma ideia do FieldRow, mas pra perguntas de
    sim/não com checkbox em vez de campo de texto."""

    def __init__(self, text, checkbox, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.spacing = dp(12)
        self.padding = [dp(8), dp(6), dp(8), dp(6)]
        self.add_widget(checkbox)

        self.lbl = MDLabel(text=text, valign="middle", font_size="14sp", size_hint_y=None)
        self.lbl.bind(width=self._resize_label, texture_size=self._resize_label)
        self.add_widget(self.lbl)

    def _resize_label(self, *_args):
        if self.lbl.width <= 0:
            return
        self.lbl.text_size = (self.lbl.width, None)
        self.lbl.texture_update()
        self.lbl.height = max(dp(44), self.lbl.texture_size[1])
        self.height = self.lbl.height + self.padding[1] + self.padding[3]
