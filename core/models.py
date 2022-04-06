#!/usr/bin/env python

from django.db import models

class MenuItem(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=256, unique=True)
	price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
	cost = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

	def __unicode__(self):
		return self.name


class Table(models.Model):
	id = models.AutoField(primary_key=True)

	def __unicode__(self):
		return "Table %s" % self.id


class Employee(models.Model):
	id = models.AutoField(primary_key=True)
	name_first = models.CharField(max_length=256)
	name_last = models.CharField(max_length=256)
	name_display = models.CharField(max_length=256)
	uid = models.IntegerField()
	password = models.CharField(max_length=256)

	def __unicode__(self):
		return self.name_display


class Check(models.Model):
	id = models.AutoField(primary_key=True)
	table = models.ForeignKey(Table)
	server = models.ForeignKey(Employee)

	def __unicode__(self):
		return "%s-%s" % (self.server.name_display, self.table.id)


class CheckItem(models.Model):
	id = models.AutoField(primary_key=True)
	check = models.ForeignKey(Check)
	item = models.ForeignKey(MenuItem)
	charge = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

	def __unicode__(self):
		return "ck%d %s: %0.2f" % (self.check.id, self.item.name, self.charge)

	
class Attendance(models.Model):
	id = models.AutoField(primary_key=True)
	employee = models.ForeignKey(Employee)
	time_in = models.DateTimeField()
	time_out = models.DateTimeField(null=True)

	def __unicode__(self):
		return "%s/%s/%s" % (self.employee.name_display, self.time_in, self.time_out)

