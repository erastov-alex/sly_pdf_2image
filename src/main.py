import supervisely as sly

from supervisely.app.widgets import Container

import src.ui.file_select as file_select


card = file_select.card
layout = Container(widgets=[card])
app = sly.Application(layout=layout)
        
