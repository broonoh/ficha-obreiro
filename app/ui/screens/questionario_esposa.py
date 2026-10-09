# app/ui/screens/questionario_esposa.py
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
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


class QuestionarioEsposaContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(16)
        self.padding = dp(16)
        self.adaptive_height = True
        self.fields = {}
        self.limited_fields = {}

        self.add_widget(SectionTitle("QUESTIONÁRIO PARA ESPOSAS DOS UNGIDOS — FAZER BREVE COMENTÁRIO SOBRE OS ITENS ABAIXO"))

        # "Nome da Esposa" já é coletado em Vida Espiritual (item 26) — não
        # repetir o campo aqui. Tinha a MESMA chave "nome_esposa" nas duas
        # telas, e como essa tela é processada por último ao salvar/gerar o
        # PDF, ela sempre apagava o valor digitado em Vida Espiritual.

        perguntas = [
            ("q1_acordo_ordenacao", "1- Você está de acordo com a ordenação de seu esposo e o seu propósito para o ministério? Faça um breve comentário."),
            ("q2_concorda_doutinas", "2- Você concorda com as doutrinas e orientações do Presbitério? Faça um breve comentário."),
            ("q3_ministerio_voluntario", "3- Você concorda com o ministério voluntário? Faça um breve comentário."),
            ("q4_nao_interferir", "4- Você entende que não deve interferir no ministério do seu esposo? Faça um breve comentário."),
            ("q5_outros", "5- Faça outros comentários, se achar necessário."),
        ]
        for key, pergunta in perguntas:
            ltf = LimitedTextField(
                label_text=pergunta,
                hint_text="Comentário...",
                max_chars=1000,
            )
            self.limited_fields[key] = ltf
            self.add_widget(ltf)

        self.fields["assinatura_esposa"] = MDTextField(
            hint_text="ASSINATURA DA ESPOSA:", mode="fill", size_hint_y=None, height=dp(56)
        )
        self.add_widget(self.fields["assinatura_esposa"])

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        for k, lf in self.limited_fields.items():
            d[k] = lf.get_text()
        return d