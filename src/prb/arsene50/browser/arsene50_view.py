# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from plone import api
from plone.memoize import forever
import json
import urllib2
import requests
from prb.arsene50 import _
from datetime import date
import logging
log = logging.getLogger("prb.arsene50")

EVENT_API = "https://api.brussels:443/api/agenda/0.0.1/events/"


class Arsene50View(BrowserView):

    def get_today(self):
        today = date.today()
        return "{}/{}/{}".format(
                today.day,
                today.month,
                today.year,
                )

    def get_places(self):
        lang = self.context.Language()
        if not lang or lang == "en":
            lang = "fr"
        events = []
        url_current = api.portal.get_registry_record(
                'prb.arsene50.currentoffer')
        jdict_current = get_json_from_url(url_current)
        events += [transform_jdict(jdict, lang) for jdict in jdict_current]
        places = find_places(events, lang)
        places = sorted(places, key=lambda x: x.name)
        return places


@forever.memoize
def get_place(agenda_id, lang, api_headers):
    url = EVENT_API + str(agenda_id)
    response = requests.get(url, headers=api_headers, verify=False)
    if response.status_code != 200:
        return None
    json = response.json
    place = json.get("event").get("place")
    return place


def find_places(events, lang):
    places = {}
    token = api.portal.get_registry_record('prb.arsene50.agenda_api_token')
    api_headers = {
        "Accept": "application/json",
        "Authorization": "Bearer %s" % token
    }
    for e in events:
        agenda_id = e.get("agenda_id")
        place = get_place(agenda_id, "fr", api_headers)
        if place is None:
            continue
        place_id = place.get("id")
        if place_id in places:
            places[place_id].events.append(e)
        else:
            infos = place.get("translations").get(lang)
            address = u"{} - {}".format(infos.get("address_line1"), infos.get("address_line2"))
            places[place_id] = ArsenePlace(
                id=place_id,
                name=infos.get("name"),
                address=address,
                tel=infos.get("phone_contact"),
                mail=infos.get("email"),
                website=infos.get("website"),
                events=[e])
    return places.values()


def get_json_from_url(url):
    log.info('Take data from {}'.format(url))
    try:
        data = urllib2.urlopen(url)
    except urllib2.URLError, e:
        log.error(_(u'Can\'t call url from www.arsene50.be'))
        return {}
    try:
        jdict = json.load(data)
    except ValueError, e:
        log.error(_(u'Json value error from www.arsene50.be'))
        return {}
    except SyntaxError, e:
        log.error(_(u'Json bad formatted from www.arsene50.be'))
        return {}
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
        return self.get('name')

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
        addr = u"{} {} {}".format(street, zipcode, city)
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


class ArsenePlace(object):
    id = None
    name = None
    address = None
    tel = None
    mail = None
    website = None
    events = []

    def __init__(self, id, name, address, tel, mail, website, events):
        self.id = id
        self.name = name
        self.address = address
        self.tel = tel
        self.mail = mail
        self.website = website
        self.events = events
