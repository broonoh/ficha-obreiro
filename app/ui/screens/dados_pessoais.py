# app/ui/screens/dados_pessoais.py
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from app.ui.widgets.photo_field import PhotoField
from app.ui.widgets.date_field import DateField
from app.ui.widgets.field_row import FieldRow


class SectionTitle(MDLabel):
    """Título de seção em vermelho ICM."""

    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.font_style = "Subtitle1"
        self.theme_text_color = "Custom"
        self.text_color = (0.706, 0.098, 0.149, 1)  # Vermelho ICM
        self.size_hint_y = None
        self.height = dp(36)
        self.bold = True
        self.padding = [dp(8), 0, 0, 0]
        self.bind(width=self._resize_to_text, texture_size=self._resize_to_text)

    def _resize_to_text(self, *_args):
        # Width 0 acontece no primeiro frame, antes do layout do pai
        # definir o tamanho real — calcular o texto nesse momento dá uma
        # altura sem sentido que podia "grudar" como um espaço vazio
        # enorme antes do título (o MDExpansionPanel só lê a altura do
        # conteúdo no instante em que abre).
        if self.width <= 0:
            return
        self.text_size = (self.width - self.padding[0] - self.padding[2], None)
        self.texture_update()
        self.height = max(dp(36), self.texture_size[1] + self.padding[1] + self.padding[3])


class DadosPessoaisContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(16)
        self.padding = dp(16)
        self.adaptive_height = True
        self.fields = {}

        # ═══════════════════════════════════════════════════
        # HEADER PRINCIPAL (azul marinho)
        # ═══════════════════════════════════════════════════
        self.add_widget(MDLabel(
            text="DADOS PESSOAIS",
            font_style="H5",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None,
            height=dp(48),
            bold=True,
        ))

        # ═══════════════════════════════════════════════════
        # FOTO 3x4
        # ═══════════════════════════════════════════════════
        self.photo_field = PhotoField()
        self.add_widget(self.photo_field)

        # ═══════════════════════════════════════════════════
        # 1. Informações Pessoais (APENAS UMA VEZ)
        # ══════════════════════════════════════════════════
        self.add_widget(SectionTitle("Informações Pessoais"))

        self.fields["nome"] = self._text("Nome")
        self.fields["idade"] = self._text("Idade")
        self.fields["data_nascimento"] = DateField(hint_text="Data de Nascimento")
        self.fields["estado_civil"] = self._text("Estado Civil")
        self.fields["escolaridade"] = self._text("Escolaridade")
        self.fields["profissao"] = self._text("Profissão")

        for f in [self.fields["nome"], self.fields["idade"], self.fields["data_nascimento"],
                  self.fields["estado_civil"], self.fields["escolaridade"], self.fields["profissao"]]:
            self.add_widget(FieldRow(f.hint_text, f))

        # ═══════════════════════════════════════════════════
        # 2. Endereço e Contato
        # ═══════════════════════════════════════════════════
        self.add_widget(SectionTitle("Endereço e Contato"))

        self.fields["endereco_rua"] = self._text("Rua")
        self.fields["endereco_bairro"] = self._text("Bairro")
        self.fields["endereco_cidade"] = self._text("Cidade")
        self.fields["endereco_uf"] = self._text("UF")
        self.fields["endereco_cep"] = self._text("CEP")
        self.fields["email"] = self._text("E-mail")
        self.fields["telefone"] = self._text("Tel")

        for f in [self.fields["endereco_rua"], self.fields["endereco_bairro"], self.fields["endereco_cidade"],
                  self.fields["endereco_uf"], self.fields["endereco_cep"], self.fields["email"],
                  self.fields["telefone"]]:
            self.add_widget(FieldRow(f.hint_text, f))

        # ═══════════════════════════════════════════════════
        # 3. Documentação e Dados Profissionais
        # ═══════════════════════════════════════════════════
        self.add_widget(SectionTitle("Documentação e Dados Profissionais"))

        self.fields["rg"] = self._text("Carteira de Identidade")
        self.fields["oe_orgao_emissor"] = self._text("OE (Órgão Emissor)")
        self.fields["cpf"] = self._text("C.P.F.")
        self.fields["empregado"] = self._text("Empregado")

        # Tempo de Emprego (Anos e Meses lado a lado)
        row_emprego = MDBoxLayout(size_hint_y=None, height=dp(80), spacing=dp(12))
        self.fields["tempo_emprego_anos"] = MDTextField(
            hint_text="Tempo de Emprego (ano(s))", mode="fill", input_filter="int"
        )
        self.fields["tempo_emprego_meses"] = MDTextField(
            hint_text="mês(es)", mode="fill", input_filter="int"
        )
        row_emprego.add_widget(self.fields["tempo_emprego_anos"])
        row_emprego.add_widget(self.fields["tempo_emprego_meses"])
        self.add_widget(row_emprego)

        self.fields["empresa"] = self._text("Empresa")

        for f in [self.fields["rg"], self.fields["oe_orgao_emissor"], self.fields["cpf"],
                  self.fields["empregado"], self.fields["empresa"]]:
            self.add_widget(FieldRow(f.hint_text, f))

        # ═══════════════════════════════════════════════════
        # 4. Dados Militares e Aposentadoria
        # ═══════════════════════════════════════════════════
        self.add_widget(SectionTitle("Dados Militares e Aposentadoria"))

        self.fields["militar_patente"] = self._text("Se Militar - Qual Patente")
        self.fields["arma"] = self._text("Arma")
        self.fields["aposentado_motivo"] = self._text("Se Aposentado (motivo aposentadoria)")

        for f in [self.fields["militar_patente"], self.fields["arma"], self.fields["aposentado_motivo"]]:
            self.add_widget(FieldRow(f.hint_text, f))

        # ═══════════════════════════════════════════════════
        # 5. Outras Informações
        # ═══════════════════════════════════════════════════
        self.add_widget(SectionTitle("Outras Informações"))

        self.fields["data_preenchimento"] = DateField(hint_text="Data de Preenchimento")
        self.fields["numero"] = self._text("Nº")

        for f in [self.fields["data_preenchimento"], self.fields["numero"]]:
            self.add_widget(FieldRow(f.hint_text, f))

    def _text(self, hint):
        return MDTextField(
            hint_text=hint,
            mode="fill",
            size_hint_y=None,
            height=dp(56),
            font_size="14sp",
        )

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        d["foto_base64"] = self.photo_field.get_photo_base64()
        d["foto_path"] = self.photo_field.get_photo_path()  # 添加这一行
        return d