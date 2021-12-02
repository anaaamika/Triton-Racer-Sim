from TritonRacerSim.components.component import Component
import pyrealsense2 as rs
import numpy as np
import cv2

class IntelRealsenseCam(Component):
    def __init__(self, cfg):
        super().__init__(inputs=[], outputs=['cam/img', ], threaded=True)
        self.img_w = cfg['img_w']
        self.img_h = cfg['img_h']
        self.image_format = cfg['image_format']
        
        self.pipeline = rs.pipeline()
        self.config = rs.config()

        self.processed_frame = None
        self.on = True

    def onStart(self):
        """Called right before the main loop begins"""
        self.profile = self.pipe.start(self.config)

    def step(self, *args):
        """The component's behavior in the main loop"""
        return self.processed_frame,

    def thread_step(self):
        """The component's behavior in its own thread"""

        while (self.on):
            frameset = self.pipe.wait_for_frames()
            color_frame = frameset.get_color_frame()
            processed_surface = 
            pygame.transform.scale(original_frame, (self.img_w, self.img_h))
            #duration = time.time() - start_time
            #print (duration)
            self.processed_frame = np.asarray(pygame.surfarray.array3d(processed_surface))
            #time.sleep(0.01)

    def onShutdown(self):
        """Shutdown"""
        self.on = False

    def getName(self):
        return 'Intel Realsense D455 Camera'