# -*- coding: utf-8 -*-
"""This module provides facility for editinglibrary data

The module is intended for skinners to provide access to the addon via a button
that will call RunScript.

Usage:
    Start script using Kodi Runscript builtin.  Invokation parameters are:
        DBID:  The libaray DBID of item to be modified
        type:  Media type
        tag:
    Example:
        Runscript(script.libraryeditor,DBID=$INFO[ListItem.DBID])
    The script loads a Select Dialog that shows current values and allows user
    editing.  User "OK" button updates the library.
"""

from resources.lib.main import log, Main

if __name__ == "__main__":
    Main()
log('finished')
