import supervisely as sly

from supervisely.app.widgets import (
    Container
)
import src.globals as g
from src.ui.file_select import process

class MyApp:

    def __init__(self):
        self.data = None

    def run(self):
        card = process()
        layout = Container(widgets=[card])
        app = sly.Application(layout=layout)
        
        return app

a = MyApp()
app = a.run()