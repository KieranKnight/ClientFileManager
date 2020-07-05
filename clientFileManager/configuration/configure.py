# -*- coding: utf-8 -*-

################################################################################
## INGEST TOOL - PLACING FILES INTO A DESIRED LOCATION AND TRACKING THEM
##
## File : configure.py
## Description : This file is to handle default and any configuration files the
##              user may have added. The configuration handles output, logging and
##              shotgun usability/access.
##
## Created by: Kieran Knight
## Email: kieransknight@gmail.com
## 
################################################################################

# Python Modules
import os
import re
import sys
import json
from pathlib import Path

# Application
from utils import (
    read_json, 
    write_json,
    _DEFAULT_CONFIG
)
from paths import (
    _APP_LOCATION,
    _UI_CONFIG_FOLDER, 
    _UI_CONFIGURATION,
    _LOGGING_LOCATION
)


class IntegrateConfigure(object):
    """
    Main configuration object.
    This object is ran once the tool is loaded, besides the get_seq_shot_folders
    which can be called throughout the main launch_manager module.
    """
    def __init__(self):
        super(IntegrateConfigure, self).__init__()
        self._configuration = read_json(_UI_CONFIGURATION)
        
        self.check_configuration()
        self.read_congifuration()
        self.get_seq_shot_folders()
    
    @property
    def logging(self):
        return self._logging

    @property
    def output_location(self):
        return self._output_location

    @output_location.setter
    def output_location(self, value):
        self._output_location = value

    @property
    def output_subfolders(self):
        return self._output_subfolders
    
    @property
    def logging_location(self):
        return self._logging_location

    @logging_location.setter
    def logging_location(self, value):
        self._logging_location = value

    @property
    def configuration(self):
        return self._configuration

    def check_configuration(self):
        """
        Checking the configuration file to set the options 
        on the main UI itself.
        """
        if not os.path.exists(_APP_LOCATION):
            os.makedirs(_APP_LOCATION)
        if not os.path.exists(_UI_CONFIGURATION):
            os.makedirs(_UI_CONFIG_FOLDER)
            write_json(_DEFAULT_CONFIG)
        if not os.path.exists(_LOGGING_LOCATION):
            os.makedirs(_LOGGING_LOCATION)
    
    def read_congifuration(self):
        """
        Readling the configuration file and setting the widget property values.
        """
        self._logging = True if self.configuration['loggingStatus'] == 'True' else False
        self._output_location = self.configuration['outputLocation']
        self._logging_location = self.configuration['loggingLocation']

    def get_seq_shot_folders(self):
        """
        When the tool loads or when the output location has been changed,
        this method is ran to collect the top and sub folder of the new output location.
        This gives users the option to select folders as a sequence and shot option.
        Users are still able to write their own Sequence and Shot folders ontop of this too.
        """
        self._output_subfolders = {}

        if not os.path.exists(self.output_location):
            os.makedirs(self.output_location)

        _top_folder = os.listdir(self.output_location)

        if _top_folder:
            for seq in _top_folder:
                _shot = os.path.join(self.output_location, seq)
                if os.path.isfile(_shot):
                    continue
                _shot = os.listdir(os.path.join(self.output_location, seq))
                if not _shot:
                    self._output_subfolders[os.path.join(self.output_location, seq)] = []
                else:
                    self._output_subfolders[os.path.join(self.output_location, seq)] = []
                    for shot in _shot:
                        self._output_subfolders[os.path.join(self.output_location, seq)].append(os.path.join(self.output_location, shot))

    def update_all_items(self, main):
        """
        Function to update all QTreeItems to a newly updated output location
        ie. getting the sequence and shot data to populate into the UI.

        Args:
            main (The QTreeWidget): The main QTreeWidget to loop through
        """
        for child in range(main.childCount()):
            _item = main.child(child)
            _item.sequence.clear()
            _sub_item = _item.childCount()
            self.add_updates_items(_item)
            if not _sub_item:
                continue
            for sub in range(_sub_item):
                _sub_widget = _item.child(sub)
                _sub_widget.sequence.clear()
                self.add_updates_items(_sub_widget)

    def add_updates_items(self, item):
        """
        For loop to update and add all new sequence items to 
        the QTreeWidgets.

        Args:
            item (CustomTreeItem): The Item that will be getting the new
                updates added to.
        """
        {
            item.sequence.addItem(str(os.path.basename(key)))
            for (key, value) in self.output_subfolders.items()
        }


class ConfigureFilesData(object):
    """
    Configuration object for client files that get added to the application
    Object tries to figuration a naming convention for the client file.
    It is a best guess situation however, the users are able to manipulate this
    if they are not quite happy with the convention that gets calculated.

    Returns:
        ConfigureFilesData Obj: The object itself.
    """
    _NAME_REGEX = r'(\w+?)|(\w+?)(\d+)|(\w+?)(_\d+)'
    def __init__(self, file, folder, parent_folder=None):
        super(ConfigureFilesData, self).__init__()
        self._file_path = file
        self._folder_path = folder
        self._parent_folder = parent_folder
        self._folder = os.path.dirname(file)
        self._filename = os.path.basename(file)
        self._file_location = 'plates'

        self.get_naming_info()

    @property
    def file_path(self):
        return self._file_path

    @property
    def file_size(self):
        return Path(self.file_path).stat().st_size
        
    @property
    def filename(self):
        return os.path.basename(self._filename)
    
    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def folder(self):
        return str(self._folder_path)
    
    @property
    def parent_folder(self):
        return str(self._parent_folder)

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, value):
        self._sequence = value

    @property
    def shot(self):
        return self._shot

    @shot.setter
    def shot(self, value):
        self._shot = value

    def get_naming_info(self):
        """ 
        Attempting to get the naming information from the file
        that has been passed in. This will try to find the sequence and the
        shot name.

        These will be stored into a dictionary
        """
        res = [re.findall(self._NAME_REGEX, self._filename)[0]][0]
        self.sequence = res[0]
        self.shot = "_".join((res[0], res[1]))


class ConfigureFiles(object):
    def __init__(self, folder=None):
        super(ConfigureFiles, self).__init__()
        
        self._files = []
        self._type = None
        self._folder = None

        self._folder = folder

    @property
    def files(self):
        return self._files

    @property
    def cumulative_size(self):
        _value = 0
        for file in self.files:
            _value += file.file_size
        return _value
    
    def single_file(self, file):
        self._files.append(ConfigureFilesData(file, self._folder))

    def folder_files(self, folder):
        """
        Looping through the passed folder to find
        all files whilst keeping the parent folder for reference.

        Arguments:
            folder (str) -- The folder path that will be quieried.
        
        Returns:
            list: A list of files that have been found.
        """
        for file in os.listdir(folder):
            _full_path = os.path.join(folder, file)
            if os.path.isfile(_full_path):
                self._files.append(ConfigureFilesData(_full_path, folder, parent_folder=self._folder))
            elif os.path.isdir(_full_path):
                self.folder_files(_full_path)

        



        

