#!/usr/bin/python2

import gzip, xml.dom.pulldom, xml.dom.minidom
import catalog, utils


class Import():
    'class for import CdCat data - much code from http://gnomecatalog.org'

    def __init__(self, cdcat_file):
        self.__user="user cdcat"
        self.cat = catalog.Catalog()
        self.__load(cdcat_file)
        
    def __load(self, filename):
        try: 
            print "load CdCat file: " + filename
            cdcatfile=gzip.open(filename, 'r')
            self.dom = xml.dom.pulldom.parse(cdcatfile)
            self.__import(self.dom)
            print "loading CdCat file completed"
        except IOError, (ErrorNumber, ErrorMessage):
            if ErrorNumber == 2: # file not found
                print "file not found"
            else:
                print "error #%d" % ErrorNumber
                print ErrorMessage

    def __import(self, node, lastDisk=None, lastDir=None ):
        while node:
            node = self.dom.getEvent()
            if not node: return
            
            if node[0] == 'START_ELEMENT':
                if node[1].nodeType == 1:

                    if node[1].tagName == 'catalog':
                        self.cat.name = node[1].attributes['name'].value
                     
                    elif node[1].tagName == 'media':
                        newDisk = self.__setDisk(node)
                        self.__import(node, newDisk)
                        
                    elif node[1].tagName == 'directory':
                        newDir = self.__setDir(node)
                        if lastDir == None:
                            lastDisk.dirs.append(newDir)
                        else:
                            lastDir.dirs.append(newDir)
                        self.__import(node, lastDisk, newDir)

                    elif node[1].tagName == 'file':
                        newFile = self.__setFile(node)
                        if lastDir == None:
                            lastDisk.files.append(newFile)
                        else:
                            lastDir.files.append(newFile)

            if node[0] == 'END_ELEMENT' and (node[1].tagName == 'media' or node[1].tagName == 'catalog' or node[1].tagName == 'directory'):
                return

    def __setDisk(self, mynode):
        name = self.__encode(mynode[1].attributes['name'].value) 
        tmpDisk = catalog.Disk(name)
        tmpDisk.type = '/media/cdrom'
        self.cat.disks.append(tmpDisk)
        return tmpDisk

    def __setDir(self, mynode):
        name = self.__encode(mynode[1].attributes['name'].value) 
        tmpDir = catalog.Dir(name)
        return tmpDir

    def __setFile(self, mynode):
        name = self.__encode(mynode[1].attributes['name'].value) 
        size = mynode[1].attributes['size'].value
        time = mynode[1].attributes['time'].value
        tFile = catalog.File(name)
        tFile.size = utils.bytesize(size)
        tFile.sizeh = size
        tFile.timec = time
        return tFile

    def __encode(self,mystring):
        return mystring.encode('ascii', 'xmlcharrefreplace')

