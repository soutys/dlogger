# -*- coding: utf-8 -*-

'''Applications' windows module
'''

from __future__ import with_statement, division, absolute_import, print_function

import sys

from PyQt4 import (QtGui, uic)
#from PyQt4.QtCore import QEvent

__import__('resources')
from backend import DayLogger, get_label_slug


def get_call_info(obj, args, kwargs):
    '''Returns call-time info
    '''
    return '%s.%s(args=%s, kwargs=%s)' % (obj.__class__.__name__,
        sys._getframe(1).f_code.co_name, repr(args), repr(kwargs))



class SettingsDialog(QtGui.QDialog):
    '''Settings window class
    '''

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        uic.loadUi('ui/settings.ui', self)


    def file_sel_open(self):
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


    def mail_direct_select(self):
        '''Switches mode to direct mailing
        '''
        self._smtp_mode_select(False)


    def mail_smtp_select(self):
        '''Switches mode to via-SMTP mailing
        '''
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


    def _save_config(self, *args, **kwargs):
        '''Saves config
        '''
        print(get_call_info(self, args, kwargs))


    def _load_config(self, *args, **kwargs):
        '''Loads config
        '''
        print(get_call_info(self, args, kwargs))


    def settings_save(self):
        '''Saves settings, closes settings dialog
        '''
        self._save_config()
        self.close()


    def settings_cancel(self):
        '''Closes settings dialog
        '''
        self._load_config()
        self.close()


    def settings_def_restore(self, button):
        '''Restores default settings
        '''
        if self.btn_box.buttonRole(button) == QtGui.QDialogButtonBox.ResetRole:
            self._reset_settings()



class StatsDialog(QtGui.QDialog):
    '''Stats window class
    '''

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        uic.loadUi('ui/stats.ui', self)



class SystemTrayIcon(QtGui.QSystemTrayIcon):
    '''System tray icon class
    '''

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.setIcon(QtGui.QIcon(':/images/icon.png'))
        self.activated.connect(self.activate)
        self._wnd_visible = True


    def toggle_visibility(self):
        '''Toggles main window visibility
        '''
        print('pre-visible?:', self._wnd_visible)
        if self._wnd_visible:
            self.parent().hide()
        else:
            self.parent().show()
        self._wnd_visible = not self._wnd_visible
        print('post-visible?:', self._wnd_visible)


    def activate(self, reason):
        '''Click handler
        '''
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.toggle_visibility()



class MainWindow(QtGui.QMainWindow):
    '''Main window class
    '''

    def __init__(self, app):
        super(self.__class__, self).__init__()
        uic.loadUi('ui/main.ui', self)
        self.app = app
        self.app.aboutToQuit.connect(self._save_state)
        self.dlog = DayLogger()
        args = app.arguments()
        if len(args) >= 2:
            self.dlog.set_log(args[1])
        self.settings_dlg = SettingsDialog(self)
        self.stats_dlg = StatsDialog(self)
        self._load_dlog(self.dlog.get_log())
        self.show()

        self.systray_ico = SystemTrayIcon(self)
        self.systray_ico.show()

        self.installEventFilter(self)


    def eventFilter(self, qobject, qevent):
        '''Event filter method
        '''
#        qtype = qevent.type()
#        if qtype == QEvent.WindowStateChange:
#            print('qobject, qevent, qtype, visible?:', qobject, qevent, qtype,
#                self.isVisible())
#            self.systray_ico.toggle_visibility()
        return super(self.__class__, self).eventFilter(qobject, qevent)


    def _load_dlog(self, log_name):
        '''Loads d-log
        '''
        self.dlog.set_log(log_name)
        self.dlog.load_log()
        self.dlog.parse_data()
        self._reload_task_btns()


    def _save_state(self, *args, **kwargs):
        '''Saves the applications state
        '''
        print(get_call_info(self, args, kwargs))


    def menu_load(self):
        '''Prompts for d-log and loads it
        '''
        self.settings_dlg.file_sel_open()
        log_name = self.settings_dlg.file_edit.text()
        self._load_dlog(log_name)
        log_name = self.dlog.get_log()
        self.settings_dlg.file_edit.setText(log_name)


    def menu_show_stats(self):
        '''Shows stats
        '''
        stats_str = self.dlog.render_stats()
        self.stats_dlg.text_brwsr.setHtml('<pre>' + stats_str + '</pre>')
        self.stats_dlg.show()


    def menu_settings(self):
        '''Opens settings dialog (modal window)
        '''
        self.settings_dlg.show()


    def menu_exit(self):
        '''Closes the app
        '''
        self.app.closeAllWindows()


    @classmethod
    def _calc_task_btn_pos(cls, idx, cols_cnt):
        '''Calculates task button position (row, column)
        '''
        return divmod(idx, cols_cnt)


    def _get_task_btns(self):
        '''Returns all task buttons
        '''
        return self.scroll_area_widget.findChildren(QtGui.QPushButton)


    def _reload_task_btns(self):
        '''Reloads task buttons
        '''
        rows_cnt = self.grid_layout.rowCount()
        cols_cnt = self.grid_layout.columnCount()
        if rows_cnt and cols_cnt:
            for task_btn in self._get_task_btns():
                self.grid_layout.removeWidget(task_btn)
                task_btn.hide()
                task_btn.setParent(None)
                del task_btn

        for idx, slug in enumerate(self.dlog.iter_slugs()):
            row, col = self._calc_task_btn_pos(idx, cols_cnt)

            task_btn = QtGui.QPushButton(self.scroll_area_widget)
            task_btn.setEnabled(True)
            size_policy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
            size_policy.setHorizontalStretch(0)
            size_policy.setVerticalStretch(0)
            size_policy.setHeightForWidth(task_btn.sizePolicy()\
                .hasHeightForWidth())
            task_btn.setSizePolicy(size_policy)
            task_btn.setCheckable(True)
            task_btn.setChecked(False)
            task_btn.setObjectName('task_btn_{}'.format(idx))
            task_btn.setText(slug)
            task_btn.clicked.connect(self.task_start_slot_factory(slug))
            self.grid_layout.addWidget(task_btn, row, col, 1, 1)
            task_btn.show()


    def _recheck_task_btns(self, slug_curr):
        '''Restores state for task buttons
        '''
        for task_btn in self._get_task_btns():
            slug = task_btn.text()
            if slug_curr == slug:
                task_btn.setChecked(True)
                task_btn.setEnabled(False)
            else:
                task_btn.setChecked(False)
                task_btn.setEnabled(True)


    def new_task_add(self):
        '''Adds new task
        '''
        label = self.new_task_edit.text()
        if not label.strip():
            return
        self.new_task_edit.setText('')
        if not self.dlog.get_log():
            self._load_dlog(None)
        self.dlog.add_log_item(label)
        self._reload_task_btns()
        slug = get_label_slug(label)
        self._recheck_task_btns(slug)


    def task_start_slot_factory(self, slug):
        '''Factory for a `task_start()` slot
        '''
        return lambda: self.task_start(slug)


    def task_start(self, slug):
        '''Task start action
        '''
        if not slug.strip():
            return
        if not self.dlog.get_log():
            self._load_dlog(None)
        self.dlog.add_log_item(slug)
        self._recheck_task_btns(slug)


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
