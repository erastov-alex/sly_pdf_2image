import os

import supervisely as sly
from dotenv import load_dotenv

DATA = None

IS_PRODUCTION = sly.is_production()
if IS_PRODUCTION is True:
    load_dotenv("advanced.env")
    STORAGE_DIR = sly.app.get_data_dir()
else:
    load_dotenv("local.env")

load_dotenv(os.path.expanduser("~/supervisely.env"))

# Get ENV variables
TEAM_ID = sly.env.team_id()
WORKSPACE_ID = sly.env.workspace_id()
PATH_TO_FOLDER = sly.env.folder(raise_not_found=False)

api: sly.Api = sly.Api.from_env()
