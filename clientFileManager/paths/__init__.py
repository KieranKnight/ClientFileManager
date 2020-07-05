# platform
from .application_paths import _WINDOW_PATH 

# application root
from .application_paths import _ROOT

# user documents - typically where the main configuration is saved to.
from .application_paths import _USER_DOCUMENTS

# application configuration and location for startup folders - creates if they don't already exist
from .application_paths import (
    _APP_LOCATION,
    _UI_CONFIG_FOLDER, 
    _UI_CONFIGURATION,
    _LOGGING_LOCATION,
    _INTEGRATE_LOCATION,
)

# applications ui location and items
from .application_paths import (
    _UI_LOCATION,
    _CSS,
    _ICONS
)

# applications icons for QTreeWidgetItems.
from .application_paths import (
    _BRANCH_CLOSED_PNG,
    _BRANCH_END_PNG,
    _BRANCH_MORE_PNG,
    _BRANCH_OPEN_PNG,
    _BRANCH_VINE_PNG,
)

# application group
APPLICATION_PATHS = [_APP_LOCATION, _UI_CONFIG_FOLDER, _UI_CONFIGURATION, _LOGGING_LOCATION, _INTEGRATE_LOCATION]
# application ui location and items group
APPLICATION_UI = [_UI_LOCATION, _CSS, _ICONS]
# application QTreeWidgetItem paths
APPLICATION_ICONS = [_BRANCH_CLOSED_PNG, _BRANCH_END_PNG, _BRANCH_MORE_PNG, _BRANCH_OPEN_PNG, _BRANCH_VINE_PNG]
