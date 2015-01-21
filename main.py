#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Main (app) module
'''

# future syntax = on
from __future__ import with_statement, division, absolute_import, print_function

import sys

# older Pythons patch
if sys.version_info < (3, 0):
    from sip import setapi
    setapi('QDate', 2)
    setapi('QDateTime', 2)
    setapi('QString', 2)
    setapi('QTextStream', 2)
    setapi('QTime', 2)
    setapi('QUrl', 2)
    setapi('QVariant', 2)

from PyQt4 import QtGui

from windows import MainWindow


def main():
    '''Inits and atarts the app
    '''
    app = QtGui.QApplication(sys.argv)
    _ = MainWindow(app)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
