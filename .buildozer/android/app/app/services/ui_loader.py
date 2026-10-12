# app/services/ui_loader.py
def populate_screen(content, data: dict):
    """通用函数：将字典数据填充回 Kivy UI 组件"""
    if not data:
        return

    # 1. 填充普通文本字段 (MDTextField) 和 Dropdown
    if hasattr(content, 'fields'):
        for key, widget in content.fields.items():
            if key in data and data[key] is not None:
                val = str(data[key])
                if hasattr(widget, 'text'):
                    widget.text = val
                elif hasattr(widget, 'selected_value'): # DropdownField
                    widget.selected_value = val
                    widget.button.text = f"  {val}"

    # 1b. 填充 Dropdown (DropdownField guardado em content.dropdowns)
    if hasattr(content, 'dropdowns'):
        for key, widget in content.dropdowns.items():
            if key in data and data[key] is not None:
                val = str(data[key])
                widget.selected_value = val
                widget.button.text = f"  {val}"

    # 2. 填充 Checkbox
    if hasattr(content, 'checks'):
        touched = getattr(content, 'checks_touched', None)
        for key, widget in content.checks.items():
            if key in data:
                val = data[key]
                # 兼容字符串 "True"/"False" 和 布尔值
                if isinstance(val, str):
                    val = val.lower() in ('true', 'sim', '1', 'yes')
                widget.active = bool(val) if val is not None else False
                # Restaura se o campo foi respondido (None = nunca respondido),
                # para o botão bind de _add_check não marcar "tocado" incorretamente.
                if touched is not None and key in touched:
                    touched[key] = val is not None

    # 3. 填充 LimitedTextField (带计数器的文本框)
    if hasattr(content, 'limited_fields'):
        for key, widget in content.limited_fields.items():
            if key in data and data[key] is not None:
                widget.text_field.text = str(data[key])
                # 手动触发计数器更新
                widget._on_text_changed(widget.text_field, widget.text_field.text)

    # 4. 填充 Foto (如果有)
    # Prioriza o base64 (portável entre dispositivos) sobre foto_path, que
    # é um caminho absoluto do aparelho que gerou o arquivo e quase nunca
    # existe em outro dispositivo/instalação — ex.: pastor importando a
    # ficha enviada pelo obreiro por outro celular.
    if hasattr(content, 'photo_field'):
        import os
        foto_base64 = data.get('foto_base64')
        foto_path = data.get('foto_path')
        if foto_base64:
            content.photo_field.set_photo_from_base64(foto_base64)
        elif foto_path and os.path.exists(foto_path):
            content.photo_field.photo_path = foto_path
            content.photo_field._update_preview()