import dearpygui.dearpygui as dpg

def clear_canvas(tag):
    """Удаляет всё, что было на drawlist."""
    print(f"[drawer] clear_canvas(tag={tag!r})")      # <<<<<< отладка
    dpg.delete_item(tag, children_only=True)

def draw_features(tag, features, pos, cfg):
    """
    Рисует фичи на drawlist.
    """
    end_window = pos + cfg["window_size"]
    print(f"[drawer] draw_features(tag={tag!r}, pos={pos}, window_size={cfg['window_size']})")
    print(f"[drawer] total features passed: {len(features)}")
    for idx, (start, end_f, strand, ftype) in enumerate(features):
        if end_f < pos or start > end_window:
            continue

        x0 = (max(start, pos) - pos) * cfg["scale"]
        x1 = (min(end_f, end_window) - pos) * cfg["scale"]
        y0, y1 = 10, 30
        color = (100,200,100,200) if strand >= 0 else (200,100,100,200)

        print(f"  [drawer] drawing feature #{idx}: {ftype} [{start}:{end_f}], "
              f"strand={strand}, x0={x0}, x1={x1}")   # <<<<<< отладка

        dpg.draw_rectangle((x0, y0), (x1, y1),
                           color=color, fill=color,
                           parent=tag)

        if strand == 1:
            dpg.draw_triangle((x1, y0),
                              (x1 + 8, (y0+y1)/2),
                              (x1, y1),
                              color=color, fill=color,
                              parent=tag)
        elif strand == -1:
            dpg.draw_triangle((x0, y0),
                              (x0 - 8, (y0+y1)/2),
                              (x0, y1),
                              color=color, fill=color,
                              parent=tag)

        dpg.draw_text(((x0+x1)/2, y1 + 2), ftype,
                      size=12, color=(255,255,255,255),
                      parent=tag)
