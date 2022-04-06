#!/usr/bin/env python 

import pygtk
import gtk
pygtk.require("2.0") 

class Console (object):
	def __init__(self):
		builder = gtk.Builder()
		builder.add_from_file("glade/console.glade")
		builder.connect_signals(self)
		self.console = builder.get_object("console")
		self.textbuffer1 = builder.get_object("textbuffer1")
		self.console.show()
	
	def write(self, src, msg):
		self.textbuffer1.place_cursor(self.textbuffer1.get_end_iter())
		self.textbuffer1.insert_at_cursor("%s\n" % msg)
		self.textbuffer1.insert_at_cursor("\n")


if __name__ == "__main__":
	cons = Console()
	gtk.main()

