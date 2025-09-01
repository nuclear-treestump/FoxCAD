def world_to_canvas(point, zoom, offset):
    x, y = point
    cx = (x - offset[0]) * zoom
    cy = (y - offset[1]) * zoom
    return cx, cy

def canvas_to_world(point, zoom, offset):
    x, y = point
    wx = x / zoom + offset[0]
    wy = y / zoom + offset[1]
    return wx, wy