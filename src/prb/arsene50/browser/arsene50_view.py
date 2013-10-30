# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
import json
import urllib2
from prb.arsene50 import _


class Arsene50View(BrowserView):

    def get_events(self):
        lang = self.context.Language()
        events = []
        url_co = api.portal.get_registry_record('prb.arsene50.currentoffer')
        url_no = api.portal.get_registry_record('prb.arsene50.nextoffer')
        jdict_co = get_json_from_url(url_co)
        jdict_no = get_json_from_url(url_no)
        events += [transform_jdict(jdict, lang) for jdict in jdict_co]
        events += [transform_jdict(jdict, lang) for jdict in jdict_no]
        return events


def get_json_from_url(url):
    try:
        data = urllib2.urlopen(url)
    except urllib2.URLError, e:
        error = _(u'Can\'t call url from www.arsene50.be')
        return error + e
    try:
        jdict = json.load(data)
    except ValueError, e:
        error = _(u'Json value error from ww.arsene50.be')
        return error
    except SyntaxError, e:
        error = _(u'Json bad formatted from ww.arsene50.be')
        return error
    return jdict


def transform_jdict(dict_from_json, lang):
    ea = EventArsene(dict_from_json, lang)
    return ea


class EventArsene(dict):
    context_lang = ''

    def __init__(self, jdict, context_lang):
        self.update(jdict)
        self.context_lang = context_lang

    @property
    def name(self):
        return self.get_content('name')

    @property
    def longdesc(self):
        return self.get_content('longdesc')

    def get_content(self, key):
        return self.get("{}_{}".format(key, self.context_lang.lower()))

    def get_place(self):
        return self.get('Place')

    def get_sale_all_day(self):
        return self.get('sale_all_day')

    def get_spectacle_id(self):
        return self.get('spectacle_id')

    def get_categories(self):
        return self.get("categories")
