#!/usr/bin/env python3

import unittest
from unittest.mock import patch

from tmc import points

from tmc.utils import load, get_out

module_name="src.multiplication_table"
main = load(module_name, "main")

@points('p01-04.1')
class MultiplicationTable(unittest.TestCase):

    
    def test_lines(self):
        main()
        result = get_out().split("\n")
        self.assertEqual(len(result), 10, msg="The output should contain ten lines!")

    def test_content(self):
        main()
        result = get_out().split("\n")
        for i, line in enumerate(result):
            j = i + 1
            numbers = list(map(int, line.split()))
            self.assertEqual(numbers, list(range(j, 11*j, j)))

    def test_calls(self):
        with patch('builtins.print') as p:
            main()
            self.assertGreaterEqual(len(p.mock_calls), 100, msg="You should have called 'print' exactly 100 times!")
            
if __name__ == '__main__':
    unittest.main()
    
