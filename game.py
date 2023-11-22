import renderer as r
import Objects3D as obj
import numpy as np
from numpy import array as ar
import Time



class GameManager():
    def __init__(self,rendererObject: r.Renderer) -> None:
        self.renderer: r.Renderer = rendererObject

        quad = obj.R3Object([obj.Face([obj.Vertex(ar([-1.364,1,0,1])),
                                            obj.Vertex(ar([-1.364,-1,0,1])),
                                            obj.Vertex(ar([1.364,-1,0,1])),
                                            obj.Vertex(ar([1.364,1,0,1]))],
                                            virtualCamera=self.renderer.camera,
                                            planeImage="cardBackside",
                                            planeImageScale=95)],
                                            position=ar([5,1,0,1]),
                                            
                                            triangulate=False)
        
        self.renderer.objectList.append(quad)

    def run(self):
        
        if self.renderer.clickedObject != None:
            self.renderer.clickedObject.Rotate(1*Time.deltaTime,0,0)

