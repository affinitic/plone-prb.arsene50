# -*- coding: utf-8 -*-
from plone import api


def testSetup(context):
    if context.readDataFile('prb.arsene50.txt') is None:
        return

    portal = api.portal.get()
    doc = add_doc(portal, 'fr')
    doc_nl = add_doc(portal, 'nl')
    doc_nl.addTranslationReference(doc)

    doc_en = add_doc(portal, 'en')
    doc_en.addTranslationReference(doc)


def add_doc(portal, lang):
    doc = api.content.create(
        container=portal,
        type="Document",
        title="Arsene50",
        language=lang
    )
    doc.setLayout('arsene50_view')
    #api.content.transition(obj=doc, transition='publish')
    return doc
