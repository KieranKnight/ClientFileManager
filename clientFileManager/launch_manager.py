# -*- coding: utf-8 -*-

################################################################################
## Client File Manager TOOL - Ingesting client files into a production pipeline
##  with tracking, logging and configuration overrides.
##
## File : launch_manager.py
## Description : The main file to launch the UI for the ingest tool.
##
## Created by: Kieran Knight
## Email: kieransknight@gmail.com
## 
################################################################################

# Python Modules
import os
import sys

# Application - ui_items
from configuration.configure import ConfigureFiles
from third_party.Qt import QtWidgets, QtCore, QtGui
from integrate.integrate_files import IntegrateFiles
from ui_items.customTreeWidget import CustomTreeWidget
from logger.application_logging import IntegrateLogger
from paths import _USER_DOCUMENTS
from ui_items.addWidgets import (
    GroupWidgets, 
    AddClientItemsButtons, 
    AddIntegrateButton, 
    AddConfigurationWidgets,
    AddSaveConfigurationWidget
)
from utils import (
    open_file, 
    open_folder, 
    write_json, 
    read_css, 
    _DEFAULT_CONFIG
)

class ClientFileManager(QtWidgets.QMainWindow):
    _OBJ_NAME = 'Client File Manager'
    def __init__(self, parent=None):
        super(ClientFileManager, self).__init__(parent=parent)

        # setting up the UI 
        self.setWindowTitle(self._OBJ_NAME)
        self.setStyleSheet(read_css())
        self.centralwidget = QtWidgets.QWidget(self)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)

        self.configuration_widgets = AddConfigurationWidgets(parent=self.centralwidget)
        self.configuration_widgets_grp = GroupWidgets([self.configuration_widgets], 'Configuration')
        
        self.save_configuration = AddSaveConfigurationWidget(parent=self.centralwidget)
        self.save_configuration_grp = GroupWidgets([self.save_configuration], '')
        
        # Creating the tree widget
        self.tree_widget = CustomTreeWidget(parent=self.centralwidget)
        self.tree_grp = GroupWidgets([self.tree_widget], 'Client Files')

        # Add Buttons to add or remove files/Folders
        self.client_buttons = AddClientItemsButtons(parent=self.centralwidget)
        self.client_buttons_grp = GroupWidgets([self.client_buttons], 'Add Client Files')

        self.integrate_buttons = AddIntegrateButton(parent=self.centralwidget)
        self.integrate_buttons_grp = GroupWidgets([self.integrate_buttons], 'Integrate')
        
        # adding the widgets to the layout
        self.verticalLayout.addWidget(self.configuration_widgets_grp)
        self.verticalLayout.addWidget(self.save_configuration_grp)
        self.verticalLayout.addWidget(self.tree_grp)
        self.verticalLayout.addWidget(self.client_buttons_grp)
        self.verticalLayout.addWidget(self.integrate_buttons_grp)
        
        self.setCentralWidget(self.centralwidget)

        self.build_connections()

        self._output_locations = self.configuration_widgets.add_configuration.output_subfolders
    
    def build_connections(self):
        self.configuration_widgets.logging_location_changeBtn.clicked.connect(self.change_logging_location)
        self.configuration_widgets.integrate_location_changeBtn.clicked.connect(self.change_integrate_location)
        self.save_configuration.save_configuration.clicked.connect(self.save_configuration_overrides)
        self.client_buttons.add_file_btn.clicked.connect(self.open_file)
        self.client_buttons.add_folder_btn.clicked.connect(self.open_folder)
        self.client_buttons.remove_btn.clicked.connect(self.remove_selected)
        self.integrate_buttons.integrate_btn.clicked.connect(self.integrate_client_files)

    def change_integrate_location(self):
        selected_folder = open_folder(self, 'Change Folder', _USER_DOCUMENTS, 'All Folders (*)')
        if not selected_folder:
            self.configuration_widgets.logger.warning('No Folder has been selected.')
            return
        self.configuration_widgets.set_integrate_location_label(selected_folder)
        self.configuration_widgets.add_configuration.output_location = selected_folder
        self.configuration_widgets.add_configuration.get_seq_shot_folders()
        self.configuration_widgets.logger.info('Integration Location Changed.')
        root = self.tree_widget.invisibleRootItem()
        child_count = root.childCount()
        if not child_count:
            return
        self.configuration_widgets.add_configuration.update_all_items(root)
        
    def change_logging_location(self):
        selected_folder = open_folder(self, 'Change Folder', _USER_DOCUMENTS, 'All Folders (*)')
        if not selected_folder:
            self.configuration_widgets.logger.warning('No Folder has been selected.')
            return
        self.configuration_widgets.set_logging_location_label(selected_folder)
        self.configuration_widgets.add_configuration.logging_location = selected_folder
        self.configuration_widgets.logger.info('Logging Location Changed.')

    def save_configuration_overrides(self):
        _logging_location = self.configuration_widgets.logging_location_label.text().replace('Logging Location: ', '')
        _output_location = self.configuration_widgets.integrate_location_label.text().replace('Output Location: ', '')
        _DEFAULT_CONFIG = {
            'loggingLocation': self.configuration_widgets.logging_location_label.text().replace('Logging Location: ', ''),
            'outputLocation': self.configuration_widgets.integrate_location_label.text().replace('Output Location: ', ''),
            'loggingStatus': 'True' if self.configuration_widgets.logging_status_checkBox.isChecked() else 'False'
        }

        write_json(_DEFAULT_CONFIG)

    def open_file(self):
        selected_file = open_file(self, 'Add File', _USER_DOCUMENTS, 'All Files (*)')
        if not selected_file:
            self.configuration_widgets.logger.warning('No file has been selected.')
            return
        self.configuration_widgets.logger.info('Processing File - {}'.format(selected_file))
        _configure_object = ConfigureFiles(folder=os.path.dirname(selected_file))
        _configure_object.single_file(selected_file)
        self.tree_widget.add_items(_configure_object, self.configuration_widgets)

    def open_folder(self):
        selected_folder = open_folder(self, 'Add Folder', _USER_DOCUMENTS, 'All Folders (*)')
        if not selected_folder:
            self.configuration_widgets.logger.warning('No Folder has been selected.')
            return
        self.configuration_widgets.logger.info('Processing Folder - {}'.format(selected_folder))
        _configure_object = ConfigureFiles(folder=selected_folder)
        _configure_object.folder_files(selected_folder) 
        self.tree_widget.add_items(_configure_object, self.configuration_widgets)

    def remove_selected(self):
        if not self.tree_widget.selectedItems():
            self.configuration_widgets.logger.warning('Nothing has been selected. Please select an item and try again.')
            return
        _selected_items = self.tree_widget.selectedItems()
        root = self.tree_widget.invisibleRootItem()
        [(item.parent() or root).removeChild(item) for item in _selected_items]

    def integrate_client_files(self):
        self.configuration_widgets.logger.info('Starting to integrate client files...')
        if self.configuration_widgets.logging_status_checkBox.isChecked:
            save_integrate_logging = IntegrateLogger(
                self.configuration_widgets.logging_location_label.text().replace('Logging Location: ', '')
            )
        root = self.tree_widget.invisibleRootItem()
        child_count = root.childCount()
        if not child_count:
            self.configuration_widgets.logger.warning('No Client Files have been added.')
            return
        _integrate = IntegrateFiles(
            root, 
            child_count, 
            ui_main=self,
            app_logging=self.configuration_widgets.logger,
            save_logging=save_integrate_logging)

def launchUI():
    """
    Opening the UI and resizing the window
    """
    app = QtWidgets.QApplication(sys.argv)
    ui = ClientFileManager()
    ui.resize(1200, 650)
    ui.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launchUI()