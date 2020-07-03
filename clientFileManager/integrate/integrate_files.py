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
    def __init__(self, root, children, ui_main=None):
        super(IntegrateFiles, self).__init__()

        self._integrate_files = []

        self._root = root
        self._child_count = children
        self._ui_main = ui_main

        _can_run = self.check_all_integration()
        if not _can_run:
            return
        self._run()

    def check_all_integration(self):
        for i in range(self._child_count):
            _item = self._root.child(i)
            _sub_item = _item.childCount()
            if _item.option.currentText() == 'Ignore':
                continue
            if not _sub_item:
                _paths = self.check_paths(_item)
                if not _paths:
                    return False
                self._integrate_files.append(_item)
            for sub in range(_sub_item):
                _sub_widget = _item.child(sub)
                if _sub_widget.option.currentText() == 'Ignore':
                    continue
                _sub_paths = self.check_paths(_sub_widget)
                if not _sub_paths:
                    return False
                self._integrate_files.append(_sub_widget)
        return True

    def check_paths(self, item):
        if not item.sequence.currentText() and not item.shot.currentText() and not item.location.currentText():
            print('Sequence, Shot and Location are required to Integrate client files correctly.\' \
                nPlease make sure these are filled out correctly')
            return False
        return True

    def _run(self):
        _cmds = []
        for client_file in self._integrate_files:
            _output = client_file.location.currentText()
            _sequence = client_file.sequence.currentText()
            _shot = client_file.shot.currentText()
            _output_seq_shot = os.path.join(_output, _sequence, _shot)
            if not os.path.exists(_output_seq_shot):
                print('folder does not exist')
                os.makedirs(_output_seq_shot)
            
            src = os.path.join(client_file.item_contents.folder, client_file.filename.text())
            dst = os.path.join(_output_seq_shot, client_file.option.currentText(), client_file.filename.text())
            _cmd = 'cmd /c echo F | xcopy /R /Y /K "{src}" "{dst}"'.format(src=src, dst=dst)
            integrate = subprocess.Popen(_cmd, shell=True, stdout=subprocess.PIPE)
            integrate_str = integrate.communicate()[0].strip()
            print('Copied: {0} from {1}'.format(src, dst))
            if not os.path.exists(dst):
                print('Failed to copy file {}'.format(dst))
            [
                wdg.setStyleSheet('background-color: orange;') 
                if client_file.option.currentText() == 'Ignore' else 
                wdg.setStyleSheet('background-color: green;') 
                for wdg in client_file.items
            ]