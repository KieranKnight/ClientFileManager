import os
import sys
from pathlib import Path

# platform
_WINDOW_PATH = sys.platform

# application root
_ROOT = Path(os.path.realpath(__file__)).parent.parent

# user documents - typically where the main configuration is saved to.
_USER_DOCUMENTS = str(Path(os.path.expanduser("~") , 'Documents'))

# application configuration and location for startup folders - creates if they don't already exist
_APP_LOCATION = str(Path(_USER_DOCUMENTS, 'ClientFileManager'))
_UI_CONFIG_FOLDER = str(Path(_APP_LOCATION, 'ui_configuration'))
_UI_CONFIGURATION = str(Path(_UI_CONFIG_FOLDER, 'configuration.json'))
_LOGGING_LOCATION = str(Path(_APP_LOCATION, 'logging'))
_INTEGRATE_LOCATION = str(Path(_APP_LOCATION, 'integrate'))

# applications ui location and items
_UI_LOCATION = str(Path(_ROOT, 'ui_items'))
_CSS = str(Path(_UI_LOCATION, 'ui_style_sheet.css'))
_ICONS = str(Path(_UI_LOCATION, 'icons'))

# applications icons for QTreeWidgetItems.
_BRANCH_CLOSED_PNG = str(Path(_ICONS, 'branch_closed.png')) if not _WINDOW_PATH == 'win32' else str(Path(_ICONS, 'branch_closed.png')).replace('\\', '/')
_BRANCH_END_PNG = str(Path(_ICONS, 'branch_end.png')) if not _WINDOW_PATH == 'win32' else str(Path(_ICONS, 'branch_end.png')).replace('\\', '/')
_BRANCH_MORE_PNG = str(Path(_ICONS, 'branch_more.png')) if not _WINDOW_PATH == 'win32' else str(Path(_ICONS, 'branch_more.png')).replace('\\', '/')
_BRANCH_OPEN_PNG = str(Path(_ICONS, 'branch_open.png')) if not _WINDOW_PATH == 'win32' else str(Path(_ICONS, 'branch_open.png')).replace('\\', '/')
_BRANCH_VINE_PNG = str(Path(_ICONS, 'branch_vine.png')) if not _WINDOW_PATH == 'win32' else str(Path(_ICONS, 'branch_vine.png')).replace('\\', '/')
