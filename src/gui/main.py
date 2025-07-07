import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Genome Browser", width=800, height=600):
    dpg.add_text("Hello Genome Browser")
    dpg.add_button(label="Click Me", callback=lambda: print("Button clicked!"))

dpg.create_viewport(title="Genome Browser", width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()

import dearpygui.dearpygui as dpg
from Bio import SeqIO

# глобальные переменные
seq = ""
comp = ""
features = []
window_size = 200     # число нуклеотидов в окне просмотра
scale = 10            # пикселей на нуклеотид

def file_callback(_, app_data):
    global seq, comp, features, slider_max

    path = app_data["file_path_name"]
    fmt = "genbank" if path.lower().endswith((".gb", ".gbk")) else "fasta"
    rec = next(SeqIO.parse(path, fmt))
    seq = str(rec.seq)
    comp = str(rec.seq.complement())

    # GenBank-фичи
    features = []
    if fmt == "genbank":
        for f in rec.features:
            start = int(f.location.start.position)
            end = int(f.location.end.position)
            strand = f.location.strand or 0
            features.append((start, end, strand, f.type))

    # пересчитать слайдер
    slider_max = max(len(seq) - window_size, 0)
    dpg.configure_item("pos_slider", max_value=slider_max)
    dpg.set_value("pos_slider", 0)
    redraw_tracks()

def redraw_tracks():
    """Перерисовать фичи и последовательность для текущей позиции слайдера."""
    pos = dpg.get_value("pos_slider")
    end = pos + window_size
    sub_seq = seq[pos:end]
    sub_comp = comp[pos:end]

    # очистка древа отрисовки
    dpg.delete_item("track_canvas", children_only=True)

    # размеры канваса
    cw = window_size * scale
    ch = 80

    # рисуем фичи
    for start, end_f, strand, ftype in features:
        # если фича пересекает текущее окно
        if end_f < pos or start > end:
            continue
        x0 = (max(start, pos) - pos) * scale
        x1 = (min(end_f, end) - pos) * scale
        y0, y1 = 10, 30

        color = (100, 200, 100, 200) if strand >= 0 else (200, 100, 100, 200)
        dpg.draw_rectangle((x0, y0), (x1, y1), color=color, fill=color, parent="track_canvas")

        # стрелка для направления
        if strand == 1:
            dpg.draw_triangle(
                (x1, y0), (x1+8, (y0+y1)/2), (x1, y1),
                color=color, fill=color, parent="track_canvas"
            )
        elif strand == -1:
            dpg.draw_triangle(
                (x0, y0), (x0-8, (y0+y1)/2), (x0, y1),
                color=color, fill=color, parent="track_canvas"
            )

        # подпись типа
        dpg.draw_text(((x0+x1)/2, y1+2), ftype, size=12, color=(255,255,255,255), parent="track_canvas")

    # обновляем текст последовательностей
    dpg.set_value("seq_text", sub_seq)
    dpg.set_value("comp_text", sub_comp)

# Создаём GUI
dpg.create_context()

with dpg.window(label="Genome Visualizer", width=900, height=700):
    dpg.add_button(label="Open FASTA/GenBank", callback=lambda: dpg.show_item("file_dlg"))
    dpg.add_separator()

    # слайдер позиции
    dpg.add_slider_int(label="Start position", tag="pos_slider",
                       min_value=0, max_value=0, default_value=0,
                       width=400, callback=lambda *_: redraw_tracks())

    # область для графического трека
    with dpg.child_window(width=-1, height=120, horizontal_scrollbar=True):
        dpg.add_drawing(width=window_size*scale, height=80, tag="track_canvas")

    dpg.add_separator()

    # текстовые поля с горизонтальным скроллом
    dpg.add_input_text(label="Sequence",
                       tag="seq_text", multiline=True, readonly=True,
                       height=200, width=-1, no_wrap=True)
    dpg.add_input_text(label="Complement",
                       tag="comp_text", multiline=True, readonly=True,
                       height=200, width=-1, no_wrap=True)

# диалог выбора файла
with dpg.file_dialog(directory_selector=False, show=False,
                     callback=file_callback, tag="file_dlg"):
    dpg.add_file_extension(".fasta")
    dpg.add_file_extension(".fa")
    dpg.add_file_extension(".gb")
    dpg.add_file_extension(".gbk")
    dpg.add_file_extension(".*")

# Запуск приложения
dpg.create_viewport(title="Genome Visualizer", width=900, height=700)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
