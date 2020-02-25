# -*- coding: utf-8 -*-

from plone import api

PROFILE_ID = "profile-prb.arsene50:default"


def reload_registry(context):
    portal_setup = api.portal.get_tool("portal_setup")
    portal_setup.runImportStepFromProfile(PROFILE_ID, "plone.app.registry")
