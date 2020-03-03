from panda3d.core import *
from direct.showbase.ShowBase import ShowBase

base = ShowBase()

base.trackball.node().set_pos(0, 100, 0)

model = loader.load_model("panda.egg")
model.reparent_to(base.render)

# Add a dummy node to the camera to hold the projection matrix
proj_dummy = base.cam.attach_new_node("proj-dummy")

# Set up a node in 2-D space to hold the drawn lines
line_node = GeomNode("lines")
line_path = base.render2d.attach_new_node(line_node)

def draw_box(task):
    # Copy the projection matrix to the dummy
    proj_mat = base.cam.node().get_lens().get_projection_mat_inv()
    proj_dummy.set_transform(TransformState.make_mat(proj_mat))

    # Calculate the box in projected (2D) space and draw lines in the 2D graph
    min, max = model.get_tight_bounds(proj_dummy)

    segs = LineSegs()
    segs.move_to(min[0], 0, min[1])
    segs.draw_to(min[0], 0, max[1])
    segs.draw_to(max[0], 0, max[1])
    segs.draw_to(max[0], 0, min[1])
    segs.draw_to(min[0], 0, min[1])

    line_node.remove_all_geoms()
    segs.create(line_node)

    return task.cont

base.taskMgr.add(draw_box, "draw-box")

base.run()