import supervisely as sly

from supervisely.app.widgets import Container

from src.ui.file_select import process


card = process()
layout = Container(widgets=[card])
app = sly.Application(layout=layout)
        
