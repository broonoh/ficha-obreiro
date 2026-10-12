# app/ui/widgets/date_field.py
"""Campo de data: digitação com máscara DD/MM/AAAA + seletor em calendário."""
import re
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDIconButton
from kivymd.uix.pickers import MDDatePicker


class _MaskedDateTextField(MDTextField):
    """MDTextField que formata a digitação automaticamente como DD/MM/AAAA."""

    def insert_text(self, substring, from_undo=False):
        if from_undo:
            return super().insert_text(substring, from_undo=from_undo)

        # Mantém a máscara simples: sempre digita no final do campo.
        if self.cursor_index() != len(self.text):
            self.cursor = self.get_cursor_from_index(len(self.text))

        digits = re.sub(r"\D", "", self.text + substring)[:8]

        if len(digits) <= 2:
            formatted = digits
        elif len(digits) <= 4:
            formatted = f"{digits[:2]}/{digits[2:]}"
        else:
            formatted = f"{digits[:2]}/{digits[2:4]}/{digits[4:]}"

        self.text = ""
        return super().insert_text(formatted, from_undo=from_undo)


class DateField(MDBoxLayout):
    """Campo de data com máscara DD/MM/AAAA e botão de calendário."""

    def __init__(self, hint_text="Data", **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = None
        self.height = dp(56)
        self.spacing = dp(4)

        self.text_field = _MaskedDateTextField(
            hint_text=hint_text,
            mode="fill",
            size_hint_y=None,
            height=dp(56),
            font_size="14sp",
        )
        self.add_widget(self.text_field)

        self.calendar_button = MDIconButton(
            icon="calendar",
            theme_text_color="Custom",
            text_color=(0.012, 0.133, 0.247, 1),
            pos_hint={"center_y": 0.5},
        )
        self.calendar_button.bind(on_release=self._open_date_picker)
        self.add_widget(self.calendar_button)

    def _open_date_picker(self, *args):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self._on_date_save)
        date_dialog.open()

    def _on_date_save(self, instance, value, date_range):
        self.text_field.text = value.strftime("%d/%m/%Y")

    @property
    def text(self):
        return self.text_field.text

    @text.setter
    def text(self, value):
        self.text_field.text = value

    @property
    def hint_text(self):
        return self.text_field.hint_text

    @hint_text.setter
    def hint_text(self, value):
        self.text_field.hint_text = value
