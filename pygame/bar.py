#!/usr/bin/env python

import sys, pygame, time, random
from bunch import Bunch

if not pygame.font: print 'Warning, fonts disabled'

pygame.init()


# global event mask (whitelist)
allowed_events = [	pygame.QUIT,
					pygame.KEYDOWN,
					pygame.MOUSEBUTTONDOWN,
				]

pygame.event.set_allowed(None)
pygame.event.set_allowed(allowed_events)


# color constants
color = Bunch(	black=(0, 0, 0),
				red=(255, 0, 0),
				purple=(255, 0, 255),
				green=(0, 255, 0),
				blue=(0, 0, 255),
				white=(255, 255, 255),
			)


def target_circle (screen, pos, color=color.purple, level=3):
	"""
	draws concentric rings originating from the specified position
	used as visual feedback to indicate exactly where mouse clicks occur
	"""
	width = 0
	for i in range(level+1):
		if i == 0:
			radius = 3
			width = 0
		else:
			radius = i*10
			width = 3
		rect = pygame.draw.circle(screen, color, pos, radius, width)
		pygame.display.update(rect)
		time.sleep(0.03)


def load_image(name, colorkey=None):
	"""
	load an image from disk
	returns surface, rect
	performs native format conversion
	colorkey is the transparency color
	setting colorkey=-1 causes the top-leftmost color to be used
	"""
	try:
		image = pygame.image.load(name)
	except pygame.error, message:
		print 'Cannot load image:', name
		raise SystemExit, message

	image = image.convert()

	# colorkey is the transparency color
	if colorkey is not None:
		if colorkey is -1:
			colorkey = image.get_at((0,0))
	image.set_colorkey(colorkey, pygame.RLEACCEL)
	return image, image.get_rect()


if __name__ == "__main__":
	# window manager flags
	flags = pygame.NOFRAME
	#flags |= pygame.FULLSCREEN

	size = width, height = 1024, 768
	screen = pygame.display.set_mode(size, flags)
	screen.fill(color.white)

	# hide mouse pointer by default
	cursor_visible = False
	pygame.mouse.set_visible(cursor_visible)

	# persisted display artifacts (across screen refreshes)
	# list containing Bunches with image, rect properties
	persist = []

	# load table images
	tables = []
	for i in range(1, 5):
		fname = "%d.png" % i
		(s, r) = load_image(fname, colorkey=-1)
		tables += [ Bunch(image=s, rect=r, label="template:seats%d" % (i*2)) ]
	
	# buttons
	for b in ['move', 'merge', 'rotate', 'delete']:
		(s, r) = load_image("%s.png" % b, colorkey=-1)
		tables += [ Bunch(image=s, rect=r, label="button:%s" % b) ]

	persist.extend(tables)

	# maintain 25-pixel border
	border=Bunch(top=25, bottom=height-25, left=25, right=width-25)

	# initial image placement
	last = None
	for t in tables:
		if last is None:
			t.rect = t.rect.move([border.right-t.rect.right, border.top])
		else:
			t.rect = t.rect.move([border.right-t.rect.right, last.bottom+2])
			
		screen.blit(t.image, t.rect)
		last = t.rect

	# title text
	font = pygame.font.Font(None, 36)
	text = font.render("FOOBAR", 1, color.black)
	rect = text.get_rect(centerx=screen.get_width()/2)
	persist.append(Bunch(image=text, rect=rect, label="title"))
	screen.blit(text, rect)

	# update the whole screen for the initial layout
	pygame.display.flip()

	# ui state
	current_selection = None
	selection_mode = None

	while 1:
		# main loop
		redraw = []

		# event handler dispatch
		event = pygame.event.wait()

		print("%s" % event)
		
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			# keystrokes
			if event.unicode.lower() == 'c':
				# toggle mouse pointer
				cursor_visible = not cursor_visible
				pygame.mouse.set_visible(cursor_visible)
			elif event.unicode.lower() == 'f':
				# toggle fullscreen
				pygame.display.toggle_fullscreen()
			elif event.unicode.lower() == 'q':
				# quit
				sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			# mouse clicks
			if event.button == 1:
				target_circle(screen, event.pos)

				def find_collision ():
					for p in persist:
						if p.rect.collidepoint(event.pos):
							return(p)
					return(None)

				p = find_collision()
				if p is not None:
					# widget selection
					if p.label.startswith('template:'):
						print("Template selected: %s" % p.label)
						selection_mode = 'template'
						current_selection = p
					elif p.label.startswith('button:'):
						# button selected
						cmd = p.label.split(':')[1]
						print("Button selected: %s" % cmd)
						current_selection = None
						selection_mode = cmd
					elif p.label.startswith('instance:') and selection_mode in ['delete', 'move', 'merge', 'rotate']:
						# table instance selected for move or merge
						print("Selected for %s: %s" % (selection_mode, p.label))
						if selection_mode == 'merge':
							if current_selection not in [ None, p ]:
								# current_selection is the merge source
								# p is the merge target
								curr_seats = int(current_selection.label[-1])
								p_seats = int(p.label[-1])
								new_seats = curr_seats + p_seats
								if new_seats > 8:
									new_seats = 8
								if new_seats != p_seats:
									# create new instance with larger seating size
									new_p_label = "seats%d" % new_seats
									for t in tables:
										# find template to copy
										if t.label == "template:%s" % new_p_label:
											new_p = Bunch(image=t.image, rect=t.rect.copy(), label="instance:%s" % new_p_label)
											new_p.rect.center=(p.rect.center)
											persist.remove(p)
											persist.append(new_p)
											p = new_p
											break
								persist.remove(current_selection)
						elif selection_mode == 'delete':
							persist.remove(p)
							p = None
						elif selection_mode == 'rotate':
							# rotate 45 degrees
							if 'rotation' in p:
								rotation = p.rotation
							else:
								p.orig_image = p.image
								rotation = 0

							p.rotation = (rotation + 45) % 360
							p.image = pygame.transform.rotate(p.orig_image, p.rotation)
							p.image.convert()
							rect = p.rect
							p.rect = p.image.get_rect()
							p.rect.center = rect.center
							p = None

						current_selection = p
					else:
						print("Collision detected for: %s" % p.label)
				else:
					# empty space selected
					if current_selection is not None:
						if selection_mode == 'template':
							# new instance
							p = current_selection
							instance = Bunch(image=p.image, rect=p.rect.copy(), label="instance:%s" % (p.label.split(':')[1]))
							instance.rect.center=(event.pos)
							persist.append(instance)
						elif selection_mode == 'move':
							# move selected instance to new location
							current_selection.rect.center=(event.pos)
							current_selection = None

		# redraw
		screen.fill(color.white)
		for p in persist:
			screen.blit(p.image, p.rect)
		pygame.display.flip()


### bugged snap code
#		for p in persist:
#			# snap to grid
#			left_test = p.rect.left % 10
#			if left_test:
#				if left_test < 5:
#					# integer maths
#					new_left = p.rect.left / 10 * 10
#					if new_left < border.left:
#						new_left = border.left
#				else:
#					new_left = (p.rect.left / 10 + 1) * 10
#			p.rect.left = new_left
#
#			top_test = p.rect.top % 10
#			if top_test:
#				if top_test < 5:
#					new_top = p.rect.top / 10 * 10
#					if new_top < border.top:
#						new_top = border.top
#				else:
#					new_top = (p.rect.top / 10 + 1) * 10
#			p.rect.top = new_top



# old table dancing sample code
#	m = 20
#		for t in tables[1:]:
#			if t.rect.left < 0:
#				t.rect.left = 0
#				if m < 0:
#					m = -m
#			elif t.rect.right > width:
#				if m > 0:
#					m = -m
#			t.rect = t.rect.move([m, 0])
#
