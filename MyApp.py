from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor

from panda3d.core import *

from direct.interval.IntervalGlobal import *

class MyApp(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Load the environment model.
        self.scene = self.loader.loadModel("models/environment")
        # Reparent the model to render.
        self.scene.reparentTo(self.render)
        # Apply scale and position transforms on the model.
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager.
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask")

        # Load and transform the panda actor.
        self.pandaActor = Actor("models/panda-model",
                                {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)
        # Loop its animation.
        self.pandaActor.loop("walk")

        ambLight = AmbientLight('ambient')
        ambLight.setColor(Vec4(0.3, 0.2, 0.2, 1.0))
        ambNode = self.render.attachNewNode(ambLight)
        self.render.setLight(ambNode)

        dirLight = DirectionalLight('directional')
        dirLight.setColor(Vec4(0.3, 0.9, 0.3, 1.0))
        dirNode = self.render.attachNewNode(dirLight)
        dirNode.setHpr(60, 0, 90)
        self.render.setLight(dirNode)

        pntLight = PointLight('point')
        pntLight.setColor(Vec4(3.9, 3.9, 3.8, 1.0))
        pntNode = self.render.attachNewNode(pntLight)
        pntNode.setPos(0, 0, 15)
        self.pandaActor.setLight(pntNode)

        sptLight = Spotlight('spot')
        sptLens = PerspectiveLens()
        sptLight.setLens(sptLens)
        sptLight.setColor(Vec4(1.0, 0.4, 0.4, 1.0))
        sptLight.setShadowCaster(True)
        sptNode = self.render.attachNewNode(sptLight)
        sptNode.setPos(-10, -10, 20)
        sptNode.lookAt(self.pandaActor)
        self.render.setLight(sptNode)

        self.render.setShaderAuto()

        self.activeRamp = 0
        toggle = Func(self.toggleRamp)
        switcher = Sequence(toggle, Wait(3))
        switcher.loop()

        # Add a dummy node to the camera to hold the projection matrix
        self.proj_dummy = self.cam.attach_new_node("proj-dummy")

        # Set up a node in 2-D space to hold the drawn lines
        self.line_node = GeomNode("lines")
        self.line_path = self.render2d.attach_new_node(self.line_node)

        self.taskMgr.add(self.draw_box, "draw-box")



    def toggleRamp(self):
        if self.activeRamp == 0:
            self.render.setAttrib(LightRampAttrib.makeDefault())
        elif self.activeRamp == 1:
            self.render.setAttrib(LightRampAttrib.makeHdr0())
        elif self.activeRamp == 2:
            self.render.setAttrib(LightRampAttrib.makeHdr1())
        elif self.activeRamp == 3:
            self.render.setAttrib(LightRampAttrib.makeHdr2())
        elif self.activeRamp == 4:
            self.render.setAttrib(LightRampAttrib.
                                  makeSingleThreshold(0.1, 0.3))
        elif self.activeRamp == 5:
            self.render.setAttrib(LightRampAttrib.
                                  makeDoubleThreshold(0, 0.1, 0.3, 0.8))

        self.activeRamp += 1
        if self.activeRamp > 5:
            self.activeRamp = 0
    # Define a procedure to move the camera.
    def spinCameraTask(self, task):
        angleDegrees = task.time * 10.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        #self.screenshot()
        return Task.cont

    def draw_box(self, task):
        # Copy the projection matrix to the dummy
        proj_mat = self.cam.node().get_lens().get_projection_mat_inv()
        self.proj_dummy.set_transform(TransformState.make_mat(proj_mat))

        # Calculate the box in projected (2D) space and draw lines in the 2D graph
        min, max = self.pandaActor.get_tight_bounds(self.proj_dummy)

        segs = LineSegs()
        segs.move_to(min[0], 0, min[1])
        segs.draw_to(min[0], 0, max[1])
        segs.draw_to(max[0], 0, max[1])
        segs.draw_to(max[0], 0, min[1])
        segs.draw_to(min[0], 0, min[1])

        self.line_node.remove_all_geoms()
        segs.create(self.line_node)

        return task.cont


app = MyApp()
app.run()