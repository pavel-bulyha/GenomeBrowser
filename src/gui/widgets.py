import dearpygui.dearpygui as dpg

def create_controls(open_cb, slide_cb):
    """
    Добавляет кнопку «Open FASTA/GenBank» и слайдер навигации.
    open_cb  — коллбэк открытия файла
    slide_cb — коллбэк перерисовки (redraw_tracks)
    """
    dpg.add_button(label="Open FASTA/GenBank", callback=open_cb)
    dpg.add_separator()
    dpg.add_slider_int(
        label="Start position",
        tag="pos_slider",
        min_value=0,
        max_value=0,
        default_value=0,
        width=400,
        callback=slide_cb
    )

def create_canvas(cfg):
    """
    Создаёт DrawList с тегом "track_canvas" для отрисовки фич.
    """
    with dpg.child_window(
        width=-1,
        height=cfg["canvas_height"],
        horizontal_scrollbar=True
    ):
        dpg.add_drawlist(
            tag="track_canvas",
            width=cfg["window_size"] * cfg["scale"],
            height=cfg["canvas_height"]
        )

def create_sequence_text(cfg):
    """
    Два поля вывода для исходной и комплементарной цепей.
    """
    dpg.add_separator()
    dpg.add_input_text(
        label="Sequence", tag="seq_text", multiline=True,
        readonly=True, height=200, width=cfg["text_width"],
        no_horizontal_scroll=True
    )
    dpg.add_input_text(
        label="Complement", tag="comp_text", multiline=True,
        readonly=True, height=200, width=cfg["text_width"],
        no_horizontal_scroll=True
    )
