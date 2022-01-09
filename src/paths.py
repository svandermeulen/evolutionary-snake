"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 09/01/2022
"""

import os
from dataclasses import dataclass


@dataclass
class Paths:

    path_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path_input = os.path.join(path_home, "input")
    path_output = os.path.join(path_home, "output")
    path_output_temp = os.path.join(path_output, "temp")


def main():
    pass


if __name__ == "__main__":
    main()
