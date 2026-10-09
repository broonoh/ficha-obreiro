# app/ui/widgets/photo_field.py
"""Campo de foto 3x4 com upload e remoção — versão simplificada."""
import base64
import os
from pathlib import Path
from kivy.metrics import dp
from kivy.uix.image import Image as KivyImage
from kivy.clock import Clock
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.filemanager import MDFileManager
from PIL import Image


class PhotoField(MDBoxLayout):
    """Campo de foto 3x4 com preview, upload e remoção."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(240)
        self.spacing = dp(8)
        self.photo_path = None
        self.photo_base64 = None

        # Label do campo
        self.add_widget(MDLabel(
            text="FOTO 3x4 (TERNO E GRAVATA)",
            font_style="Caption",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            size_hint_y=None,
            height=dp(22),
            bold=True,
        ))

        # Container horizontal: foto + botões
        row = MDBoxLayout(
            size_hint_y=None,
            height=dp(170),
            spacing=dp(12),
        )

        # CORREÇÃO: Usar MDBoxLayout simples com fundo branco (sem MDCard)
        self.photo_area = MDBoxLayout(
            size_hint_y=None,
            height=dp(160),
            size_hint_x=None,
            width=dp(120),
            md_bg_color=(1, 1, 1, 1),  # Fundo branco sólido
        )
        # Placeholder inicial
        self.placeholder_label = MDLabel(
            text="Sem foto\nselecionada",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(0.5, 0.5, 0.5, 1),
        )
        self.photo_area.add_widget(self.placeholder_label)
        row.add_widget(self.photo_area)

        # Container vertical de botões
        btn_col = MDBoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(160),
            size_hint_x=None,
            width=dp(140),
            spacing=dp(8),
        )

        # Botão de upload
        # MDFlatButton (em vez de MDRaisedButton) não usa o
        # CommonElevationBehavior/sombra, que ficava "fantasma" (não
        # acompanhava a posição real do botão) ao rolar a tela dentro do
        # MDExpansionPanel/ScrollView.
        btn_upload = MDFlatButton(
            text="📷 Selecionar Foto",
            md_bg_color=(0.012, 0.133, 0.247, 1),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(44),
        )
        btn_upload.bind(on_release=self._open_file_manager)
        btn_col.add_widget(btn_upload)

        # Botão de remover
        self.btn_remove = MDFlatButton(
            text="🗑️ Remover Foto",
            md_bg_color=(0.706, 0.098, 0.149, 1),
            md_bg_color_disabled=(0.706, 0.098, 0.149, 0.4),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=dp(44),
            disabled=True,
        )
        self.btn_remove.bind(on_release=self._remove_photo)
        btn_col.add_widget(self.btn_remove)

        row.add_widget(btn_col)
        self.add_widget(row)

        self.file_manager = None

    def _open_file_manager(self, *args):
        if self.file_manager is None:
            self.file_manager = MDFileManager(
                exit_manager=self._close_file_manager,
                select_path=self._select_path,
                ext=[".jpg", ".jpeg", ".png", ".JPG", ".JPEG", ".PNG"],
            )
        self.file_manager.show(str(Path.home()))

    def _close_file_manager(self, *args):
        self.file_manager.close()

    def _select_path(self, path):
        """Callback quando o usuário seleciona um arquivo."""
        self._close_file_manager()

        if not os.path.exists(path):
            self._show_error("Arquivo não encontrado!")
            return

        if not os.access(path, os.R_OK):
            self._show_error("Sem permissão para ler!")
            return

        try:
            # Valida a imagem com PIL
            img = Image.open(path)
            img.verify()
            img = Image.open(path)  # Reabre após verify()

            # Converte para RGB se necessário
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')

            # Salva cópia temporária em local seguro
            temp_path = Path.home() / ".ficha_obreiro_temp.jpg"
            img.save(temp_path, "JPEG", quality=95)

            self.photo_path = str(temp_path)

            # Usa Clock para garantir que o layout esteja pronto
            Clock.schedule_once(lambda dt: self._update_preview(), 0.1)

        except Exception as e:
            print(f"❌ Erro ao processar imagem: {e}")
            self._show_error(f"Erro: {str(e)[:50]}")

    def _show_error(self, message):
        """Mostra mensagem de erro na área da foto."""
        self.photo_area.clear_widgets()
        self.photo_area.add_widget(MDLabel(
            text=f"️ {message}",
            halign="center",
            valign="middle",
            theme_text_color="Custom",
            text_color=(0.706, 0.098, 0.149, 1),
            font_style="Caption",
        ))

    def _remove_photo(self, *args):
        """Remove a foto selecionada."""
        self.photo_path = None
        self.photo_base64 = None
        self.photo_area.clear_widgets()
        self.photo_area.add_widget(self.placeholder_label)
        self.btn_remove.disabled = True

    def _update_preview(self):
        """Atualiza o preview da foto."""
        if not self.photo_path or not os.path.exists(self.photo_path):
            self._show_error("Caminho inválido!")
            return

        self.photo_area.clear_widgets()

        try:
            # Carrega e redimensiona a imagem
            img = Image.open(self.photo_path)
            img.thumbnail((120, 160), Image.Resampling.LANCZOS)

            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Salva preview temporário
            temp_preview = Path.home() / ".ficha_obreiro_preview.jpg"
            img.save(temp_preview, "JPEG", quality=95)

            # Cria widget de imagem do Kivy
            kivy_img = KivyImage(
                source=str(temp_preview),
                allow_stretch=True,
                keep_ratio=True,
                size_hint=(1, 1),  # CORREÇÃO: size_hint explícito
            )

            # Adiciona ao container
            self.photo_area.add_widget(kivy_img)
            self.btn_remove.disabled = False

            # Gera base64
            self._generate_base64(str(temp_preview))

            print(f"✅ Foto carregada com sucesso: {self.photo_path}")

        except Exception as e:
            print(f"❌ Erro ao atualizar preview: {e}")
            self._show_error(f"Erro: {str(e)[:40]}")

    def _generate_base64(self, image_path):
        """Gera data URI (data:image/jpeg;base64,...) para uso direto em <img src>."""
        try:
            with open(image_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            self.photo_base64 = f"data:image/jpeg;base64,{encoded}"
        except Exception as e:
            print(f"❌ Erro ao gerar base64: {e}")
            self.photo_base64 = None

    def get_photo_base64(self) -> str:
        return self.photo_base64 or ""

    def get_photo_path(self) -> str:
        return self.photo_path or ""