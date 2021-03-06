#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from tmc import points

from tmc.utils import load, get_out

module_name="src.compliment"
main = load(module_name, "main")

@points('p01-02.1')
class Compliment(unittest.TestCase):

    
    def test_first(self):
        with patch('builtins.input', side_effect=['France']) as prompt:
            main()
            output = get_out()
            self.assertEqual("I have heard that France is a beautiful country.", output)
            prompt.assert_called_once_with("What country are you from? ")

if __name__ == '__main__':
    unittest.main()
    
