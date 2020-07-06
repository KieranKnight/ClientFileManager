# -*- coding: utf-8 -*-

################################################################################
## INGEST TOOL - PLACING FILES INTO A DESIRED LOCATION AND TRACKING THEM
##
## File : integrate_files.py
## Description : Taking the files that have been added to the UI and placing 
##               them into the desired locations on disk.
##
## Created by: Kieran Knight
## Email: kieransknight@gmail.com
## 
################################################################################


# Python Modules
import os
import sys
import subprocess

class IntegrateFiles(object):
    def __init__(self, root, children, ui_main=None, app_logging=False, save_logging=False):
        super(IntegrateFiles, self).__init__()

        self._failed = []

        self._root = root
        self._child_count = children
        self._ui_main = ui_main
        self._app_logging = app_logging
        self._save_logging = save_logging

        _can_run = self.check_all_integration()
        if not _can_run:
            return

    def check_all_integration(self):
        """
        Checking the files inside of the tree widget
        to make sure the files are renderable and processed 
        correctly.

        Directly goes to the copy method to copy individual files
        rather than looping through items twice. This saves
        querying the widgets for a second time.
        """
        for child in range(self._child_count):
            _item = self._root.child(child)
            _sub_item = _item.childCount()
            if _item.option.currentText() == 'Ignore':
                _msg = '{} is set to ignore - will not be integrating'.format(
                    _item.item_contents.file_path
                )
                self._app_logging.info(_msg)
                continue
            if not _sub_item:
                _msg = '{} - Checking widget is set correctly'.format(_item.item_contents.file_path)
                self._app_logging.info(_msg)
                _paths = self.check_paths(_item)
                if not _paths:
                    return False
                self._run(_item)
            for sub in range(_sub_item):
                _sub_widget = _item.child(sub)
                if _sub_widget.option.currentText() == 'Ignore':
                    _msg = '{} is set to ignore - will not be integrating'.format(
                        _sub_widget.item_contents.file_path
                    )
                    self._app_logging.info(_msg)
                    continue
                _sub_paths = self.check_paths(_sub_widget)
                if not _sub_paths:
                    return False
                self._run(_sub_widget)
                if not self._failed:
                    self.update_all_widgets(_item)

    def check_paths(self, item):
        if not item.sequence.currentText() and not item.shot.currentText() and not item.location.currentText():
            self._app_logging.error('Sequence, Shot and Location are required to Integrate client files correctly.\' \
                nPlease make sure these are filled out correctly')
            return False
        return True

    def _run(self, c_file):
        """
        The main copying function to take the files from the client location
        to the desired output location.

        Args:
            c_file (CustomTreeWidget Obj): The custom tree widget object displayed in the UI.
        """
        self._app_logging.info('Starting Copy for Item - {}'.format(c_file.item_contents.file_path))
        _output = c_file.location.currentText()
        _sequence = c_file.sequence.currentText()
        _shot = c_file.shot.currentText()
        _output_seq_shot = os.path.join(_output, _sequence, _shot)
        if not os.path.exists(_output_seq_shot):
            self._app_logging.error('Folder does not exist - Creating required folder')
            os.makedirs(_output_seq_shot)
        
        src = os.path.join(c_file.item_contents.folder, c_file.filename.text())
        dst = os.path.join(_output_seq_shot, c_file.option.currentText(), c_file.filename.text())
        _cmd = 'cmd /c echo F | xcopy /R /Y /K "{src}" "{dst}"'.format(src=src, dst=dst)
        integrate = subprocess.Popen(_cmd, shell=True, stdout=subprocess.PIPE)
        integrate_str = integrate.communicate()[0].strip()
        if not os.path.exists(dst):
            self._failed.append(c_file)
            self._app_logging.error('Failed to copy file {}'.format(dst))
            [
            wdg.setStyleSheet('background-color: red; border: 1.5px solid #32414B') 
            for wdg in c_file.items
            ]
            return
        self._app_logging.info('successfully Copied: {0} from {1}'.format(src, dst))
        self.update_all_widgets(c_file)

    def update_all_widgets(self, c_file):
        """
        Updating all of the widgets within the Custom QTreeWidgetItem.
        Updates all widgets with the correct colouring.

        Args:
            c_file (CustomTreeWidget Obj): The custom tree widget object displayed in the UI.
        """
        [
            wdg.setStyleSheet('background-color: #885007; border: 1.5px solid #32414B') 
            if c_file.option.currentText() == 'Ignore' else 
            wdg.setStyleSheet('background-color: #099008; border: 1.5px solid #32414B') 
            for wdg in c_file.items
        ]
