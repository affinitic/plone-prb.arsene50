# -*- coding: utf-8 -*-
from plone.testing import layered
import unittest
import robotsuite

from prb.arsene50.testing import PRB_ARSENE50_ROBOT_TESTING


def test_suite():
    suite = unittest.TestSuite()
    robots_file = [
        'example.robot',
    ]

    for robot_file in robots_file:
        rts = robotsuite.RobotTestSuite(robot_file)
        suite.addTests([
            layered(rts,  layer=PRB_ARSENE50_ROBOT_TESTING)
        ])
    return suite
