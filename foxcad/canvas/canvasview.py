import tkinter as tk
from tkinter import Canvas
from ..engine.engineclass import DrawingEngine
from .canvasutils import canvas_to_world, world_to_canvas

class CanvasView(Canvas):
    def __init__(self, root, engine, config, **kwargs):
        self.engine = engine
        self.config = config 
        super().__init__(root, **kwargs)

        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self.bind("<MouseWheel>", self.on_zoom)
        self.bind("<Motion>", self.on_motion)

        self.current_line = None
        self.redraw()

    def redraw(self):
        self.configure(bg=self.config["background"])
        self.delete("all")
        self.draw_grid()
        self.draw_origin()
        self.engine.draw_all(self, self.config) 

        if self.current_line:
            x1, y1 = world_to_canvas(self.current_line[0], self.engine.zoom, self.engine.offset)
            x2, y2 = world_to_canvas(self.current_line[1], self.engine.zoom, self.engine.offset)
            self.create_line(x1, y1, x2, y2, fill="red", dash=(5, 3), width=2)

    def draw_grid(self):
        spacing = 50
        limit = 2000
        for i in range(-limit, limit, spacing):
            x1, y1 = world_to_canvas((i, -limit), self.engine.zoom, self.engine.offset)
            x2, y2 = world_to_canvas((i, limit), self.engine.zoom, self.engine.offset)
            self.create_line(x1, y1, x2, y2, fill=self.config["grid"])

            x1, y1 = world_to_canvas((-limit, i), self.engine.zoom, self.engine.offset)
            x2, y2 = world_to_canvas((limit, i), self.engine.zoom, self.engine.offset)
            self.create_line(x1, y1, x2, y2, fill=self.config["grid"])

    def draw_origin(self):
        ox, oy = world_to_canvas((0, 0), self.engine.zoom, self.engine.offset)
        self.create_line(ox - 10, oy, ox + 10, oy, fill=self.config["sketch_boundary"], width=2)  # X-axis
        self.create_line(ox, oy - 10, ox, oy + 10, fill=self.config["sketch_boundary"], width=2)  # Y-axis
        self.create_oval(ox - 2, oy - 2, ox + 2, oy + 2, fill="black")

    def on_click(self, event):
        wx, wy = canvas_to_world((event.x, event.y), self.engine.zoom, self.engine.offset)
        self.current_line = [(wx, wy)]

    def on_drag(self, event):
        if self.current_line:
            wx, wy = canvas_to_world((event.x, event.y), self.engine.zoom, self.engine.offset)
            self.current_line = [self.current_line[0], (wx, wy)]
            self.redraw()

    def on_release(self, event):
        if self.current_line and len(self.current_line) == 2:
            self.engine.add_line(self.current_line)
        self.current_line = None
        self.redraw()

    def on_zoom(self, event):
        factor = 1.1 if event.delta > 0 else 0.9
        self.engine.zoom *= factor
        self.redraw()

    def on_motion(self, event):
        wx, wy = canvas_to_world((event.x, event.y), self.engine.zoom, self.engine.offset)
        self.master.title(f"FoxxCAD — Cursor: ({wx:.2f}, {wy:.2f})")