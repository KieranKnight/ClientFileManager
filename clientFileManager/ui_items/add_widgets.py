################################################################################
## Client File Manager TOOL - Ingesting client files into a production pipeline
##  with tracking, logging and configuration overrides.
##
## File : add_widgets.py
## Description : Module to add widgets to the main application UI
##
## Created by: Kieran Knight
## Email: kieransknight@gmail.com
## 
################################################################################

# Application
from configuration.configure import IntegrateConfigure
from third_party.Qt import QtWidgets, QtCore, QtGui


class GroupWidgets(QtWidgets.QGroupBox):
    """
    Class that takes a list of widgets and places the contents
    into a QGroupBox

    Args:
        QtWidgets.QGroupBox (QGroupBox): Inheriting from QT's QGroupBox
    """
    def __init__(self, widgets, title, margin=0, parent=None):
        super(GroupWidgets, self).__init__(title, parent)
        self.setFlat(True)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(margin, margin, margin, margin)
        [self.layout().addWidget(widget) for widget in widgets]


class BaseAddItems(QtWidgets.QWidget):
    """
    Base class that all/most UI widgets should inherit from

    Args:
        QtWidgets.QWidget (QWidget): Inheriting from QT's QWidget

    Raises:
        NotImplementedError: All inheriting classes should include the 
            build_widget method
    """
    _ATTRIBUTE_CLASSES = [property]
    def __init__(self, parent):
        super(BaseAddItems, self).__init__(parent)

        self._h_layout = QtWidgets.QHBoxLayout()  # setting the main layout
        self.build_widget()  # building the widget contents
        self.set_layout()  # adding all items to the main layout
        
    def build_widget(self):
        raise NotImplementedError

    def _get_properties(self):
        """
        Method loops through all property items of the inheriting classes
        and returns a dictionay of the avaliable properties and their values

        Note: All properties should be a QT Widget so they are correctly added
        to the main layout.

        Returns:
            dict: Dictionary of all properties
        """
        _widgets = {}
        for name in dir(self.__class__):
            if name.startswith('__'):
                continue
            obj = getattr(self.__class__, name)
            if isinstance(obj, *self._ATTRIBUTE_CLASSES):
                val = obj.__get__(self, self.__class__)
                _widgets[name] = val
        return _widgets

    def set_layout(self):
        """
        Setting all found widgets to the main layout.
        """
        [self._h_layout.addWidget(item) for key,item in self._get_properties().items()]
        self.setLayout(self._h_layout)


class AddClientItemsButtons(BaseAddItems):
    """
    Class that adds Client item buttons to the main UI.
    This class is for the add file, add folder and remove items.
    """
    def __init__(self, parent=None):
        super(AddClientItemsButtons, self).__init__(parent)

    @property
    def add_file_btn(self):
        return self._add_file_btn

    @property
    def add_folder_btn(self):
        return self._add_folder_btn

    @property
    def remove_btn(self):
        return self._remove_btn

    def build_widget(self):
        """
        Building the widgets for client items.
        """
        self._add_file_btn = QtWidgets.QPushButton()
        self._add_file_btn.setText('Add Single Client File')
        
        self._add_folder_btn = QtWidgets.QPushButton()
        self._add_folder_btn.setText('Add Client Folder')

        self._remove_btn = QtWidgets.QPushButton()
        self._remove_btn.setText('Remove Client File/Folder')


class AddIntegrateButton(BaseAddItems):
    """
    Class that adds the Integrate button to the main UI
    """
    def __init__(self, parent=None):
        super(AddIntegrateButton, self).__init__(parent)

    @property
    def integrate_btn(self):
        return self._integrate_btn

    def build_widget(self):
        self._integrate_btn = QtWidgets.QPushButton()
        self._integrate_btn.setText('Integrate Client Files')


class AddSaveConfigurationWidget(BaseAddItems):
    """
    Class that add the save configuration button
    """
    def __init__(self, parent=None):
        super(AddSaveConfigurationWidget, self).__init__(parent)

    @property
    def save_configuration(self):
        return self._save_configuration_btn

    def build_widget(self):
        self._save_configuration_btn = QtWidgets.QPushButton()
        self._save_configuration_btn.setText('Save Configuration Changes To File')


class AddConfigurationWidgets(QtWidgets.QWidget):
    """
    Class that adds the main Configuration widgets.

    Note: This class does not inherit from the BaseAddItems.
    This is intentional as a different set of requirements is needed
    for this functionality to display as intended
    """
    def __init__(self, parent=None):
        super(AddConfigurationWidgets, self).__init__(parent)
        self._configuration = IntegrateConfigure()
        self.build_widget()

    @property
    def logger(self):
        return self._configuration.logger

    @property
    def logging_status_checkBox(self):
        return self._logging_status_checkBox
    
    @property
    def logging_location_label(self):
        return self._logging_location_label
    
    @property
    def logging_location_changeBtn(self):
        return self._logging_location_changeBtn

    @property
    def integrate_location_label(self):
        return self._integrate_location_label

    @property
    def integrate_location_changeBtn(self):
        return self._integrate_location_changeBtn

    @property
    def add_configuration(self):
        return self._configuration

    def set_integrate_location_label(self, value):
        self.integrate_location_label.setText('Output Location: {}'.format(value))

    def set_logging_location_label(self, value):
        self._logging_location_label.setText('Logging Location: {}'.format(value))

    def build_widget(self):
        self._h_layout = QtWidgets.QHBoxLayout()       

        spacer = QtWidgets.QSpacerItem(20, 20)

        self._integrate_location_label = QtWidgets.QLabel()
        self._integrate_location_label.setText('Output Location: {}'.format(self.add_configuration.output_location))
        self._integrate_location_changeBtn = QtWidgets.QPushButton()
        self._integrate_location_changeBtn.setMaximumHeight(23)
        self._integrate_location_changeBtn.setText('Change')

        self._logging_location_label = QtWidgets.QLabel()
        self._logging_location_label.setText('Logging Location: {}'.format(self.add_configuration.logging_location))
        self._logging_location_changeBtn = QtWidgets.QPushButton()
        self._logging_location_changeBtn.setMaximumHeight(23)
        self._logging_location_changeBtn.setText('Change')

        self._logging_status = QtWidgets.QLabel()
        self._logging_status.setText('Logging: ')
        self._logging_status_checkBox = QtWidgets.QCheckBox()
        self._logging_status_checkBox.setChecked(self.add_configuration.logging_option)

        self._h_layout.addWidget(self._integrate_location_label)
        self._h_layout.addWidget(self._integrate_location_changeBtn)
        self._h_layout.addItem(spacer)
        self._h_layout.addWidget(self._logging_location_label)
        self._h_layout.addWidget(self._logging_location_changeBtn)
        self._h_layout.addItem(spacer)
        self._h_layout.addWidget(self._logging_status)
        self._h_layout.addWidget(self._logging_status_checkBox)
        self.setLayout(self._h_layout)