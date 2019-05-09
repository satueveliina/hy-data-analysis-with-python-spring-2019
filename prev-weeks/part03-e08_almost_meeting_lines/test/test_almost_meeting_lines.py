#!/usr/bin/python3

import unittest
from unittest.mock import patch

#from numpy.linalg.linalg import LinAlgError
import numpy as np


from tmc import points

from tmc.utils import load, get_out, patch_name
module_name='src.almost_meeting_lines'
almost_meeting_lines = load(module_name, 'almost_meeting_lines')

@points('p03-08.1')
class AlmostMeetingLines(unittest.TestCase):


    def test_first(self):
        a1=1
        b1=4
        a2=3
        b2=2
        p=(a1,b1,a2,b2)
        system="(a1=%i, b1=%i, a2=%i, b2=%i)" % p
        (y,x), exact = almost_meeting_lines(*p)
        self.assertEqual(exact, True, msg="Expected exact solution for system %s!" % system)
        self.assertAlmostEqual(y, a1*x + b1,
                               msg="Solution %f does not satisfy the first equation of system %s!"%(y,system))
        self.assertAlmostEqual(y, a2*x + b2,
                               msg="Solution %f does not satisfy the second equation of system %s!"%(y,system))

    def test_calls(self):
        with patch(patch_name(module_name, "np.linalg.lstsq"), side_effect=np.linalg.lstsq) as psolve:
            a1=1
            b1=4
            a2=3
            b2=2
            almost_meeting_lines(a1,b1,a2,b2)
            psolve.assert_called()

    def test_underdetermined(self):
        a1=1
        b1=4
        p=(a1,b1,a1,b1)
        system="(a1=%i, b1=%i, a2=%i, b2=%i)" % p
        (y,x), exact = almost_meeting_lines(*p)
        self.assertEqual(exact, False,
                         msg="Did not expect exact solution for underdetermined system %s!" % system)

    def test_inconsistent(self):
        a1=1
        b1=4
        p=(a1,b1,a1,b1+1)
        system="(a1=%i, b1=%i, a2=%i, b2=%i)" % p
        (y,x), exact = almost_meeting_lines(*p)
        self.assertEqual(exact, False, msg="Did not expect exact solution for inconsistent system %s!" % system)

if __name__ == '__main__':
    unittest.main()

