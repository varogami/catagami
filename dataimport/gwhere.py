#!/usr/bin/python2

import gzip
import catalog, utils

class Import():
    'GWhere class, for load ctg files'
    def __init__(self, mycatalog):
        self.__version = "0.2.3"
        self.__doTag = False
        self.__disk_position=0
        self.__dir_position = 0
        self.cat = catalog.Catalog()
        self.parent_item = None
        self.last_item = catalog.Disk("NO NAME")
        self.__load(mycatalog)

    def __load(self, filename):
        try:
            gwfile = gzip.open(filename, 'r')
            count = 0 
            for line in gwfile:
                count += 1
                if count == 1:
                    fileinfo = line.split(":")
                    if fileinfo[0] == "GWhere": #check if is correct file
                        print "correct file Gwhere - version:", fileinfo[1]
                        print "required version:", self.__version
                    else:
                        print "incorrect file" 
                        break
                elif count == 2:
                    name=line.split(":")
                    self.cat.name = name[0] #get name and description of catalog
                    self.cat.desc = name[1]
                #if have tag in line 3 set "Have TAG" 
                elif count == 3: 
                    if line != "//\n":
                        self.__doTag = True
                    else:
                        self.__disk_position = count + 1
                else:
                    if line == "//\n": #when find // set "Have Disk and position"
                        self.__doTag = False
                        self.__disk_position = count + 1
                    else:
                        if self.__doTag: #if True "Have TAG" become to insert TAG else Disk
                            self.cat.tags.append(self.__getTag(line))
                        else:
                            self.__insert_line(count,line)
            gwfile.close()
            print "loading Gwhere file completed"
        except IOError, (ErrorNumber, ErrorMessage):
            if ErrorNumber == 2: # file not found
                print "file not found"
            else:
                print "error #%d" % ErrorNumber
                print ErrorMessage
        
    def __getTag(self, string):
        taginfo = string.split(":")
        return catalog.Tag(taginfo[0],taginfo[1])

    def __insert_line(self, cur_position, string):
        item_name = self.__getName(string)
        if cur_position == self.__disk_position:
            self.parent_item = self.last_item
            self.curDisk = self.__getDisk(string)
            self.last_item = self.curDisk
        if string != "/\n" and string != "\\\n" and string != "//\n" and cur_position != self.__dir_position and cur_position != self.__disk_position:
            if item_name != "." and item_name != "..": #not load "." and ".." file
                self.last_item.files.append(self.__getFile(string))
        if string == "/\n":
            self.__dir_position = cur_position + 1
        if cur_position == self.__dir_position:
            self.parent_item = self.last_item
            curDir = self.__getDir(string)
            self.last_item.dirs.append(curDir)
            self.last_item = curDir
        if string == "\\\n":
            if self.last_item.__class__.__name__ == "Disk":
                self.cat.disks.append(self.curDisk)
            else:
                if self.parent_item is not None:
                    self.last_item = self.parent_item

    def __getName(self, string):
        return string.split(":")[0]
    
    def __getDisk(self, string):
        #name;num;dev;path;type;volume;size;free;date;serial;category;description
        diskinfo= string.split(":")
        tmpDisk = catalog.Disk(diskinfo[0]) #to cdcat: name,num,type(DVD,??),time
        tmpDisk.num = diskinfo[1]
        tmpDisk.time = utils.convertTimeS(diskinfo[8])
        tmpDisk.type = diskinfo[4]
        return tmpDisk
    
    def __getDir(self, string):
        dirinfo = string.split(":") #to cdcat: name,time
        tmpDir = catalog.Dir(dirinfo[0]) #name
        #name;rights;owner;group;inode;size;date_create;date_acc;date_mod;category;description
        tmpDir.timec = utils.convertTimeS(dirinfo[6]) #time in CdCat format #7 8? - convert string to decimal
        return tmpDir

    def __getFile(self, string):
        #same of directory
        fileinfo = string.split(":") #cdcat name size time
        tmpFile = catalog.File(fileinfo[0]) #insert name
        tmpFile.size = fileinfo[5]
        #7 8? - convert string to decimal                                                                                                       
        tmpFile.timec = utils.convertTimeS(fileinfo[6]) 
        return tmpFile
