# app/ui/screens/vida_espiritual.py
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.label import MDLabel
from app.ui.widgets.dropdown_field import DropdownField
from app.ui.widgets.date_field import DateField
from app.ui.widgets.field_row import FieldRow, CheckRow


class SectionTitle(MDLabel):
    def __init__(self, text, **kwargs):
        super().__init__(**kwargs)
        self.text = f"▸ {text}"
        self.font_style = "Subtitle1"
        self.theme_text_color = "Custom"
        self.text_color = (0.706, 0.098, 0.149, 1)
        self.size_hint_y = None
        self.height = dp(36)
        self.bold = True
        self.padding = [dp(8), 0, 0, 0]
        self.bind(width=self._resize_to_text, texture_size=self._resize_to_text)

    def _resize_to_text(self, *_args):
        if self.width <= 0:
            return
        self.text_size = (self.width - self.padding[0] - self.padding[2], None)
        self.texture_update()
        self.height = max(dp(36), self.texture_size[1] + self.padding[1] + self.padding[3])


class VidaEspiritualContent(MDBoxLayout):
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

        # Header
        self.add_widget(MDLabel(
            text="ÁREA RESERVADA AO PREENCHIMENTO DO \"OBREIRO\" APRESENTADO",
            font_style="H6",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None,
            height=dp(50),
            bold=True,
        ))

        # ── 01-02: Função e Tempo ──────────────────────────
        self.add_widget(SectionTitle("FUNÇÃO E TEMPO"))

        self.dropdowns["funcao_atual"] = DropdownField(
            "01) FUNÇÃO ATUAL: EVANGELISTA, OBREIRO, DIÁCONO OU UNGIDO?",
            ["Evangelista", "Obreiro", "Diácono", "Ungido"]
        )
        self.add_widget(self.dropdowns["funcao_atual"])

        row_tempo = MDBoxLayout(size_hint_y=None, height=dp(80), spacing=dp(12))
        self.fields["tempo_funcao_anos"] = MDTextField(hint_text="02) ANO(S)", mode="fill", input_filter="int")
        self.fields["tempo_funcao_meses"] = MDTextField(hint_text="MÊS(ES)", mode="fill", input_filter="int")
        row_tempo.add_widget(self.fields["tempo_funcao_anos"])
        row_tempo.add_widget(self.fields["tempo_funcao_meses"])
        self.add_widget(row_tempo)

        # ─ 03-07: Ministério ──────────────────────────────
        self.add_widget(SectionTitle("MINISTÉRIO E SERVIÇO"))

        self._add_check("03) GRUPO DE INTERCESSÃO?", "grupo_intercessao")
        self._add_check("04) É RESPONSÁVEL POR TRABALHO/IGREJA?", "responsavel_trabalho")
        self.fields["responsavel_trabalho_qual"] = MDTextField(hint_text="SE SIM, QUAL?", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(self.fields["responsavel_trabalho_qual"])

        self.fields["crescimento_grupo_pct"] = MDTextField(
            hint_text="05) CRESCIMENTO (OU NÃO) DE SEU GRUPO ASSISTÊNCIA OU IGREJA (%)",
            mode="fill", input_filter="float", size_hint_y=None, height=dp(48)
        )
        self.fields["visitas_mes"] = MDTextField(
            hint_text="06) FAZ QUANTAS VISITAS POR MÊS AOS IRMÃOS DA IGREJA?",
            mode="fill", input_filter="int", size_hint_y=None, height=dp(48)
        )
        self.add_widget(FieldRow(
            "05) CRESCIMENTO (OU NÃO) DE SEU GRUPO ASSISTÊNCIA OU IGREJA (%)",
            self.fields["crescimento_grupo_pct"],
        ))
        self.add_widget(FieldRow(
            "06) FAZ QUANTAS VISITAS POR MÊS AOS IRMÃOS DA IGREJA?",
            self.fields["visitas_mes"],
        ))

        self._add_check("07) É DIZIMISTA FIEL?", "dizimista_fiel")

        # ── 08-09: Tempo ICM e Afastamento ─────────────────
        self.add_widget(SectionTitle("TEMPO NA ICM E HISTÓRICO"))

        row_icm = MDBoxLayout(size_hint_y=None, height=dp(80), spacing=dp(12))
        self.fields["tempo_icm_anos"] = MDTextField(hint_text="08) ANO(S)", mode="fill", input_filter="int")
        self.fields["tempo_icm_meses"] = MDTextField(hint_text="MÊS(ES)", mode="fill", input_filter="int")
        row_icm.add_widget(self.fields["tempo_icm_anos"])
        row_icm.add_widget(self.fields["tempo_icm_meses"])
        self.add_widget(row_icm)

        self._add_check("09) JÁ AFASTOU-SE DA IGREJA POR ALGUM MOTIVO?", "afastou_igreja")
        self.fields["afastou_igreja_motivo"] = MDTextField(hint_text="MOTIVO", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(self.fields["afastou_igreja_motivo"])

        row_datas = MDBoxLayout(size_hint_y=None, height=dp(80), spacing=dp(12))
        self.fields["afastou_data1"] = DateField(hint_text="DATA")
        self.fields["afastou_data2"] = DateField(hint_text="DATA")
        self.fields["afastou_data3"] = DateField(hint_text="DATA")
        row_datas.add_widget(self.fields["afastou_data1"])
        row_datas.add_widget(self.fields["afastou_data2"])
        row_datas.add_widget(self.fields["afastou_data3"])
        self.add_widget(row_datas)

        # ── 10-13: Provas e Experiências ──────────────────
        self.add_widget(SectionTitle("PROVAS E EXPERIÊNCIAS"))

        self._add_check("10) FOI PROVADO? (FOLHA ANEXA)", "foi_provado")
        self.fields["foi_provado_qual"] = MDTextField(hint_text="QUAIS?", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(self.fields["foi_provado_qual"])

        self._add_check("11) TEM EXPERIÊNCIA? (FOLHA ANEXA)", "tem_experiencia")
        self.fields["tem_sequelas_passado"] = MDTextField(hint_text="12) TEM SEQÜELAS DO PASSADO?", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(FieldRow("12) TEM SEQÜELAS DO PASSADO?", self.fields["tem_sequelas_passado"]))

        self.add_widget(MDLabel(
            text="13) ÚLTIMOS SEMINÁRIOS",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None,
            height=dp(18),
            bold=True,
        ))
        row_seminarios = MDBoxLayout(size_hint_y=None, height=dp(56), spacing=dp(20))
        self.fields["ultimo_seminario1"] = DateField(hint_text="1º Seminário")
        self.fields["ultimo_seminario2"] = DateField(hint_text="2º Seminário")
        self.fields["ultimo_seminario3"] = DateField(hint_text="3º Seminário")
        row_seminarios.add_widget(self.fields["ultimo_seminario1"])
        row_seminarios.add_widget(self.fields["ultimo_seminario2"])
        row_seminarios.add_widget(self.fields["ultimo_seminario3"])
        self.add_widget(row_seminarios)

        # ── 14: Maanaim ────────────────────────────────────
        self.add_widget(SectionTitle("14) PARTICIPAÇÃO NO MAANAIM/IGREJA"))

        row_maanaim = MDBoxLayout(size_hint_y=None, height=dp(70), spacing=dp(8))
        for label, key in [
            ("VOLUNTÁRIO", "participa_maanaim_voluntario"),
            ("MEIO SEMANA", "participa_maanaim_meio_semana"),
            ("FINAL SEMANA", "participa_maanaim_final_semana"),
        ]:
            cb = MDCheckbox(active=False)
            self.checks[key] = cb
            col = MDBoxLayout(orientation="vertical", size_hint_x=1)
            col.add_widget(MDLabel(text=label, halign="center", font_style="Caption"))
            col.add_widget(cb)
            row_maanaim.add_widget(col)
        self.add_widget(row_maanaim)

        # ── 15-20: Vida devocional e caráter ───────────────
        self.add_widget(SectionTitle("VIDA DEVOCIONAL E CARÁTER"))

        self._add_check("15) PARTICIPA DOS CULTOS DE MADRUGADA?", "participa_madrugada")
        self._add_check("16) É INTEGRADO AO CULTO PROFÉTICO?", "integrado_culto_profetico")
        self._add_check("17) TEM GOVERNO NO LAR E NA IGREJA?", "tem_governo_lar")
        self._add_check("18) A FAMÍLIA É INTEGRADA NA ICM?", "familia_integrada")
        self._add_check("19) RESPEITA O PASTOR E AO PRESBITÉRIO?", "respeita_pastor_presbiterio")
        self._add_check("20) É ZELOSO COM OS BENS DA ICM?", "zelo_bens_icm")

        # ── 21: Dons ───────────────────────────────────────
        self.add_widget(SectionTitle("21) DONS ESPIRITUAIS"))

        dons_row = MDBoxLayout(size_hint_y=None, height=dp(70), spacing=dp(6))
        for label, key in [
            ("LÍNGUAS", "dons_linguas"),
            ("INTERPRETAÇÃO", "dons_interpretacao"),
            ("CIÊNCIA", "dons_ciencia"),
            ("SONHO", "dons_sonho"),
            ("VISÃO", "dons_visao"),
            ("REVELAÇÃO", "dons_revelacao"),
            ("NÃO", "dons_nenhum"),
        ]:
            col = MDBoxLayout(orientation="vertical", size_hint_x=1)
            cb = MDCheckbox(active=False)
            self.checks[key] = cb
            col.add_widget(cb)
            col.add_widget(MDLabel(text=label, halign="center", font_size="10sp"))
            dons_row.add_widget(col)
        self.add_widget(dons_row)

        # ── 22-24: Histórico ───────────────────────────────
        self.add_widget(SectionTitle("HISTÓRICO"))

        self.fields["veio_outra_igreja"] = MDTextField(hint_text="22) VEIO DE OUTRA IGREJA (DENOMINAÇÃO)? QUAL?", mode="fill", size_hint_y=None, height=dp(48))
        self._add_check("23) É CUMPRIDOR DE SUAS OBRIGAÇÕES NO SEU TRABALHO?", "cumpridor_obrigacoes")
        self._add_check("24) TEM DÍVIDA COM IRMÃOS DA IGREJA?", "divida_irmaos")
        self.add_widget(FieldRow("22) VEIO DE OUTRA IGREJA (DENOMINAÇÃO)? QUAL?", self.fields["veio_outra_igreja"]))

        # ── 25-32: Família ─────────────────────────────────
        self.add_widget(SectionTitle("FAMÍLIA"))

        self.fields["tempo_casado"] = MDTextField(
            hint_text="25) TEMPO DE CASADO (CANDIDATO E ESPOSA)", mode="fill",
            size_hint_y=None, height=dp(48),
        )
        self.add_widget(FieldRow("25) TEMPO DE CASADO (CANDIDATO E ESPOSA)", self.fields["tempo_casado"]))

        self.fields["nome_esposa"] = MDTextField(hint_text="26) NOME DA ESPOSA:", mode="fill", size_hint_y=None, height=dp(48))
        self.fields["funcao_esposa"] = MDTextField(hint_text="27) FUNÇÃO DA ESPOSA NA IGREJA:", mode="fill", size_hint_y=None, height=dp(48))
        self.fields["profissao_esposa"] = MDTextField(hint_text="28) PROFISSÃO DA ESPOSA", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(FieldRow("26) NOME DA ESPOSA:", self.fields["nome_esposa"]))
        self.add_widget(FieldRow("27) FUNÇÃO DA ESPOSA NA IGREJA:", self.fields["funcao_esposa"]))
        self.add_widget(FieldRow("28) PROFISSÃO DA ESPOSA", self.fields["profissao_esposa"]))

        self.fields["estado_civil_antes_candidato"] = MDTextField(hint_text="29) ESTADO CIVIL DO CANDIDATO ANTES DO CASAMENTO ATUAL", mode="fill", size_hint_y=None, height=dp(48))
        self.fields["estado_civil_antes_esposa"] = MDTextField(hint_text="30) ESTADO CIVIL DA ESPOSA ANTES DO CASAMENTO ATUAL", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(FieldRow("29) ESTADO CIVIL DO CANDIDATO ANTES DO CASAMENTO ATUAL", self.fields["estado_civil_antes_candidato"]))
        self.add_widget(FieldRow("30) ESTADO CIVIL DA ESPOSA ANTES DO CASAMENTO ATUAL", self.fields["estado_civil_antes_esposa"]))

        # size_hint_y=None + bind(minimum_height=...) em vez de uma altura
        # fixa: os dois FieldRow dentro da linha têm altura dinâmica (o
        # rótulo pode quebrar em mais de uma linha), e uma altura fixa
        # cortava o conteúdo sempre que isso acontecia.
        row_filhos = MDBoxLayout(size_hint_y=None, spacing=dp(12))
        row_filhos.bind(minimum_height=row_filhos.setter("height"))
        self.fields["quantos_filhos"] = MDTextField(hint_text="31) QUANTOS FILHOS TEM?", mode="fill", input_filter="int")
        self.fields["quantos_membros_igreja"] = MDTextField(hint_text="QUANTOS SÃO MEMBROS IGREJA?", mode="fill", input_filter="int")
        row_filhos.add_widget(FieldRow("31) QUANTOS FILHOS TEM?", self.fields["quantos_filhos"]))
        row_filhos.add_widget(FieldRow("QUANTOS SÃO MEMBROS IGREJA?", self.fields["quantos_membros_igreja"]))
        self.add_widget(row_filhos)

        self.fields["filhos_motivo_sem"] = MDTextField(hint_text="32) CASO NÃO TENHA FILHOS, QUAL MOTIVO?", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(FieldRow("32) CASO NÃO TENHA FILHOS, QUAL MOTIVO?", self.fields["filhos_motivo_sem"]))

        # ── 33-41: Formação e prática ──────────────────────
        self.add_widget(SectionTitle("FORMAÇÃO E PRÁTICA"))

        self._add_check("33) DISPOSTO A DESEMPENHAR MINISTÉRIO VOLUNTÁRIO?", "disposto_ministerio_voluntario")
        self._add_check("34) LEU TODA A BÍBLIA?", "leu_toda_biblia")
        self.fields["livros_lidos"] = MDTextField(hint_text="CASO NÃO TENHA LIDO, QUANTOS LIVROS LEU?", mode="fill", input_filter="int", size_hint_y=None, height=dp(48))
        self.add_widget(FieldRow("CASO NÃO TENHA LIDO, QUANTOS LIVROS LEU?", self.fields["livros_lidos"]))

        self._add_check("35) COLOCA EM PRÁTICA ENSINOS DO SATÉLITE E EBD?", "pratica_ensinos_satelite")
        self._add_check("36) APLICA OS ASSUNTOS DO SATÉLITE NA IGREJA?", "aplica_satelite_igreja")
        self._add_check("37) CONCLUIU O CURSO DO INSTITUTO BÍBLICO?", "concluiu_instituto_biblico")
        self.fields["curso_realizado"] = MDTextField(hint_text="QUAL CURSO:", mode="fill", size_hint_y=None, height=dp(48))
        self.add_widget(self.fields["curso_realizado"])

        self.fields["frequencia_media_igreja"] = MDTextField(hint_text="38) FREQUÊNCIA MÉDIA DA SUA IGREJA:", mode="fill", input_filter="int", size_hint_y=None, height=dp(48))
        self._add_check_sim_nao("39) ESTUDA NOITE?", "estuda_noite")
        self._add_check("40) DISPOSTO A REALIZAR VIAGEM?", "disposto_viagem")
        self.fields["contribuicoes_ebd_mes"] = MDTextField(hint_text="41) ENVIA QUANTAS CONTRIBUIÇÕES DA EBD POR MÊS?", mode="fill", input_filter="int", size_hint_y=None, height=dp(48))
        self.add_widget(FieldRow("38) FREQUÊNCIA MÉDIA DA SUA IGREJA:", self.fields["frequencia_media_igreja"]))
        self.add_widget(FieldRow("41) ENVIA QUANTAS CONTRIBUIÇÕES DA EBD POR MÊS?", self.fields["contribuicoes_ebd_mes"]))

    def _add_check(self, text, key):
        cb = MDCheckbox(active=False, size_hint_x=None, width=dp(48))
        self.checks[key] = cb
        self.checks_touched[key] = False
        cb.bind(active=lambda *_a, k=key: self.checks_touched.__setitem__(k, True))
        self.add_widget(CheckRow(text, cb))

    def _add_check_sim_nao(self, text, key):
        """Pergunta com dois checkboxes (SIM / NÃO) mutuamente exclusivos."""
        row = MDBoxLayout(size_hint_y=None, height=dp(56), spacing=dp(12), padding=[dp(8), 0, 0, 0])
        row.add_widget(MDLabel(text=text, valign="middle", font_size="14sp"))

        group_name = f"group_{key}"

        sim_box = MDBoxLayout(size_hint_x=None, width=dp(90), spacing=dp(4))
        cb_sim = MDCheckbox(active=False, group=group_name, size_hint_x=None, width=dp(36))
        sim_box.add_widget(cb_sim)
        sim_box.add_widget(MDLabel(text="SIM", valign="middle", size_hint_x=None, width=dp(44)))
        row.add_widget(sim_box)

        nao_box = MDBoxLayout(size_hint_x=None, width=dp(90), spacing=dp(4))
        cb_nao = MDCheckbox(active=False, group=group_name, size_hint_x=None, width=dp(36))
        nao_box.add_widget(cb_nao)
        nao_box.add_widget(MDLabel(text="NÃO", valign="middle", size_hint_x=None, width=dp(44)))
        row.add_widget(nao_box)

        self.checks[f"{key}_sim"] = cb_sim
        self.checks[f"{key}_nao"] = cb_nao
        self.add_widget(row)

    def to_dict(self):
        d = {k: v.text for k, v in self.fields.items()}
        for k, dd in self.dropdowns.items():
            d[k] = dd.get_value()
        # Checkbox de pergunta Sim/Não não tocado vira None (não preenchido),
        # em vez de False, para o PDF não exibir "Não" sem o usuário responder.
        # Chips de seleção múltipla (maanaim/dons) e pares Sim/Não mutuamente
        # exclusivos não entram em checks_touched e mantêm o valor bruto.
        for k, cb in self.checks.items():
            if k in self.checks_touched:
                d[k] = cb.active if self.checks_touched[k] else None
            else:
                d[k] = cb.active
        return d