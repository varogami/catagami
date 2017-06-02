#!/usr/bin/python2

class Catalog():
    def __init__(self):
        self.name = "generic catalog"
        self.disks = []
        self.tags = []
        
class Disk():
    def __init__(self, name):
        self.name = name
        self.dirs = []
        self.files = []

class Dir():
    def __init__(self, name):
        self.name = name
        self.dirs = []
        self.files = []
        
class File():
    def __init__(self, name):
        self.name = name
        self.sizeh = ""

class Tag():
    def __init__(self, op1, op2):
        self.tag1 = op1
        self.tag2 = op2
