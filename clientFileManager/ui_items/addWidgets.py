from configuration.configure import IntegrateConfigure

from third_party.Qt import QtWidgets, QtCore, QtGui


class GroupWidgets(QtWidgets.QGroupBox):
    def __init__(self, widgets, title, margin=0, parent=None):
        super(GroupWidgets, self).__init__(title, parent)
        self.setFlat(True)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(margin, margin, margin, margin)
        [self.layout().addWidget(widget) for widget in widgets]


class BaseAddItems(QtWidgets.QWidget):
    _ATTRIBUTE_CLASSES = [property]
    def __init__(self, parent):
        super(BaseAddItems, self).__init__(parent)

        self._h_layout = QtWidgets.QHBoxLayout()
        self.build_widget()
        self.set_layout()
        
    def build_widget(self):
        raise NotImplementedError

    def _get_properties(self):
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
        [self._h_layout.addWidget(item) for key,item in self._get_properties().items()]
        self.setLayout(self._h_layout)


class AddClientItemsButtons(BaseAddItems):
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
        self._add_file_btn = QtWidgets.QPushButton()
        self._add_file_btn.setText('Add Single Client File')
        
        self._add_folder_btn = QtWidgets.QPushButton()
        self._add_folder_btn.setText('Add Client Folder')

        self._remove_btn = QtWidgets.QPushButton()
        self._remove_btn.setText('Remove Client File/Folder')


class AddIntegrateButton(BaseAddItems):
    def __init__(self, parent=None):
        super(AddIntegrateButton, self).__init__(parent)

    @property
    def integrate_btn(self):
        return self._integrate_btn

    def build_widget(self):
        self._integrate_btn = QtWidgets.QPushButton()
        self._integrate_btn.setText('Integrate Client Files')


class AddSaveConfigurationWidget(BaseAddItems):
    def __init__(self, parent=None):
        super(AddSaveConfigurationWidget, self).__init__(parent)

    @property
    def save_configuration(self):
        return self._save_configuration_btn

    def build_widget(self):
        self._save_configuration_btn = QtWidgets.QPushButton()
        self._save_configuration_btn.setText('Save Configuration Changes To File')


class AddConfigurationWidgets(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(AddConfigurationWidgets, self).__init__(parent)
        self._configuration = IntegrateConfigure()
        self.build_widget()

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
    def configuration(self):
        return self._configuration

    def set_integrate_location_label(self, value):
        self.integrate_location_label.setText('Output Location: {}'.format(value))

    def set_logging_location_label(self, value):
        self._logging_location_label.setText('Logging Location: {}'.format(value))

    def build_widget(self):
        self._h_layout = QtWidgets.QHBoxLayout()       

        spacer = QtWidgets.QSpacerItem(20, 20)

        self._integrate_location_label = QtWidgets.QLabel()
        self._integrate_location_label.setText('Output Location: {}'.format(self.configuration.output_location))
        self._integrate_location_changeBtn = QtWidgets.QPushButton()
        self._integrate_location_changeBtn.setMaximumHeight(23)
        self._integrate_location_changeBtn.setText('Change')

        self._logging_location_label = QtWidgets.QLabel()
        self._logging_location_label.setText('Logging Location: {}'.format(self.configuration.logging_location))
        self._logging_location_changeBtn = QtWidgets.QPushButton()
        self._logging_location_changeBtn.setMaximumHeight(23)
        self._logging_location_changeBtn.setText('Change')

        self._logging_status = QtWidgets.QLabel()
        self._logging_status.setText('Logging: ')
        self._logging_status_checkBox = QtWidgets.QCheckBox()
        self._logging_status_checkBox.setChecked(self.configuration.logging)

        self._h_layout.addWidget(self._integrate_location_label)
        self._h_layout.addWidget(self._integrate_location_changeBtn)
        self._h_layout.addItem(spacer)
        self._h_layout.addWidget(self._logging_location_label)
        self._h_layout.addWidget(self._logging_location_changeBtn)
        self._h_layout.addItem(spacer)
        self._h_layout.addWidget(self._logging_status)
        self._h_layout.addWidget(self._logging_status_checkBox)
        self.setLayout(self._h_layout)