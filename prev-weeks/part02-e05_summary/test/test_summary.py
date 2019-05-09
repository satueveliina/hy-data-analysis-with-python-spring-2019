#!/usr/bin/env python3

import sys
import math
import unittest
from unittest.mock import patch

from tmc import points

from tmc.utils import load, get_out

module_name="src.summary"
summary = load(module_name, "summary")
main = load(module_name, "main")

def get_path(filename):
    import sys
    import os
    return os.path.join(os.path.dirname(sys.argv[0]), "..", "src", filename)

class Summary(unittest.TestCase):

    @points('p02-05.1')
    def test_one(self):
        s,a,d = summary(get_path("example.txt"))
        self.assertAlmostEqual(s, 51.400000, places=4, msg="Wrong sum for file example.txt!")
        self.assertAlmostEqual(a, 10.280000, places=4, msg="Wrong average for file example.txt!")
        self.assertAlmostEqual(d, 8.904606, places=4, msg="Wrong std for file example.txt!")

    @points('p02-05.1')
    def test_two(self):
        s,a,d = summary(get_path("example2.txt"))
        self.assertAlmostEqual(s, 5446.200000, places=4, msg="Wrong sum for file example2.txt!")
        self.assertAlmostEqual(a, 1815.400000, places=4, msg="Wrong average for file example2.txt!")
        self.assertAlmostEqual(d, 3124.294045, places=4, msg="Wrong std for file example2.txt!")

    @points('p02-05.2')
    def test_three(self):
        s,a,d = summary(get_path("example3.txt"))
        self.assertAlmostEqual(s, 0.000000, places=4, msg="Wrong sum for file example3.txt!")
        self.assertAlmostEqual(a, 0.000000, places=4, msg="Wrong average for file example3.txt!")
        self.assertAlmostEqual(d, 50.000000, places=4, msg="Wrong std for file example3.txt!")

    @points('p02-05.1')
    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            summary("doesnotexist")

    @points('p02-05.1')
    def test_calls(self):
        with patch('builtins.open', side_effect=open) as o:
            with patch('math.sqrt', wraps=math.sqrt) as s:
                summary(get_path("example.txt"))
                o.assert_called()
                s.assert_called()

    @points('p02-05.1')
    def test_main(self):
        orig_argv = sys.argv
        n = 7
        sys.argv[1:] = ["file%i" % i for i in range(n)]
        with patch('src.summary.summary',
                   side_effect=[(0.0,0.0,0.0)]*n) as s:
            main()
            self.assertEqual(s.call_count, n,
                             msg="Expected %i calls to summary for %i command line parameters!" % (n,n))
        result = get_out().split('\n')
        for i, line in enumerate(result):
            self.assertEqual(line.strip(), "File: file%i Sum: 0.000000 Average: 0.000000 Stddev: 0.000000" % i,
                             msg="Wrong result for data consisting of zeros!")
        sys.argv = orig_argv
        
if __name__ == '__main__':
    unittest.main()
    
