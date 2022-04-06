#!/usr/bin/env python 

import gtk
import gobject

from console import Console
from numpad import Numpad
from core.models import Employee


class Login(object):
	def __init__(self, numpad):
		self.numpad = numpad
		self.uid = None
		self.context_id = numpad.statusbar.get_context_id("login")
		numpad.statusbar.push(self.context_id, "Enter User ID")
		numpad.connect("ding", self.get_value)


	def login_attempt(self, pwd):
		try:
			return Employee.objects.filter(uid=int(self.uid), password=str(pwd)).values('name_display')[0]['name_display']
		except IndexError:
			# failed
			self.uid = None
			return None


	def get_value(self, src, val):
		if self.uid is None:
			self.uid = val
			self.numpad.statusbar.push(self.context_id, "Enter Password")
		else:
			user = self.login_attempt(val)
			if user is not None:
				cons.write(self, "login succeeded: %s" % user)
			else:
				cons.write(self, "login failed")

			self.numpad.statusbar.pop(self.context_id)


if __name__ == "__main__":
	cons = Console()
	gobject.type_register(Numpad)
	gobject.signal_new("ding", Numpad, gobject.SIGNAL_RUN_LAST,
			   gobject.TYPE_NONE, (gobject.TYPE_PYOBJECT,))
	numpad = Numpad()
	login = Login(numpad)
	gtk.main()

