# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
import json
import urllib2
from prb.arsene50 import _
from datetime import date
import logging
log = logging.getLogger("prb.arsene50")


class Arsene50View(BrowserView):

    def get_today(self):
        today = date.today()
        return "{}/{}/{}".format(
                today.day,
                today.month,
                today.year,
                )

    def get_events(self):
        lang = self.context.Language()
        if lang == "en":
            lang = "fr"
        events = []
        url_current = api.portal.get_registry_record(
                'prb.arsene50.currentoffer')
        jdict_current = get_json_from_url(url_current)
        events += [transform_jdict(jdict, lang) for jdict in jdict_current]
        #url_next = api.portal.get_registry_record('prb.arsene50.nextoffer')
        #jdict_next = get_json_from_url(url_next)
        #events += [transform_jdict(jdict, lang) for jdict in jdict_next]
        name = 'name_{}'.format(lang)
        sort_by_place_events = sorted(events,
                key=lambda k: k['Place'][name])
        places = find_places(sort_by_place_events)
        group_list = group_list_by_place(sort_by_place_events)
        return {'places': places, 'list': group_list}


def group_list_by_place(events):
    names = set(map(lambda x: x.place_name, events))
    grouplists = [[y for y in events if y.place_name == x] for x in names]
    return dict(zip(names, grouplists))


def find_places(events):
    places = map(lambda x: {'name': x.place_name,
                            'address': x.place_address,
                            'tel': x.place_tel,
                            'mail': x.place_mail,
                            'website': x.place_website}, events)
    return [dict(t) for t in set([tuple(place.items()) for place in places])]


def get_json_from_url(url):
    log.info('Take data from {}'.format(url))
    try:
        data = urllib2.urlopen(url)
    except urllib2.URLError, e:
        error = _(u'Can\'t call url from www.arsene50.be')
        return error + e
    try:
        jdict = json.load(data)
    except ValueError, e:
        error = _(u'Json value error from www.arsene50.be')
        return error
    except SyntaxError, e:
        error = _(u'Json bad formatted from www.arsene50.be')
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

    def place(self):
        return self.get('Place')

    @property
    def place_name(self):
        return self.place().get('name_{}'.format(self.context_lang))

    @property
    def place_address(self):
        place = self.place()
        street = place.get('street_{}'.format(self.context_lang))
        nr = place.get('house_nr')
        zipcode = place.get('zip')
        city = place.get('city_{}'.format(self.context_lang))
        addr = u"{}, {} <br />{} {}".format(street, nr, zipcode, city)
        return addr

    @property
    def place_mail(self):
        place = self.place()
        return place.get('email_{}'.format(self.context_lang))

    @property
    def place_tel(self):
        place = self.place()
        return place.get('tel')

    @property
    def place_website(self):
        place = self.place()
        return place.get('website_{}'.format(self.context_lang))

    @property
    def sale_all_day(self):
        return self.get('sale_all_day')

    @property
    def spectacle_id(self):
        return self.get('spectacle_id')

    def categories(self):
        cat = self.get("categories")
        if isinstance(cat, list):
            cat = cat[0]
        return cat

    @property
    def normal_price(self):
        cat = self.categories()
        return "{0:.2f}&euro;".format(
                cat.get('normal_price')).replace('.', ',')

    @property
    def arsene_price(self):
        cat = self.categories()
        return "{0:.2f}&euro;".format(
                cat.get('arsene_price')).replace('.', ',')

    @property
    def hour(self):
        cat = self.categories()
        return cat.get('hour')

    @property
    def date(self):
        cat = self.categories()
        date = cat.get('date').split('-')
        format_date = u"{}/{}/{}".format(date[2], date[1], date[0])
        return format_date

    @property
    def available_seats(self):
        cat = self.categories()
        return cat.get('available_seats')

    @property
    def seat_category(self):
        cat = self.categories()
        return cat.get('seat_category')

    @property
    def remark(self):
        cat = self.categories()
        return cat.get('remark_{}'.format(self.context_lang))
