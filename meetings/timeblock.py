"""
author:
sources:
description:
"""

class timeblock:

    def __init__(self):
        self.start = None
        self.end = None
        self.type = None
        self.summary = None

    def set(self, first, last, category, desc=None):
        self.start = first
        self.end = last
        self.type = category
        self.summary = desc if desc else None

    def setStart(self, begin):
        self.start = begin

    def setEnd(self, last):
        self.end = last

    def setType(self, category):
        self.type = category

    def setSummary(self, description):
        self.summary = description
