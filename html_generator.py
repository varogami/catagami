#!/usr/bin/python2

import sys, os, json 
from dataimport import gwhere
from dataimport import cdcat

app_name="html_generator.py"
export_tag="export"
dir_sep = "/"

ico_fold="/usr/share/icons/gnome/24x24/places/folder.png"
ico_gen_file="/usr/share/icons/gnome/24x24/mimetypes/empty.png"
ico_gen_drive="/usr/share/icons/gnome/24x24/devices/drive-removable-media.png"

class HtmlSrc():
    def __init__(self):
        self.title = "NO TITLE"
        self.head = ""
        self.head3 = ""
        self.info = ""
        self.items = ""
        self.body = ""
        self.home = "index.html"
        self.up = "index.html"

    def set_head(self, name):
        self.head = """<h1>""" + name + """</h1>""" + "\n"

    def set_head3(self, name):
        self.head = """<h3>""" + name + """</h3>""" + "\n"
        
    def add_item(self, icon, name, isdir=True):
        if isdir is True:
            url = name + dir_sep + "index.html"
        else:
            url = name + ".html"
        self.items = self.items + """<br><br><img src=\"""" + icon + """\">   <a href=\"""" + url + """\">""" + name + """</a>""" + "\n"

    def set_file_info(self, fileob):
        self.info = self.info + """<i>size: """ + str(fileob.size) + """ byte</i><br>""" + "\n"
        self.info = self.info + """<i>size: """ + fileob.sizeh + """</i><br>""" + "\n"
        self.info = self.info + """<i>date: """ + fileob.timec + """</i><br>""" + "\n"

    def set_dir_info(self, direob):
        self.info = self.info + """<i>name: """ + direob.name + """</i><br>""" + "\n"

    def set_disk_info(self, diskob):
        self.info = self.info + """<i>media type: """ + diskob.type + """</i><br>""" + "\n"
        
    def build(self):
        self.src="""<html>
         <head>
          <meta charset="UTF-8">
          <title>""" +self.title+ """</title>
         </head>
         <body>
          <a href=\"""" + self.home  + """\" >Home</a> - <a href=\"""" + self.up  + """\" >Up</a>
          """ + self.head + self.head3 + self.info + self.items + self.body + """</body>
        </html>
        """

class Generate():
    def __init__(self):
        self.html_home = "index.html"
        self.__cli()
        
    def __generate(self, data):
        if data is not None:
            if os.path.exists(self.export_dir):
                print self.export_dir  + " dir - exist!"
            else:
                os.makedirs(self.export_dir)
                home = HtmlSrc()
                home.title = data.cat.name
                home.set_head(data.cat.name)
                for disk in data.cat.disks:
                    disk_dir=self.export_dir + dir_sep + disk.name
                    os.makedirs(disk_dir)
                    home.add_item(ico_gen_drive, disk.name)
                    disk_code = HtmlSrc()
                    disk_code.title = disk.name
                    disk_code.set_head(disk.name)
                    disk_code.set_disk_info(disk)
                    disk_code.up = "../" + self.html_home
                    disk_code.home = "../" + self.html_home
                    for cdir in disk.dirs:
                        disk_code.add_item(ico_fold, cdir.name)
                        self.__generate_dir(cdir, self.export_dir + dir_sep + disk.name, "../" + self.html_home)
                    for cfile in disk.files:
                        disk_code.add_item(ico_gen_file, cfile.name, False)
                        File = HtmlSrc()
                        File.title = cfile.name
                        File.set_head3(cfile.name)
                        File.set_file_info(cfile)
                        File.up = self.html_home
                        File.home = disk_code.home
                        self.__write_html( disk_dir + dir_sep + cfile.name + ".html", File )
                    self.__write_html( disk_dir + dir_sep + "index.html", disk_code)
                self.__write_html(self.export_dir + dir_sep  + "index.html", home)

    def __generate_dir(self, dir_data, parent_dir, home_link):
        if dir_data is not None:
            son_path = parent_dir+dir_sep+dir_data.name
            if not os.path.exists(son_path):
                os.makedirs(son_path)
            Dir = HtmlSrc()
            Dir.title = dir_data.name
            Dir.set_head(dir_data.name)
            Dir.set_dir_info(dir_data)
            Dir.up = "../index.html"
            Dir.home = "../" + home_link
            for sondir in dir_data.dirs:
                Dir.add_item(ico_fold, sondir.name)
                self.__generate_dir(sondir, son_path, "../" + home_link)
            for sonfile in dir_data.files:
                Dir.add_item(ico_gen_file, sonfile.name, False)
                File = HtmlSrc()
                File.title = sonfile.name
                File.set_head3(sonfile.name)
                File.set_file_info(sonfile)
                File.up = self.html_home
                File.home = Dir.home
                self.__write_html( son_path + dir_sep + sonfile.name + ".html", File )
            self.__write_html( son_path + dir_sep + "index.html", Dir )
                
    def __write_html(self, html_file, html):
        html.build()
        print "write export file: " + html_file
        DataFile = open(html_file, "w")
        DataFile.write(html.src)
        DataFile.close()

    def __getdata(self):
        filename, ext = os.path.splitext(self.file)
        if ext == ".hcf":
            self.type = "cdcat"
            data = cdcat.Import(self.file)
        elif ext == ".ctg":
            self.type = "gwhere"
            data = gwhere.Import(self.file)
        else:
            self.type = ""
            print "extension "+ext+" not supported"
            data = None
        self.export_dir = self.type + "-" + self.file.replace("/","_") + "-" + export_tag
        return data
            
    def __cli(self):
        if len(sys.argv) == 1:
            self.help()
        elif len(sys.argv) == 2:
            self.file = sys.argv[1]
            self.__generate(self.__getdata())
        else:
            print "too much parameter"

    def help(self):
        print "use: " + app_name + " \"filename\""
        print "     where filename is cdcat or gwhere type"

    
if __name__ == "__main__" :
    Generate()
