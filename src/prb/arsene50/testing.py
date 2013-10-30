# -*- coding: utf-8 -*-
from plone.testing import z2
from plone.app.testing import PloneWithPackageLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.app.robotframework.testing import AUTOLOGIN_LIBRARY_FIXTURE

import prb.arsene50


PRB_ARSENE50 = PloneWithPackageLayer(
    zcml_package=prb.arsene50,
    zcml_filename='testing.zcml',
    gs_profile_id='prb.arsene50:testing',
    name='PRB_ARSENE50'
)

PRB_ARSENE50_INTEGRATION = IntegrationTesting(
    bases=(PRB_ARSENE50, ),
    name="PRB_ARSENE50_INTEGRATION"
)

PRB_ARSENE50_FUNCTIONAL = FunctionalTesting(
    bases=(PRB_ARSENE50, ),
    name="PRB_ARSENE50_FUNCTIONAL"
)

PRB_ARSENE50_ROBOT_TESTING = FunctionalTesting(
    bases=(PRB_ARSENE50, AUTOLOGIN_LIBRARY_FIXTURE, z2.ZSERVER_FIXTURE),
    name="PRB_ARSENE50_ROBOT_TESTING")


