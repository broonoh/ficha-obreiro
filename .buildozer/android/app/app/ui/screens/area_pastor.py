# app/ui/screens/area_pastor.py
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from app.ui.widgets.dropdown_field import DropdownField
from app.ui.widgets.limited_text_field import LimitedTextField
from app.ui.widgets.field_row import FieldRow, CheckRow


class SectionTitle(MDLabel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = f" {text}"
        self.font_style = "Subtitle1"
        self.theme_text_color = "Custom"
        self.text_color = (0.706, 0.098, 0.149, 1)
        self.size_hint_y = None
        self.height = dp(36)
        self.bold = True
        self.padding = [dp(8), 0, 0, 0]
        self.bind(width=self._resize_to_text, texture_size=self._resize_to_text)

    def _resize_to_text(self, *_args):
        # Ver comentário equivalente em experiencias.py: width 0 no
        # primeiro frame gera uma altura sem sentido que podia "grudar"
        # como um espaço vazio enorme antes do título.
        if self.width <= 0:
            return
        self.text_size = (self.width - self.padding[0] - self.padding[2], None)
        self.texture_update()
        self.height = max(dp(36), self.texture_size[1] + self.padding[1] + self.padding[3])


class AreaPastorContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(10)
        self.padding = dp(12)
        self.adaptive_height = True
        self.fields = {}
        self.checks = {}
        self.checks_touched = {}
        self.dropdowns = {}
        self.limited_fields = {}

        self.add_widget(MDLabel(
            text="ÁREA RESERVADA AO PREENCHIMENTO DO PASTOR RESPONSÁVEL",
            font_style="H6", theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None, height=dp(50), bold=True,
        ))

        # Igreja / Cidade / UF
        self.add_widget(SectionTitle("IGREJA / CIDADE / UF"))
        row_loc = MDBoxLayout(size_hint_y=None, height=dp(80), spacing=dp(12))
        self.fields["pastor_igreja"] = MDTextField(hint_text="IGREJA", mode="fill")
        self.fields["pastor_cidade"] = MDTextField(hint_text="CIDADE", mode="fill")
        self.fields["pastor_uf"] = MDTextField(hint_text="UF", mode="fill")
        row_loc.add_widget(self.fields["pastor_igreja"])
        row_loc.add_widget(self.fields["pastor_cidade"])
        row_loc.add_widget(self.fields["pastor_uf"])
        self.add_widget(row_loc)

        # 01) Função - agora é campo de digitação (label + input)
        self.add_widget(SectionTitle("FUNÇÃO"))
        self.fields["funcao_apresentada"] = MDTextField(
            hint_text="01) FUNÇÃO A SER APRESENTADO",
            mode="fill",
            size_hint_y=None,
            height=dp(56),
            font_size="14sp",
        )
        self.add_widget(FieldRow("01) FUNÇÃO A SER APRESENTADO", self.fields["funcao_apresentada"]))

        # 02-04
        self.add_widget(SectionTitle("MINISTÉRIO"))
        self.limited_fields["caracteristica_ministerio"] = LimitedTextField(
            label_text="02) CARACTERÍSTICA DO MINISTÉRIO",
            hint_text="Descreva a característica do ministério...",
            max_chars=1000,
        )
        self.add_widget(self.limited_fields["caracteristica_ministerio"])
        self._add_check("03) TEM MENSAGEM REVELADA? (FOLHA ANEXA)", "tem_mensagem_revelada")
        self._add_check("04) TRANSMITE BEM A MENSAGEM?", "transmite_bem_mensagem")

        # 05-10
        self.add_widget(SectionTitle("CARÁTER E TESTEMUNHO"))
        self.fields["defeito"] = MDTextField(hint_text="05) DEFEITO (TÍMIDO/AFOITO/LENTO/RÍGIDO, ETC)", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(FieldRow("05) DEFEITO (TÍMIDO/AFOITO/LENTO/RÍGIDO, ETC)", self.fields["defeito"]))
        self._add_check("06) TEM BOM TESTEMUNHO?", "tem_bom_testemunho")
        self._add_check("07) TEM MATURIDADE NOS DONS?", "maturidade_dons")
        self._add_check("08) GOSTA DE IMITAR MOVIMENTOS?", "gosta_imitar_movimentos")
        self._add_check("09) É GASTADOR?", "e_gastador")
        self._add_check("10) É DADO A COMENTÁRIOS DEPRECIATIVOS?", "dado_comentarios_depreciativos")
        self.fields["comentarios_depreciativos_quais"] = MDTextField(hint_text="QUAIS?", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(self.fields["comentarios_depreciativos_quais"])

        # 11-14
        self.add_widget(SectionTitle("CONDUTA E CONTEXTO"))
        self._add_check("11) É PONTUAL?", "pontual")
        self._add_check("12) É SÓBRIO NO VESTIR?", "sobrio_vestir")
        row13 = MDBoxLayout(size_hint_y=None, spacing=dp(12))
        row13.bind(minimum_height=row13.setter("height"))
        self.fields["numero_igrejas_bairro"] = MDTextField(hint_text="13) Nº IGREJAS NO BAIRRO OU CIDADE?", mode="fill", input_filter="int")
        self.fields["numero_pastores_bairro"] = MDTextField(hint_text="14) Nº PASTORES NO BAIRRO OU CIDADE?", mode="fill", input_filter="int")
        row13.add_widget(FieldRow("13) Nº IGREJAS NO BAIRRO OU CIDADE?", self.fields["numero_igrejas_bairro"]))
        row13.add_widget(FieldRow("14) Nº PASTORES NO BAIRRO OU CIDADE?", self.fields["numero_pastores_bairro"]))
        self.add_widget(row13)

        # 15-17
        self.add_widget(SectionTitle("OBEDIÊNCIA E HISTÓRICO"))
        self._add_check("15) OBEDIENTE AOS DONS RELACIONADOS À SUA VIDA OU FAMÍLIA?", "obediente_dons")
        self.fields["obediente_dons_quais"] = MDTextField(hint_text="OUTRA(S)? QUAIS?", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(self.fields["obediente_dons_quais"])

        self._add_check("16) JÁ FOI APRESENTADO ALGUMA VEZ PARA ESTA FUNÇÃO?", "ja_apresentado_antes")
        row16 = MDBoxLayout(size_hint_y=None, height=dp(80), spacing=dp(12))
        self.fields["quantas_vezes_apresentado"] = MDTextField(hint_text="SE SIM, QUANTAS?", mode="fill", input_filter="int")
        self.fields["ano_apresentacao"] = MDTextField(hint_text="ANO DA APRESENTAÇÃO?", mode="fill", input_filter="int")
        row16.add_widget(self.fields["quantas_vezes_apresentado"])
        row16.add_widget(self.fields["ano_apresentacao"])
        self.add_widget(row16)

        self.limited_fields["motivo_nao_aprovado"] = LimitedTextField(
            label_text="CASO NÃO TENHA SIDO APROVADO, FAVOR INFORMAR O MOTIVO:",
            hint_text="Informe o motivo...",
            max_chars=1000,
        )
        self.add_widget(self.limited_fields["motivo_nao_aprovado"])

        self.fields["igreja_assumira"] = MDTextField(
            hint_text="17) QUAL IGREJA O CANDIDATO IRÁ ASSUMIR EM CASO DE ORDENAÇÃO?",
            mode="fill", size_hint_y=None, height=dp(48)
        )
        self.add_widget(FieldRow("17) QUAL IGREJA O CANDIDATO IRÁ ASSUMIR EM CASO DE ORDENAÇÃO?", self.fields["igreja_assumira"]))

        self.limited_fields["observacao_pastor"] = LimitedTextField(
            label_text="OBSERVAÇÃO DO PASTOR RESPONSÁVEL / DOM DA IGREJA:",
            hint_text="Descreva a observação...",
            max_chars=1000,
        )
        self.add_widget(self.limited_fields["observacao_pastor"])

        self.fields["assinatura_pastor"] = MDTextField(
            hint_text="ASSINATURA DO PASTOR RESPONSÁVEL (INDISPENSÁVEL)",
            mode="fill", size_hint_y=None, height=dp(48)
        )
        self.add_widget(FieldRow("ASSINATURA DO PASTOR RESPONSÁVEL (INDISPENSÁVEL)", self.fields["assinatura_pastor"]))

    def _add_check(self, text, key):
        cb = MDCheckbox(active=False, size_hint_x=None, width=dp(48))
        self.checks[key] = cb
        self.checks_touched[key] = False
        cb.bind(active=lambda *_a, k=key: self.checks_touched.__setitem__(k, True))
        self.add_widget(CheckRow(text, cb))

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        for k, lf in self.limited_fields.items():
            d[k] = lf.get_text()
        # Checkbox não tocado pelo usuário vira None (não preenchido), em vez
        # de False, para o PDF não exibir "Não" em campo que ninguém respondeu.
        for k, cb in self.checks.items():
            d[k] = cb.active if self.checks_touched.get(k) else None
        return d