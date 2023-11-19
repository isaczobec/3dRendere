import renderer as r
import Objects3D as obj
import Time

class GameManager():
    def __init__(self,rendererObject: r.Renderer) -> None:
        self.renderer: r.Renderer = rendererObject

    def run(self):
        
        if self.renderer.clickedObject != None:
            self.renderer.clickedObject.Rotate(1*Time.deltaTime,0,0)