# -*- coding: utf-8 -*-

'''Applications' windows module
'''

from __future__ import with_statement, division, absolute_import, print_function

import sys

from PyQt4 import (QtCore, QtGui, uic)


def get_call_info(obj, args, kwargs):
    return '%s.%s(args=%s, kwargs=%s)' % (obj.__class__.__name__,
        sys._getframe(1).f_code.co_name, repr(args), repr(kwargs))



class SettingsDialog(QtGui.QDialog):
    '''Settings window class
    '''

    def __init__(self, *args, **kwargs):
        print (get_call_info(self, args, kwargs))
        super(self.__class__, self).__init__(*args, **kwargs)
        uic.loadUi('ui/settings.ui', self)


    def file_sel_open(self, *args, **kwargs):
        '''Opens file selection dialog
        '''
        fname = QtGui.QFileDialog.getOpenFileName(self, self.tr('Open d-log'),
            '', self.tr('D-log files (*.dlog)'))
        self.file_edit.setText(fname)


    def _smtp_mode_select(self, enabled):
        '''Switches mailing mode controls
        '''
        self.smtp_host_lbl.setEnabled(enabled)
        self.smtp_host_edit.setEnabled(enabled)
        self.smtp_port_lbl.setEnabled(enabled)
        self.smtp_port_edit.setEnabled(enabled)
        self.smtp_login_lbl.setEnabled(enabled)
        self.smtp_login_edit.setEnabled(enabled)
        self.smtp_passwd_lbl.setEnabled(enabled)
        self.smtp_passwd_edit.setEnabled(enabled)


    def mail_direct_select(self, *args, **kwargs):
        '''Switches mode to direct mailing
        '''
        print (get_call_info(self, args, kwargs))
        self._smtp_mode_select(False)


    def mail_smtp_select(self, *args, **kwargs):
        '''Switches mode to via-SMTP mailing
        '''
        print (get_call_info(self, args, kwargs))
        self._smtp_mode_select(True)


    def _reset_settings(self):
        '''Resets settings dialog controls
        '''
        self.file_edit.setText('')
        self.email_edit.setText('')
        self.mail_direct_btn.setChecked(True)
        self._smtp_mode_select(False)
        self.smtp_host_edit.setText('')
        self.smtp_port_edit.setText('')
        self.smtp_login_edit.setText('')
        self.smtp_passwd_edit.setText('')


    def settings_def_restore(self, button):
        '''Restores default settings
        '''
        print (get_call_info(self, (button,), {}))
        if self.btn_box.buttonRole(button) == QtGui.QDialogButtonBox.ResetRole:
            self._reset_settings()


    def _save_config(self, *args, **kwargs):
        '''Saves config
        '''
        print (get_call_info(self, args, kwargs))


    def _load_config(self, *args, **kwargs):
        '''Loads config
        '''
        print (get_call_info(self, args, kwargs))


    def settings_save(self, *args, **kwargs):
        '''Saves settings, closes settings dialog
        '''
        print (get_call_info(self, args, kwargs))
        self._save_config()


    def settings_cancel(self, *args, **kwargs):
        '''Closes settings dialog
        '''
        print (get_call_info(self, args, kwargs))
        self._load_config()



class MainWindow(QtGui.QMainWindow):
    '''Main window class
    '''

    def __init__(self, app):
        super(self.__class__, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.app = app
        self.app.aboutToQuit.connect(self._save_state)
        self.settings_dlg = SettingsDialog(self)
        self.show()


    def _load_dlog(self, *args, **kwargs):
        '''Loads d-log
        '''
        print (get_call_info(self, args, kwargs))


    def _save_state(self, *args, **kwargs):
        '''Saves the applications state
        '''
        print (get_call_info(self, args, kwargs))


    def menu_load(self, *args, **kwargs):
        '''Prompts for d-log and loads it
        '''
        self.settings_dlg.file_sel_open()
        fname = self.settings_dlg.file_edit.text()
        self._load_dlog()


    def menu_show_log(self, *args, **kwargs):
        '''Shows d-log as a list
        '''
        print (get_call_info(self, args, kwargs))


    def menu_settings(self, *args, **kwargs):
        '''Opens settings dialog (modal window)
        '''
        print (get_call_info(self, args, kwargs))
        self.settings_dlg.show()


    def menu_exit(self, *args, **kwargs):
        '''Closes the app
        '''
        self.app.closeAllWindows()


    def new_task_add(self, *args, **kwargs):
        '''Adds task
        '''
        print (get_call_info(self, args, kwargs))


    def task_1_start(self, *args, **kwargs):
        '''
        '''
        print (get_call_info(self, args, kwargs))


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
