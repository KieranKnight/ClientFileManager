################################################################################
## Client File Manager TOOL - Ingesting client files into a production pipeline
##  with tracking, logging and configuration overrides.
##
## File : custom_tree_widget.py
## Description : A Custom tree widget to display items to ingest into a
##  production pipeline. Top widget will be the selected folder, widgets
##  below will be the folders items. Single items will be one widget.
##
## Created by: Kieran Knight
## Email: kieransknight@gmail.com
## 
################################################################################

# Python Modules
import os

# Application
from utils import read_css
from third_party.Qt import QtWidgets, QtCore, QtGui
from paths import (
    _BRANCH_CLOSED_PNG,
    _BRANCH_END_PNG,
    _BRANCH_MORE_PNG,
    _BRANCH_OPEN_PNG,
    _BRANCH_VINE_PNG
)


class CustomTreeWidget(QtWidgets.QTreeWidget):
    """
    Creating the TreeWidget Object that will be used
    to hold the custom TreeWidgetItems.

    Arguments:
        QtWidgets {QTreeWidget} -- Inheriting the base QTreeWidget

    Returns:
        CustomTreeWidget -- Object linking to the widget and items created.
    """
    _HEADERS = ['Folder', 'filename', 'Sequence', 'Shot', 'Location', 'Option']
    _OVERRIDE_STYLE = "QTreeView::branch:has-siblings:!adjoins-item " \
        "{border-image: url('%s') 0;}" \
        "QTreeView::branch:has-siblings:adjoins-item " \
        "{border-image: url('%s') 0;}" \
        "QTreeView::branch:!has-children:!has-siblings:adjoins-item " \
        "{border-image: url('%s') 0;}" \
        "QTreeView::branch:has-children:!has-siblings:closed, " \
        "QTreeView::branch:closed:has-children:has-siblings " \
        "{border-image: none; image: url('%s');}" \
        "QTreeView::branch:open:has-children:!has-siblings, " \
        "QTreeView::branch:open:has-children:has-siblings " \
        "{border-image: none; image: url('%s');}" % (
            _BRANCH_VINE_PNG,
            _BRANCH_MORE_PNG, 
            _BRANCH_END_PNG,
            _BRANCH_CLOSED_PNG,
            _BRANCH_OPEN_PNG
        )
    def __init__(self, parent=None):
        """
        Sorting through the data within the initial method
        as we want this to run as soon as the class is instantiated.

        Keyword Arguments:
            parent {QMainWindow} -- The main application window to attach to(default: {None})
        """
        super(CustomTreeWidget, self).__init__(parent)

        self.setStyleSheet(self._OVERRIDE_STYLE)   

        self._data = None
        self._widgets = []
        self._parent = parent
        self.setColumnCount(len(self.headers))
        self.setHeaderLabels(self.headers)  

        ## Set Columns Width to match content:
        self.setColumnWidth(0, 350)
        self.setColumnWidth(1, 150)
        self.setColumnWidth(2, 100)
        self.setColumnWidth(3, 100)
        self.setColumnWidth(4, 350)
        self.setColumnWidth(5, 100)

        # Setting the alignment of the header files
        self.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.headerItem().setTextAlignment(2, QtCore.Qt.AlignCenter)
        self.headerItem().setTextAlignment(3, QtCore.Qt.AlignCenter)
        self.headerItem().setTextAlignment(4, QtCore.Qt.AlignCenter)
        self.headerItem().setTextAlignment(5, QtCore.Qt.AlignCenter)
        
    @property
    def headers(self):
        return self._HEADERS
    
    @property
    def widgets(self):
        return self._widgets

    def check_items(self, files, app_config):
        """
        Checking the files that have been passed.
        Sometimes, an empty folder may be passed which would
        be pointless to track so we return None and don't add this to
        the Widget. If only a single file is passed then we don't need
        to worry about a top level item, so the class itself will be passed.
        Finally, if multiple files are added we want to lay this out nicely
        with a top level folder. We build this top level item (_header)
        and return this as the item for what the parent will be.

        Args:
            files (List): The list of files collected from the ConfigureFiles object
            app_config (Configuration Object): The tools configuration object

        Returns:
            None, self, CustomTreeItem: Depending on what has been passed the return
                value will be modified. 
        """
        if not files:
            return None
        elif len(files) == 1:
            return self
        else:
            _header = CustomTreeItem(self)
            _header.build_top_level_values(files[0], app_config)
            _header.build_widget_items(self)
            return _header

    def add_items(self, items, app_config):
        """
        Main section to loop through the passed items
        and add the files to the QTreeWidget.

        Args:
            items (ConfigureFiles Object): The configure files object class.
            app_config (Configuration Object): The tools configuration object
        """
        _header = self.check_items(items.files, app_config)

        if not _header:
            print('The added folder has no contents.\nPlease add a folder with contents or a single file.')
            return

        single = True if len(items.files) == 1 else False
        
        for item in range(len(items.files)):
            _item = CustomTreeItem(_header)
            _item.build_subitem_values(items.files[item], single, app_config)
            _item.build_widget_items(self)
            _item.setTextAlignment(5, QtCore.Qt.AlignCenter)
            self._widgets.append(_item)
    

class CustomTreeItem(QtWidgets.QTreeWidgetItem):
    """
    Overriding the QTreeWidgetItem to work with widgets.

    Arguments:
        QtWidgets {QTreeWidgetItem} -- Inheriting the base QTreeWidgetItem
    """
    _OPTIONS = ['Plate', 'Texture', 'Model', 'Mocap', 'Reference', 'Ignore']
    _IGNORE_STYLE = 'background-color: #885007;  border: 1.5px solid #32414B'
    _REGULAR_STYLE = 'background-color: #0B1C2D; border: 1.5px solid #32414B'

    def __init__(self, parent=None):
        """
        Buidling the widgets directly within the __init__ method
        so everytime the class is instantiated, the widgets will be built.

        Keyword Arguments:
            parent {QMainWindow | CustomTreeWidget} -- The main parernt object.(default: {None})
        """
        super(CustomTreeItem, self).__init__(parent)
        
        self._item_contents = None
        self._header = False
        self._folder = None
        self._filename = None
        self._sequence = None
        self._shot = None
        self._location = None
        self._configuration = None
        self._parent = parent

    @property
    def folder(self):
        return self._folder_widget

    @property
    def filename(self):
        return self._filename_widget

    @property
    def sequence(self):
        return self._sequence_widget

    @property
    def shot(self):
        return self._shot_widget
    
    @property
    def location(self):
        return self._location_widget

    @property
    def option(self):
        return self._option_widget
    
    @property
    def item_contents(self):
        return self._item_contents

    @property
    def items(self):
        return [
            self.folder, 
            self.filename, 
            self.sequence, 
            self.shot, 
            self.location, 
            self.option
        ]

    def build_top_level_values(self, item, app_config):
        """
        Building the variables for the top level items.
        This is typically the first item in the items.files
        list.

        The top level item should only display the Folder and location.
        Checking the ignore button on the top level will check all 
        subitems linked to the folder.

        Args:
            item (ConfigureFiles Object): The configuration object that
                gets built once a file or folder is selected
            app_config (Cofiguration Object): The tools configuration
        """
        self._item_contents = item
        self._header = True
        self._folder = self._item_contents.parent_folder
        self._filename = ''
        self._sequence = ''
        self._shot = ''
        self._app_config = app_config
        self._location = app_config.add_configuration.output_location

    def build_subitem_values(self, item, single, app_config):
        """
        Building the variables for the sub level items.
        This will be places under the header item unless a
        single file is added

        A Single file will hold the full folder path,
        whereas multiple items will have teh header showing the full path
        and the sub folders displaying '...\{folder}'

        Args:
            item (ConfigureFiles Object): The configuration object that
                gets built once a file or folder is selected
            single (bool): Whether a single item has been passed
            app_config (Cofiguration Object): The tools configuration
        """
        if single:
            _folder_display = item.folder
        else:
            _parent_dir = item.parent_folder
            _folder_display = '...\{}'.format(item.folder.strip(_parent_dir))

        self._item_contents = item
        self._folder = _folder_display
        self._filename = self._item_contents.filename
        self._sequence = self._item_contents.sequence
        self._shot = self._item_contents.shot
        self._app_config = app_config
        self._location = app_config.add_configuration.output_location

    def build_widget_items(self, top_item):
        """
        Building the QTreeWidgetItems for the QTreeWidget

        Args:
            top_item (QTreeWidget): The top item the widgets
                will be parented to. Single items will only be 
                parented to QTreeWidget. Folders will be parented
                to the first item widget.
        """
        ## Column 0 - Input:
        self._folder_widget = QtWidgets.QLabel()
        self._folder_widget.setText(self._folder)
        top_item.setItemWidget(self, 0, self._folder_widget)

        ## Column 1 - filename:
        self._filename_widget = QtWidgets.QLabel()
        self._filename_widget.setText(self._filename)
        self._filename_widget.setAlignment(QtCore.Qt.AlignCenter)
        top_item.setItemWidget(self, 1, self._filename_widget)
 
        ## Column 1 - Sequence:
        self._sequence_widget = QtWidgets.QComboBox()
        self._sequence_widget.addItem(self._sequence)
        self._sequence_widget.setEditable(True)
        top_item.setItemWidget(self, 2, self._sequence_widget)
        {
            self._sequence_widget.addItem(os.path.basename(key)) 
            for (key, value) in self._app_config.add_configuration.output_subfolders.items()
        }
        self._sequence_widget.currentIndexChanged.connect(self.update_shot_wdgs)
 
        ## Column 2 - Shot:
        self._shot_widget = QtWidgets.QComboBox()
        self._shot_widget.addItem(self._shot)
        self._shot_widget.setEditable(True)
        top_item.setItemWidget(self, 3, self._shot_widget)

        ## Column 3 - Location
        self._location_widget = QtWidgets.QComboBox()
        self._location_widget.addItem(str(self._location))
        self._location_widget.setEditable(True)
        top_item.setItemWidget(self, 4, self._location_widget)

        ## Column 4 - Option
        self._option_widget = QtWidgets.QComboBox()
        [self._option_widget.addItem(option) for option in self._OPTIONS]
        top_item.setItemWidget(self, 5, self._option_widget)

        self.option_override()
        self._option_widget.currentIndexChanged.connect(self.option_override)

        # If the header file is passed, some overrides need to be set to allow 
        # an easier override option for all sub items
        if self._header:
            self._option_widget.currentIndexChanged.connect(self.header_option_override)
            self._location_widget.currentTextChanged.connect(self.header_location_override)
            self._sequence_widget.currentTextChanged.connect(self.header_sequence_override)
            self._shot_widget.currentTextChanged.connect(self.header_shot_override)

    def update_shot_wdgs(self):
        """
        Updating teh shot widgets.
        silent Try excpet added incase location isn't changed.
        This doesn't mean the code has failed, just stops an unexpected override.
        """
        try:
            _shots = [
                value for (key, value) in self._app_config.add_configuration.output_subfolders.items()
                if os.path.basename(key) == self.sequence.currentText()
                ][0]
            self.shot.clear()
            [self.shot.addItem(os.path.basename(widget)) for widget in _shots]
        except:
            pass

    def option_override(self):
        """
        Overriding the style sheet based on whether the widget option is
        set to either ignore or other.
        """
        [
            wdg.setStyleSheet(self._IGNORE_STYLE) 
            if self.option.currentText() == 'Ignore' else 
            wdg.setStyleSheet(self._REGULAR_STYLE) 
            for wdg in self.items
        ]

    def header_option_override(self):
        """
        Using the top level folder to override all children items.
        Making it easier for users to update all items at once.
        The option widget...
        """
        [
            wdg.setStyleSheet(self._IGNORE_STYLE) 
            if self.option.currentText() == 'Ignore' else 
            wdg.setStyleSheet(self._REGULAR_STYLE) 
            for wdg in self.items
        ]

        for child in range(self.childCount()):
            self.child(child).option.setCurrentIndex(self._option_widget.currentIndex())
            for wdg in self.child(child).items:
                if self.option.currentText() == 'Ignore':
                    wdg.setStyleSheet(self._IGNORE_STYLE)
                else:
                    wdg.setStyleSheet(self._REGULAR_STYLE)

    def header_location_override(self):
        """
        Using the top level folder to override all children items.
        Making it easier for users to update all items at once.
        The location widget...
        """
        [
            self.child(child).location.setCurrentText(self._location_widget.currentText())
            for child in range(self.childCount())
        ]

    def header_sequence_override(self):
        """
        Using the top level folder to override all children items.
        Making it easier for users to update all items at once.
        The sequence widget...
        """
        [
            self.child(child).sequence.setCurrentText(self._sequence_widget.currentText())
            for child in range(self.childCount())
        ]

    def header_shot_override(self):
        """
        Using the top level folder to override all children items.
        Making it easier for users to update all items at once.
        The shot widget...
        """
        [
            self.child(child).shot.setCurrentText(self._shot_widget.currentText())
            for child in range(self.childCount())
        ]
