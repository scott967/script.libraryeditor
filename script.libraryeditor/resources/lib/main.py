# -*- coding: utf-8 -*-
"""This module provides facility for editinglibrary data.
It provides a GUI for editing the library data, and a function for updating
the library.
"""


__lazy_modules__ = ["json", "os", "xbmc",
                    "xbmcaddon", "xbmcgui", "dateutil.parser"]

import json
import os
import sys

import xbmc
import xbmcaddon
import xbmcgui
from dateutil import parser

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString


def log(txt: str) -> None:
    """writes output to Kodi log at DEBUG level

    Args:
        txt (str): text message to write into Kodi.log
    """

    message = f'{__addonid__}: {txt}'
    xbmc.log(msg=message, level=xbmc.LOGDEBUG)


class Main:
    """All functionality is provided in Main class
    """

    def __init__(self):
        """Constructor handles all execution
        """

        log(f'version {__addonversion__} started')
        self._parse_argv()
        if self.TAG != "":
            self._choose_action(self.TAG)
            log("choose_action executed")
        elif self.DBID != "":
            self._select_dialog()
        else:
            log("No DBID given")

    def _parse_argv(self):
        """Sets instance attributes from arguments
        """

        try:
            params = dict(arg.split('=') for arg in sys.argv[1].split('&'))
        except Exception:
            params = {}
        self.DBID = int(params.get('DBID', False))
        self.PARAM_TYPE = str(params.get('type', ""))
        self.TAG = str(params.get('tag', ""))

    def _select_dialog(self):
        """Loads Kodi select dialog when DBID parameter provideed
        The current active media window is used to determine the current media
        item type and appropriate database attributes exposed.
        """

        self.modeselect = []
        self.identifierlist = []
        if xbmc.getCondVisibility('Container.Content(movies)'):
            self.TYPE = "Movie"
            self._AddToList(xbmc.getLocalizedString(369), "title")
            self._AddToList(xbmc.getLocalizedString(171), "sorttitle")
            self._AddToList(xbmc.getLocalizedString(20376), "originaltitle")
            self._AddToList(xbmc.getLocalizedString(20473), "premiered")
            self._AddToList(xbmc.getLocalizedString(515), "genre")
            self._AddToList(xbmc.getLocalizedString(572), "studio")
            self._AddToList(xbmc.getLocalizedString(20459), "tag")
            self._AddToList(xbmc.getLocalizedString(20417), "writer")
            self._AddToList(xbmc.getLocalizedString(20339), "director")
            self._AddToList(xbmc.getLocalizedString(202), "tagline")
            self._AddToList(xbmc.getLocalizedString(207), "plot")
            self._AddToList(xbmc.getLocalizedString(203), "plotoutline")
            self._AddToList(xbmc.getLocalizedString(13409), "top250")
            self._AddToList(xbmc.getLocalizedString(20457), "set")
            self._AddToList(xbmc.getLocalizedString(21875), "country")
            self._AddToList(xbmc.getLocalizedString(20074), "mpaa")
            self._AddToList(xbmc.getLocalizedString(20410), "trailer")
            self._AddToList(xbmc.getLocalizedString(567), "playcount")
            self._AddToList(xbmc.getLocalizedString(563), "rating")
        elif xbmc.getCondVisibility('Container.Content(tvshows)'):
            self.TYPE = "TVShow"
            self._AddToList(xbmc.getLocalizedString(369), "title")
            self._AddToList(xbmc.getLocalizedString(20376), "originaltitle")
            self._AddToList(xbmc.getLocalizedString(515), "genre")
            self._AddToList(xbmc.getLocalizedString(207), "plot")
            self._AddToList(xbmc.getLocalizedString(20459), "tag")
            self._AddToList(xbmc.getLocalizedString(572), "studio")
            self._AddToList(xbmc.getLocalizedString(20074), "mpaa")
            self._AddToList(xbmc.getLocalizedString(567), "playcount")
            self._AddToList(xbmc.getLocalizedString(563), "rating")
            self._AddToList(__language__(32001), "premiered")
        elif xbmc.getCondVisibility('Container.Content(musicvideos)'):
            self.TYPE = "MusicVideo"
            self._AddToList(xbmc.getLocalizedString(369), "title")
            self._AddToList(xbmc.getLocalizedString(345), "year")
            self._AddToList(xbmc.getLocalizedString(515), "genre")
            self._AddToList(xbmc.getLocalizedString(20339), "director")
            self._AddToList(xbmc.getLocalizedString(207), "plot")
            self._AddToList(xbmc.getLocalizedString(20459), "tag")
            self._AddToList(xbmc.getLocalizedString(572), "studio")
            self._AddToList(xbmc.getLocalizedString(567), "playcount")
            self._AddToList(xbmc.getLocalizedString(558), "album")
            self._AddToList(xbmc.getLocalizedString(557), "arr_artist")
            self._AddToList(xbmc.getLocalizedString(554), "track")
        elif xbmc.getCondVisibility('Container.Content(episodes)'):
            self.TYPE = "Episode"
            self._AddToList(xbmc.getLocalizedString(369), "title")
            self._AddToList(xbmc.getLocalizedString(20376), "originaltitle")
            self._AddToList(xbmc.getLocalizedString(515), "genre")
            self._AddToList(xbmc.getLocalizedString(207), "plot")
            self._AddToList(xbmc.getLocalizedString(20339), "director")
            self._AddToList(xbmc.getLocalizedString(20417), "writer")
            self._AddToList(xbmc.getLocalizedString(20459), "tag")
            self._AddToList(xbmc.getLocalizedString(572), "studio")
            self._AddToList(xbmc.getLocalizedString(20074), "mpaa")
            self._AddToList(xbmc.getLocalizedString(567), "playcount")
            self._AddToList(xbmc.getLocalizedString(563), "rating")
            # self._AddToList( xbmc.getLocalizedString(20416),"firstaired" )
            # self._AddToList( xbmc.getLocalizedString(20416),"title" )
            self._AddToList(xbmc.getLocalizedString(20373), "season")
            self._AddToList(xbmc.getLocalizedString(20359), "episode")
        elif xbmc.getCondVisibility('Container.Content(artists)'):
            self.TYPE = "Artist"
            # self._AddToList( xbmc.getLocalizedString(557),"str_artist" )
            self._AddToList(xbmc.getLocalizedString(515), "artist_genre")
            self._AddToList(xbmc.getLocalizedString(21893), "born")
            self._AddToList(xbmc.getLocalizedString(21894), "formed")
            self._AddToList(xbmc.getLocalizedString(
                21821), "artist_description")
            self._AddToList(xbmc.getLocalizedString(21897), "died")
            self._AddToList(xbmc.getLocalizedString(21896), "disbanded")
            self._AddToList(xbmc.getLocalizedString(21898), "yearsactive")
            self._AddToList(xbmc.getLocalizedString(175), "artist_mood")
            self._AddToList(xbmc.getLocalizedString(176), "artist_style")
            self._AddToList(xbmc.getLocalizedString(21892), "instruments")
        elif xbmc.getCondVisibility('Container.Content(albums)'):
            self.TYPE = "Album"
            # self._AddToList( xbmc.getLocalizedString(369),"title" )
            # self._AddToList( xbmc.getLocalizedString(557),"arr_artist" )
            self._AddToList(xbmc.getLocalizedString(345), "year")
            self._AddToList(xbmc.getLocalizedString(175), "album_mood")
            self._AddToList(xbmc.getLocalizedString(176), "album_style")
            self._AddToList(xbmc.getLocalizedString(515), "album_genre")
            self._AddToList(xbmc.getLocalizedString(21895), "themes")
            # self._AddToList( xbmc.getLocalizedString(515),"type" )
            self._AddToList(xbmc.getLocalizedString(21899), "albumlabel")
            self._AddToList(xbmc.getLocalizedString(
                21821), "album_description")
            self._AddToList(xbmc.getLocalizedString(563), "rating")
        elif xbmc.getCondVisibility('Container.Content(songs)'):
            self.TYPE = "Song"
            self._AddToList(xbmc.getLocalizedString(369), "title")
            self._AddToList(xbmc.getLocalizedString(557), "arr_artist")
            self._AddToList(xbmc.getLocalizedString(558), "album")
            self._AddToList(xbmc.getLocalizedString(515), "genre")
            self._AddToList(xbmc.getLocalizedString(345), "year")
            self._AddToList(xbmc.getLocalizedString(563), "rating")
            self._AddToList(xbmc.getLocalizedString(569), "comment")
            self._AddToList(xbmc.getLocalizedString(427), "disc")
            self._AddToList(xbmc.getLocalizedString(554), "Track")
            self._AddToList("Delete File", "delete")
        dialogSelection = xbmcgui.Dialog()
        self.Edit_Selection = dialogSelection.select(
            __language__(32007), self.modeselect)
        if self.Edit_Selection == -1:
            return
        self._choose_action(self.identifierlist[self.Edit_Selection])
        self._select_dialog()

    def _choose_action(self, actionstring: str):
        """Creates an action from option selected by user in select dialog
        Select Dialog select method returns integer as index into the modeselect
        list.  Calls method based on action database attribute type

        Args:
            actionstring (str): element of modeselect list to edit
        """

        # override auto type
        log("choose_action executed")
        if self.PARAM_TYPE != "":
            self.TYPE = self.PARAM_TYPE
        match actionstring:
            case "title":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Title'), self.TYPE, "title")
            case "sorttitle":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Title'), self.TYPE, "sorttitle")
            case "originaltitle":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.OriginalTitle'), self.TYPE, "originaltitle")
            case "premiered":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Premiered'), self.TYPE, "premiered")
            case "episode":
                self._edit_db_integer(self.TYPE, "episode")
            case "season":
                self._edit_db_integer(self.TYPE, "season")
            case "track":
                self._edit_db_integer(self.TYPE, "track")
            case "disc":
                self._edit_db_integer(self.TYPE, "disc")
            case "genre":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Genre'), self.TYPE, "genre")
            case "artist_genre":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_Genre)'), self.TYPE, "genre")
            case "album_genre":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Album_Genre)'), self.TYPE, "genre")
            case "writer":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Writer'), self.TYPE, "writer")
            case "director":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Director'), self.TYPE, "director")
            case "tagline":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Tagline'), self.TYPE, "tagline")
            case "plot":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Plot'), self.TYPE, "plot")
            case "plotoutline":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.PlotOutline'), self.TYPE, "plotoutline")
            case "top250":
                self._edit_db_integer(self.TYPE, "top250")
            case "set":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Set'), self.TYPE, "set")
            case "tag":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Tag'), self.TYPE, "tag")
            case "country":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Country'), self.TYPE, "country")
            case "studio":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Studio'), self.TYPE, "studio")
            case "mpaa":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Mpaa'), self.TYPE, "mpaa")
            case "trailer":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Trailer'), self.TYPE, "trailer")
            case "playcount":
                self._edit_db_integer(self.TYPE, "playcount")
            case "rating":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Rating'), self.TYPE, "rating")
            case "arr_artist":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Artist'), self.TYPE, "artist")
            case "str_artist":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Artist'), self.TYPE, "artist")
            case "albumlabel":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(Album_Label)'), self.TYPE, "albumlabel")
            case "album":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Album'), self.TYPE, "album")
            case "tracknumber":  # TrackNumber (needs checking)
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.TrackNumber'), self.TYPE, "track")
            case "firstaired":  # firstaired (needs checking)
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Premiered'), self.TYPE, "firstaired")
            case "born":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(artist_Born)'), self.TYPE, "born")
            case "formed":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(artist_Formed)'), self.TYPE, "formed")
            case "artist_description":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_Description)'), self.TYPE, "description")
            case "album_description":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(Album_Description)'), self.TYPE, "description")
            case "died":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_Died)'), self.TYPE, "died")
            case "disbanded":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_Disbanded)'), self.TYPE, "disbanded")
            case "yearsactive":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_YearsActive)'), self.TYPE, "yearsactive")
            case "comment":
                self._edit_db_string(xbmc.getInfoLabel(
                    'ListItem.Comment'), self.TYPE, "comment")
            case "artist_mood":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_Mood)'), self.TYPE, "mood")
            case "artist_style":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_Style)'), self.TYPE, "style")
            case "album_mood":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Album_Mood)'), self.TYPE, "mood")
            case "album_style":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Album_Style)'), self.TYPE, "style")
            case "instruments":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Artist_Instrument)'), self.TYPE, "instrument")
            case "themes":
                self._edit_db_array(xbmc.getInfoLabel(
                    'ListItem.Property(Album_Theme)'), self.TYPE, "theme")
            case "delete":
                os.unlink(xbmc.getInfoLabel('ListItem.FilenameAndPath'))

    def _AddToList(self, Label: str, identifier: str):
        """Adds display string and JSON param string to library edit attribute

        Args:
            Label (str): The localized label to display to user
            identifier (str): the JSON parameter for the attribute
        """

        self.modeselect.append(Label)
        self.identifierlist.append(identifier)

    def _edit_db_array(self, preset: str, media_type: str, label: str) -> None:
        """edit an attribute that takes one or more strings using separator

        Args:
            preset (str): current attribute value(s)
            media_type (str): One of defined media types
            label (str): identifier for the attribute to be edited

        Returns:
            None
        """

        keyboard = xbmc.Keyboard(preset)
        keyboard.doModal()
        if keyboard.isConfirmed():
            string_array = json.dumps(keyboard.getText().split(' / '))
            if ((media_type == "Song") or (media_type == "Album") or (media_type == "Artist")):
                xbmc.executeJSONRPC(f'{{"jsonrpc": "2.0", "id": 1, '
                                    f'"method": "AudioLibrary.Set{media_type}Details",'
                                    f'"params": {{ "{label}": {string_array},'
                                    f'"{media_type.lower()}id":{self.DBID} }}}}')
            else:
                xbmc.executeJSONRPC(f'{{"jsonrpc": "2.0", "id": 1, '
                                    f'"method": "VideoLibrary.Set{media_type}Details", '
                                    f'"params": {{ "{label}": {string_array}, '
                                    f'"{media_type.lower()}id":{self.DBID} }}}}')
        else:
            return None

    def _edit_db_integer(self, media_type: str, label: str):
        """edit an attribute that takes an integer value
        Args:
            media_type (str): One of defined media types
            label (str): identifier for the attribute to be edited
        """

        InputLabel = xbmcgui.Dialog().numeric(0, xbmc.getLocalizedString(16028))
        if ((media_type == "Song") or (media_type == "Album") or (media_type == "Artist")):
            xbmc.executeJSONRPC(f'{{"jsonrpc": "2.0", "id": 1,'
                                f'"method": "AudioLibrary.Set{media_type}Details", '
                                f'"params": {{ "{label}": {InputLabel}, '
                                f'"{media_type.lower()}id":{self.DBID} }}}}')
        else:
            xbmc.executeJSONRPC(f'{{"jsonrpc": "2.0", "id": 1, '
                                f'"method": "VideoLibrary.Set{media_type}Details", '
                                f'"params": {{ "{label}": {InputLabel}, '
                                f'"{media_type.lower()}id":{self.DBID} }}}}')

    def _edit_db_string(self, preset: str, media_type: str, label: str):
        """edit an attribute that takes a string value

        Args:
            preset (str): current attribute value
            media_type (str): One of defined media types
            label (str): identifier for the attribute to be edited

        Returns:
            None
        """

        keyboard = xbmc.Keyboard(preset)
        keyboard.doModal()
        if keyboard.isConfirmed():
            try:
                InputLabel = keyboard.getText()
                try:
                    InputLabel = parser.parse(InputLabel).isoformat()
                except parser.ParserError:
                    pass
              #  InputLabel = Time.strftime('%Y-%m-%d')
            except Exception:
                pass
            if ((media_type == "Song") or (media_type == "Album") or (media_type == "Artist")):
                xbmc.executeJSONRPC(f'{{"jsonrpc": "2.0", "id": 1, '
                                    f'"method": "AudioLibrary.Set{media_type}Details", '
                                    f'"params": {{ "{label}": "{InputLabel}", '
                                    f'"{media_type.lower()}id":{self.DBID} }}}}')
            else:
                xbmc.executeJSONRPC(f'{{"jsonrpc": "2.0", "id": 1, '
                                    f'"method": "VideoLibrary.Set{media_type}Details", '
                                    f'"params": {{ "{label}": "{InputLabel}", '
                                    f'"{media_type.lower()}id":{self.DBID} }}}}')
        else:
            return None
