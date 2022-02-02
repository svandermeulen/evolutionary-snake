"""
-*- coding: utf-8 -*-
Written by: sme30393
Date: 09/01/2022
"""

import os


class Paths:

    def __init__(self, datetime_run: str):
        self.path_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.path_input = os.path.join(self.path_home, "input")
        self.path_output = os.path.join(self.path_home, "output", datetime_run)
        self.path_neat_config = os.path.join(self.path_input, "neat_config")
        self.path_checkpoint_prefix = os.path.join(self.path_output, "neat-checkpoint-")

        if not os.path.isdir(self.path_output):
            os.makedirs(self.path_output)


def main():
    pass


if __name__ == "__main__":
    main()
