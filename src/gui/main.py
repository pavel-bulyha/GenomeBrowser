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
