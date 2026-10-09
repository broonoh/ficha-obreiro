# main.py
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.snackbar import Snackbar

# Imports dos serviços de banco de dados e carregamento de UI
from app.services.storage import salvar_rascunho_no_bd, carregar_rascunho_do_bd
from app.services.ui_loader import populate_screen

from app.ui.screens import (
    DadosPessoaisContent, VidaEspiritualContent, AreaPastorContent,
    ExperienciasGracaContent, ExperienciasObreiroContent, MensagensContent,
    QuestionarioContent, QuestionarioEsposaContent
)

KV = """
MDScreen:
    md_bg_color: 0.973, 0.969, 0.953, 1  # creme ICM (#f8f7f3)

    MDBoxLayout:
        orientation: "vertical"

        # ═══════════════════════════════════════════════════
        # HEADER COM BOTÃO DE SAIR
        # ══════════════════════════════════════════════════
        MDTopAppBar:
            title: "Ficha de Obreiro — ICM"
            elevation: 4
            md_bg_color: 0.012, 0.133, 0.247, 1  # azul marinho
            specific_text_color: 1, 1, 1, 1
            title_font_style: "H5"
            left_action_items: []
            right_action_items: [["exit-to-app", lambda x: app.sair_do_app()]]

        # ═══════════════════════════════════════════════════
        # CONTEÚDO COM SCROLLBAR VISÍVEL
        # ═══════════════════════════════════════════════════
        ScrollView:
            do_scroll_x: False
            bar_color: 0.706, 0.098, 0.149, 0.8  # vermelho ICM semi-transparente
            bar_inactive_color: 0.706, 0.098, 0.149, 0.3  # vermelho bem claro
            bar_width: dp(10)
            scroll_type: ["bars", "content"]

            MDBoxLayout:
                orientation: "vertical"
                id: box_expansions
                padding: dp(16)
                spacing: dp(12)
                adaptive_height: True

        # ═══════════════════════════════════════════════════
        # FOOTER COM BOTÕES
        # ═══════════════════════════════════════════════════
        MDCard:
            size_hint_y: None
            height: dp(72)
            padding: dp(12)
            radius: [12, 12, 0, 0]
            elevation: 8
            md_bg_color: 1, 1, 1, 1

            MDBoxLayout:
                spacing: dp(10)

                MDRaisedButton:
                    text: "  SALVAR"
                    md_bg_color: 0.706, 0.098, 0.149, 1  # vermelho ICM
                    font_style: "Button"
                    on_release: app.salvar_rascunho()

                MDRaisedButton:
                    text: "   GERAR PDF"
                    md_bg_color: 0.831, 0.627, 0.090, 1  # dourado
                    font_style: "Button"
                    on_release: app.gerar_pdf()

                MDRaisedButton:
                    text: "   SAIR"
                    md_bg_color: 0.012, 0.133, 0.247, 1  # azul marinho
                    font_style: "Button"
                    on_release: app.sair_do_app()
"""


class FichaObreiroApp(MDApp):
    _panels_content = []

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "900"
        return Builder.load_string(KV)

    def on_start(self):
        # Ícones SEM CRUZ - Material Design Icons
        secoes = [
            ("DADOS PESSOAIS", "account-circle-outline", DadosPessoaisContent),
            ("VIDA ESPIRITUAL", "book-open-page-variant", VidaEspiritualContent),
            ("ÁREA DO PASTOR RESPONSÁVEL", "clipboard-text-clock", AreaPastorContent),
            ("EXPERIÊNCIAS COM RECURSOS DA GRAÇA", "water-percent", ExperienciasGracaContent),
            ("EXPERIÊNCIAS DO OBREIRO", "script-text-outline", ExperienciasObreiroContent),
            ("MENSAGENS REVELADAS", "fire", MensagensContent),
            ("QUESTIONÁRIO", "school-outline", QuestionarioContent),
            ("QUESTIONÁRIO PARA ESPOSAS DOS UNGIDOS", "account-group-outline", QuestionarioEsposaContent),
        ]

        box = self.root.ids.box_expansions
        for titulo, icone, ContentClass in secoes:
            content = ContentClass()
            self._panels_content.append(content)

            panel = MDExpansionPanel(
                icon=icone,
                content=content,
                panel_cls=MDExpansionPanelOneLine(
                    text=titulo,
                    font_style="Subtitle1",
                ),
            )
            box.add_widget(panel)

        # 🚀 NOVO: Carregar rascunho salvo automaticamente ao iniciar
        print("🔄 Carregando rascunho salvo...")
        dados_salvos = carregar_rascunho_do_bd()
        if dados_salvos:
            for content in self._panels_content:
                populate_screen(content, dados_salvos)
            Snackbar(text="✅ Rascunho anterior carregado!").open()

    def coletar_todos_dados(self):
        dados = {}
        for content in self._panels_content:
            if hasattr(content, "to_dict"):
                dados.update(content.to_dict())
        return dados

    def salvar_rascunho(self):
        dados = self.coletar_todos_dados()

        # 🚀 NOVO: Salvar de verdade no banco de dados (SQLite)
        if salvar_rascunho_no_bd(dados):
            Snackbar(text="✅ Rascunho salvo no banco de dados!").open()
            print("💾 Dados persistidos com sucesso.")
        else:
            Snackbar(text="❌ Erro ao salvar.").open()

    def gerar_pdf(self):
        dados = self.coletar_todos_dados()
        try:
            from app.services.pdf_generator import gerar_pdf
            path = gerar_pdf(dados)
            Snackbar(text=f"✅ PDF gerado: {path}").open()
        except Exception as e:
            Snackbar(text=f"❌ Erro ao gerar PDF: {e}").open()

    def sair_do_app(self):
        """Fecha o aplicativo com confirmação."""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton

        dialog = MDDialog(
            title="Sair do aplicativo?",
            text="Tem certeza que deseja sair? Certifique-se de ter clicado em 'SALVAR' antes.",
            buttons=[
                MDFlatButton(
                    text="CANCELAR",
                    on_release=lambda x: dialog.dismiss(),
                ),
                MDFlatButton(
                    text="SAIR",
                    text_color=(0.706, 0.098, 0.149, 1),  # vermelho ICM
                    on_release=lambda x: self.stop(),
                ),
            ],
        )
        dialog.open()


if __name__ == "__main__":
    FichaObreiroApp().run()