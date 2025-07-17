import os
import dearpygui.dearpygui as dpg

from config_loader   import load_config
from core.parser     import load_sequence
from core.drawer     import clear_canvas, draw_features
from gui.dialogs     import ask_open_filename
from gui.widgets     import create_controls, create_canvas, create_sequence_text

# глобальное состояние
state = {
    "seq": "",
    "comp": "",
    "features": [],
    "cfg": {}
}

def open_file(_=None):
    """
    Колбэк кнопки «Open FASTA/GenBank».
    Вызывает Tk-диалог с папкой initial_dir,
    сохраняет новый initial_dir и запускает redraw.
    """
    cfg = state["cfg"]
    # берём из конфига последний путь
    initial_dir = cfg.get("initial_dir", "")

    path = ask_open_filename(
        title="Open FASTA/GenBank",
        filetypes=[
            ("FASTA",   ("*.fasta", "*.fa")),
            ("GenBank", ("*.gb", "*.gbk")),
            ("All files", "*.*")
        ],
        initialdir=initial_dir
    )

    if not path:
        print("[main] open_file: cancelled or empty path")
        return

    # запомним новую папку для следующего раза
    cfg["initial_dir"] = os.path.dirname(path)

    print(f"[main] file selected: {path}")
    seq, comp, feats = load_sequence(path)
    state.update(seq=seq, comp=comp, features=feats)

    # настраиваем слайдер под новую длину
    max_pos = max(len(seq) - cfg["window_size"], 0)
    dpg.configure_item("pos_slider", max_value=max_pos)
    dpg.set_value("pos_slider", 0)

    redraw_tracks()

def redraw_tracks(_=None):
    """
    Перерисовывает canvas и текстовые поля по текущему значению слайдера.
    """
    cfg = state["cfg"]
    pos = dpg.get_value("pos_slider")

    clear_canvas("track_canvas")
    draw_features("track_canvas", state["features"], pos, cfg)

    end = pos + cfg["window_size"]
    dpg.set_value("seq_text",  state["seq"][pos:end])
    dpg.set_value("comp_text", state["comp"][pos:end])

def main():
    # 1) загрузить конфиг
    state["cfg"] = load_config()
    print(f"[main] config loaded, initial_dir={state['cfg']['initial_dir']!r}")

    # 2) поднять DearPyGui
    dpg.create_context()
    with dpg.window(label="Genome Visualizer",
                    width=state["cfg"]["viewport"]["width"],
                    height=state["cfg"]["viewport"]["height"]):
        create_controls(open_file, redraw_tracks)
        create_canvas(state["cfg"])
        create_sequence_text(state["cfg"])

    dpg.create_viewport(title="Genome Visualizer",
                        width=state["cfg"]["viewport"]["width"],
                        height=state["cfg"]["viewport"]["height"])
    dpg.setup_dearpygui()
    dpg.show_viewport()
    print("[main] entering main loop")
    dpg.start_dearpygui()
    print("[main] exited main loop")
    dpg.destroy_context()

if __name__ == "__main__":
    main()
