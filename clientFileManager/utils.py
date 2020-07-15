################################################################################
## Client File Manager TOOL - Ingesting client files into a production pipeline
##  with tracking, logging and configuration overrides.
##
## File : utils.py
## Description : This file is used functions throughout the application.
##
## Created by: Kieran Knight
## Email: kieransknight@gmail.com
## 
################################################################################

# Python Modules
import os
import sys
import json
import getpass
from pathlib import Path

# Application
from paths import _CSS, _INTEGRATE_LOCATION, _LOGGING_LOCATION, _UI_CONFIGURATION
from third_party.Qt import _loadUi
from third_party.Qt import QtWidgets

_INGEST_FOLDERS = [
        'Elements', 
        'mocap',
        'plates', 
        'reference', 
        'tracking', 
        'model', 
        'textures'
    ]

_DEFAULT_CONFIG = {
    'loggingLocation': _LOGGING_LOCATION,
    'outputLocation': _INTEGRATE_LOCATION,
    'loggingStatus': 'True'
}


def open_file(instance, title, location, filter):
    """
    Opening a file dialog to select a sinlge file to be ingested.

    Arguments:
        instance {MainClassInstance} -- The main ingest window instance.
        title {str} -- The title of the dialog window.
        location {str} -- The location on where the file dialog will open up to.
        filter {str} -- The filter to be used on what files can be added.
    
    Returns:
        path -- A path object of the location that has just been selected.
    """
    file_dialog = QtWidgets.QFileDialog.getOpenFileName(instance, title, location, filter)[0]
    if file_dialog == '':
        return False
    return Path(file_dialog)


def open_folder(instance, title, location, filter):
    """
    Opening a file dialog to select a folder to items to be ingested.
    
    Arguments:
        instance {MainClassInstance} -- The main ingest window instance.
        title {str} -- The title of the dialog window.
        location {str} -- The location of where the file dialog will open up to.
        filter {str} -- The filter to be used on what can be added.

    Returns:
        path -- A path object of the folder location that has been selected.
    """
    dialog = QtWidgets.QFileDialog(instance, title, location, filter)
    dialog.setFileMode(QtWidgets.QFileDialog.DirectoryOnly)
    if not dialog.exec_() == QtWidgets.QDialog.Accepted:
        return False
    return Path(dialog.selectedFiles()[0])


def read_css(css_file=_CSS):
    """
    Reading the CSS file for the application

    Returns:
        _css : The CSS sheet for the application
    """
    with open(_CSS) as css:
        _css = css.read()
    return _css


def read_json(json_file):
    """
    Reading the contents of a json file.
    
    Arguments:
        json_file {json} -- The Json file that will be read.
    
    Returns:
        dict -- The json file in a python dictionary.
    """
    with open(json_file) as f:
        data = json.load(f)
    return data


def write_json(data):
    """
    Writing dictionary contents to a json file.

    Args:
        data (dict) -- The dictionary that will be placed 
            into the json file.

    Returns:
        JsonPath -- The path to the json file. 
    """
    with open(_UI_CONFIGURATION, 'w') as json_file:
        json.dump(data, json_file)
