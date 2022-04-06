#!/usr/bin/env python 

import pygtk
import gtk
import gobject
pygtk.require("2.0") 


class Numpad (gobject.GObject):
	def __init__(self, style="int"):
		"""
		style='price' standardizes on %0.2f
		"""
		gobject.GObject.__init__(self)
		builder = gtk.Builder()
		builder.add_from_file("glade/numpad.glade")
		builder.connect_signals(self)
		self.style = style
		self.buffer = '0'
		self.numpad = builder.get_object("numpad")
		self.entry1 = builder.get_object("entry1")
		self.statusbar = builder.get_object("statusbar1")
		if self.style == 'price':
			self.entry1.set_text('0.00')
		else:
			self.entry1.set_text('0')
		self.numpad.show()
	
	def button_clicked(self, btn):
		"""
		generic handler for all buttons' clicked signals
		"""
		label = btn.get_label()
		print("button clicked: %s" % label)
		if label == 'gtk-clear':
			self.buffer = '0'
		elif label == 'gtk-go-back':
			self.buffer = self.buffer[:-1]
			if self.buffer == '':
				self.buffer = '0'
		elif label == 'gtk-ok':
			self.emit("ding", int(self.buffer))
		elif label.startswith('gtk-'):
			# ok, cancel
			pass
		elif label == '.':
			# deprecated, '.' removed from ui, but here it is
			if '.' in self.buffer:
				# already there
				pass
			else:
				if self.style == 'price':
					# %0.2f assumed
					pass
				else:
					self.buffer += '.'
		else:
			self.buffer = "%s%s" % (self.buffer, label)

		self.entry1.set_text("%s" % str(self))
	
	def __str__(self):
		if self.style == 'price':
			display = float(self.buffer)/100
			return("%0.2f" % display)
		else:
			if '.' in self.buffer:
				display = float(self.buffer)
			else:
				display = int(self.buffer)
			return("%s" % display)

	def on_numpad_destroy(self,widget,data=None):
		gtk.main_quit()

if __name__ == "__main__":
	app = Numpad(style='price')
	gtk.main()

