# foxxcad/engine.py
from ..canvas.canvasutils import world_to_canvas, canvas_to_world
class DrawingEngine:
    def __init__(self):
        self.zoom = 1.0
        self.offset = [0, 0]
        self.lines = []

    def add_line(self, line):
        self.lines.append(tuple(line))

    def draw_all(self, canvas, config):
        for line in self.lines:
            x1, y1 = world_to_canvas(line[0], self.zoom, self.offset)
            x2, y2 = world_to_canvas(line[1], self.zoom, self.offset)
            canvas.create_line(x1, y1, x2, y2, fill=config["line"], width=2)