from dearpygui import dearpygui as dpg
dpg.create_context()
dpg.create_viewport(title="Test", width=400, height=300)
with dpg.window(label="Test Window"):
    dpg.add_button(label="Click Me")
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()