# main.py
import os
import traceback
from pathlib import Path
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.snackbar import Snackbar

# Imports dos serviços de banco de dados e carregamento de UI
from app.services.storage import (
    salvar_rascunho_no_bd, carregar_rascunho_do_bd,
    exportar_dados_para_arquivo, importar_dados_de_arquivo,
)
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
            height: dp(116)
            padding: dp(8)
            radius: [12, 12, 0, 0]
            elevation: 8
            md_bg_color: 1, 1, 1, 1

            AnchorLayout:
                # MDCard herda de BoxLayout, que ignora pos_hint — por isso
                # a centralização do bloco de botões precisa de um
                # AnchorLayout (que entende anchor_x) como filho direto.
                anchor_x: "center"
                anchor_y: "center"

                MDBoxLayout:
                    # Largura do rodapé limitada e centralizada: em telas
                    # largas (desktop) evita que os botões fiquem
                    # esticados/gigantes ocupando a janela inteira; em
                    # telas estreitas (celular) o teto de dp(640) nunca é
                    # atingido, então ocupa 100% e mantém o comportamento
                    # responsivo que evita corte de texto.
                    size_hint_x: None
                    width: min(dp(640), self.parent.width)
                    orientation: "vertical"
                    spacing: dp(6)

                    MDBoxLayout:
                        spacing: dp(6)

                        MDRaisedButton:
                            text: "SALVAR"
                            size_hint_x: 1
                            font_size: "12sp"
                            md_bg_color: 0.706, 0.098, 0.149, 1  # vermelho ICM
                            on_release: app.salvar_rascunho()

                        MDRaisedButton:
                            text: "GERAR PDF"
                            size_hint_x: 1
                            font_size: "12sp"
                            md_bg_color: 0.831, 0.627, 0.090, 1  # dourado
                            on_release: app.gerar_pdf()

                        MDRaisedButton:
                            text: "SAIR"
                            size_hint_x: 1
                            font_size: "12sp"
                            md_bg_color: 0.012, 0.133, 0.247, 1  # azul marinho
                            on_release: app.sair_do_app()

                    MDBoxLayout:
                        spacing: dp(6)

                        MDRaisedButton:
                            text: "EXPORTAR"
                            size_hint_x: 1
                            font_size: "12sp"
                            md_bg_color: 0.0, 0.4, 0.3, 1  # verde
                            on_release: app.exportar_dados()

                        MDRaisedButton:
                            text: "ENVIAR"
                            size_hint_x: 1
                            font_size: "12sp"
                            md_bg_color: 0.0, 0.4, 0.3, 1  # verde
                            on_release: app.enviar_dados()

                        MDRaisedButton:
                            text: "IMPORTAR"
                            size_hint_x: 1
                            font_size: "12sp"
                            md_bg_color: 0.4, 0.2, 0.6, 1  # roxo
                            on_release: app.abrir_importador()
"""


class FichaObreiroApp(MDApp):
    _panels_content = []
    _import_file_manager = None
    title = "Ficha do Obreiro"
    icon = "assets/icon.png"

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

            # MDExpansionPanel mede content.height UMA VEZ, no instante em
            # que começa a abrir, e anima até esse valor. Campos com rótulo
            # dinâmico (FieldRow/CheckRow) só recebem a largura final —e só
            # então recalculam a própria altura corretamente— depois desse
            # instante, deixando a altura do painel "grande demais" (sobra
            # espaço vazio abaixo do conteúdo). Resincroniza sempre que o
            # conteúdo mudar de altura enquanto o painel estiver aberto.
            def _ressincronizar_altura(_inst, _h, p=panel):
                if p.get_state() == "open" and not p._anim_playing:
                    p.height = p.content.height + p.panel_cls.height

            content.bind(height=_ressincronizar_altura)

        # 🚀 NOVO: Carregar rascunho salvo automaticamente ao iniciar
        print("🔄 Carregando rascunho salvo...")
        dados_salvos = carregar_rascunho_do_bd()
        if dados_salvos:
            for content in self._panels_content:
                populate_screen(content, dados_salvos)
            Snackbar(text="✅ Rascunho anterior carregado!").open()

        # Recebe um .json compartilhado de outro app (ex.: obreiro manda
        # por WhatsApp, pastor toca em "Abrir com Ficha de Obreiro" ou
        # escolhe o app na folha de compartilhamento nativa).
        from kivy.utils import platform
        if platform == "android":
            from app.services.android_share_intent import processar_intent_recebido
            processar_intent_recebido(self._importar_arquivo_selecionado)

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

    _ultimo_pdf = None
    _ultimo_export = None

    def gerar_pdf(self):
        dados = self.coletar_todos_dados()
        try:
            from app.services.pdf_generator import gerar_pdf
            path = gerar_pdf(dados)
            self._ultimo_pdf = path
            self._abrir_dialog_pdf_gerado(path)
        except Exception as e:
            traceback.print_exc()
            Snackbar(text=f"❌ Erro ao gerar PDF: {e}").open()

    def _abrir_dialog_pdf_gerado(self, path):
        """Após gerar o documento, oferece visualizar (conferir antes de
        enviar) e/ou enviar direto desta tela — sem precisar de um botão
        separado de 'Enviar PDF'. No Android, o arquivo gerado aqui é HTML
        (o WeasyPrint não roda lá); por isso também oferecemos 'Salvar
        como PDF', que usa a impressão nativa do Android (WebView) para
        produzir o PDF de verdade a partir desse mesmo HTML."""
        from kivy.utils import platform
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDFlatButton

        # Sem botão "FECHAR": MDDialog herda de ModalView, que já fecha
        # sozinho ao tocar fora ou apertar voltar (auto_dismiss=True por
        # padrão). Os botões aqui também usam texto mais curto e fonte
        # menor: a fileira de botões do MDDialog não quebra linha, e com
        # "VISUALIZAR" + "SALVAR COMO PDF" + "ENVIAR" o texto combinado
        # não cabia na largura de uma tela de celular — a fileira
        # estourava e o botão VISUALIZAR ficava cortado/sobreposto por
        # outro botão fora da tela, fazendo o toque cair no botão errado
        # (parecia que "VISUALIZAR só fechava o modal").
        botoes = [
            MDFlatButton(text="VISUALIZAR", font_size="12sp",
                         on_release=lambda x: (dialog.dismiss(), self._visualizar_pdf(path))),
        ]
        if platform == "android" and path.lower().endswith(".html"):
            botoes.append(MDFlatButton(
                text="SALVAR PDF",
                font_size="12sp",
                text_color=(0.012, 0.133, 0.247, 1),  # azul marinho
                on_release=lambda x: (dialog.dismiss(), self._salvar_como_pdf_android(path)),
            ))
        botoes.append(MDFlatButton(
            text="ENVIAR",
            font_size="12sp",
            text_color=(0.831, 0.627, 0.090, 1),  # dourado
            on_release=lambda x: (dialog.dismiss(), self._enviar_arquivo(path, "PDF")),
        ))

        dialog = MDDialog(title="Documento gerado!", text=path, buttons=botoes)
        dialog.open()

    def _salvar_como_pdf_android(self, html_path):
        """Gera um PDF de verdade a partir do HTML já gerado (usando o
        WebView do próprio sistema, que entende o CSS moderno do modelo,
        já que o WeasyPrint não funciona no Android) e, assim que o
        arquivo estiver pronto, abre direto o compartilhamento nativo do
        Android (ShareSheet) — em vez da tela de impressão do sistema,
        onde não fica claro para onde o arquivo foi salvo."""
        try:
            with open(html_path, encoding="utf-8") as f:
                html = f.read()
            pdf_path = str(Path(html_path).with_suffix(".pdf"))
            from app.services.android_print import gerar_pdf_android

            def _ao_concluir(caminho):
                self._enviar_arquivo(caminho, "PDF")

            def _ao_falhar(mensagem):
                Snackbar(text=f"❌ Erro ao gerar PDF: {mensagem}").open()

            gerar_pdf_android(html, pdf_path, ao_concluir=_ao_concluir, ao_falhar=_ao_falhar)
        except Exception as e:
            traceback.print_exc()
            Snackbar(text=f"❌ Erro ao preparar impressão: {e}").open()

    def _visualizar_pdf(self, path):
        try:
            from app.services.share import visualizar_arquivo
            visualizar_arquivo(path)
        except Exception as e:
            traceback.print_exc()
            Snackbar(text=f"❌ Erro ao visualizar PDF: {e}").open()

    def _enviar_arquivo(self, path, rotulo):
        try:
            from app.services.share import compartilhar_arquivo
            compartilhar_arquivo(path)
            Snackbar(text=f"✅ {rotulo}: {path}").open()
        except Exception as e:
            traceback.print_exc()
            Snackbar(text=f"❌ Erro ao enviar {rotulo}: {e}").open()

    def exportar_dados(self):
        """Gera um arquivo .json com todos os dados preenchidos em tela, para
        enviar (e-mail, WhatsApp etc.) e importar em outro dispositivo com
        este mesmo app — ex.: obreiro envia para o pastor completar a parte dele."""
        dados = self.coletar_todos_dados()
        try:
            path = exportar_dados_para_arquivo(dados)
            self._ultimo_export = path
            Snackbar(text=f"✅ Dados exportados: {path}").open()
        except Exception as e:
            traceback.print_exc()
            Snackbar(text=f"❌ Erro ao exportar: {e}").open()

    def enviar_dados(self):
        """Compartilha o arquivo de dados exportado para a outra parte
        importar no app dela e preencher o que falta."""
        if not self._ultimo_export:
            Snackbar(text="⚠️ Exporte os dados primeiro.").open()
            return
        self._enviar_arquivo(self._ultimo_export, "dados")

    def abrir_importador(self):
        """Abre o seletor de arquivos para importar um .json exportado
        anteriormente (deste ou de outro dispositivo) e preencher as telas."""
        from kivy.utils import platform
        from kivymd.uix.filemanager import MDFileManager
        from app.services.paths import pasta_fichas, pasta_privada_app

        if not hasattr(self, "_import_file_manager") or self._import_file_manager is None:
            self._import_file_manager = MDFileManager(
                exit_manager=self._fechar_importador,
                select_path=self._importar_arquivo_selecionado,
                ext=[".json"],
            )

        start_path = None
        if platform == "android":
            # Arquivo recebido por WhatsApp/e-mail normalmente cai em Download
            try:
                from android.storage import primary_external_storage_path
                download_dir = os.path.join(primary_external_storage_path(), "Download")
                if os.path.isdir(download_dir):
                    start_path = download_dir
            except Exception:
                pass
        if start_path is None:
            export_dir = pasta_fichas()
            start_path = str(export_dir) if export_dir.exists() else str(pasta_privada_app())
        self._import_file_manager.show(start_path)

    def _fechar_importador(self, *args):
        if self._import_file_manager:
            self._import_file_manager.close()

    def _importar_arquivo_selecionado(self, path):
        self._fechar_importador()
        try:
            dados = importar_dados_de_arquivo(path)
            for content in self._panels_content:
                populate_screen(content, dados)
            Snackbar(text=f"✅ Dados importados de: {path}").open()
        except Exception as e:
            traceback.print_exc()
            Snackbar(text=f"❌ Erro ao importar: {e}").open()

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