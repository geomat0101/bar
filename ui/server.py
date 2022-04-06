#!/usr/bin/env python 

import pygtk
import gtk
pygtk.require("2.0") 

from core.models import Check

class Server (object):
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("glade/server.glade")
		builder.connect_signals(self)
		self.window1 = builder.get_object("window1")
		self.open_checks = builder.get_object("liststore1")
		tables = [ "Table %s" % str(x['table']) for x in Check.objects.all().values('table') ]
		print "tables: %s" % tables
		self.open_checks.append(tables)
		self.window1.show()
	

if __name__ == "__main__":
	srv = Server()
	gtk.main()

