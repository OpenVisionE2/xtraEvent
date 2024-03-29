# -*- coding: utf-8 -*-
# by digiteng...08.2020 - 11.2021
# <widget source="session.Event_Now" render="xtraPoster" position="0,0" size="185,278" zPosition="1" />
from __future__ import absolute_import
from Components.Renderer.Renderer import Renderer
from enigma import ePixmap, loadJPG
from Components.config import config
from Components.Console import Console
import re
from os import walk
from os.path import getsize, join, exists

try:
	pathLoc = config.plugins.xtraEvent.loc.value
except:
	pathLoc = ""

try:
	pathlocation = config.plugins.xtraEvent.loc.value
	posterpath = "{}xtraEvent/poster".format(pathlocation)
	maximumfoldersize = config.plugins.xtraEvent.rmposter.value
	folder_size = sum([sum(map(lambda fname: getsize(join(posterpath, fname)), files)) for posterpath, folders, files in walk(posterpath)])
	posters_size = "%0.f GB" % (folder_size / (1024 * 1024.0) / 1000)
	print("[xtraEvent] posters_size = %s" % posters_size)
	deleteposter = "rm -f %s/*" % posterpath
	if posters_size == maximumfoldersize:
		Console().ePopen(deleteposter)
	else:
		print("[xtraEvent] Size of the posters is %s, not equal to %s, your chosen size." % (posters_size, maximumfoldersize))
except:
	pass

REGEX = re.compile(
		r'([\(\[]).*?([\)\]])|'
		r'(: odc.\d+)|'
		r'(\d+: odc.\d+)|'
		r'(\d+ odc.\d+)|(:)|'

		r'!|'
		r'/.*|'
		r'\|\s[0-9]+\+|'
		r'[0-9]+\+|'
		r'\s\d{4}\Z|'
		r'([\(\[\|].*?[\)\]\|])|'
		r'(\"|\"\.|\"\,|\.)\s.+|'
		r'\"|:|'
		r'\*|'
		r'Премьера\.\s|'
		r'(х|Х|м|М|т|Т|д|Д)/ф\s|'
		r'(х|Х|м|М|т|Т|д|Д)/с\s|'
		r'\s(с|С)(езон|ерия|-н|-я)\s.+|'
		r'\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\.\s\d{1,3}\s(ч|ч\.|с\.|с)\s.+|'
		r'\s(ч|ч\.|с\.|с)\s\d{1,3}.+|'
		r'\d{1,3}(-я|-й|\sс-н).+|', re.DOTALL)


class xtraPoster(Renderer):

	def __init__(self):
		Renderer.__init__(self)

	GUI_WIDGET = ePixmap

	def changed(self, what):
		if not self.instance:
			return
		else:
			if what[0] != self.CHANGED_CLEAR:
				evnt = ''
				pstrNm = ''
				evntNm = ''
				try:
					event = self.source.event
					if event:
						evnt = event.getEventName()
						evntNm = REGEX.sub('', evnt).strip()
						pstrNm = "{}xtraEvent/poster/{}.jpg".format(pathLoc, evntNm)
						if exists(pstrNm):
							self.instance.setPixmap(loadJPG(pstrNm))
							self.instance.setScale(1)
							self.instance.show()
						else:
							self.instance.hide()
					else:
						self.instance.hide()
					return
				except:
					self.instance.hide()
					return
			else:
				self.instance.hide()
				return
