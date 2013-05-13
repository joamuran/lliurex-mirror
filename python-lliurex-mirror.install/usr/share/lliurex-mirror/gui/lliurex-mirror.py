#!/usr/bin/env python

import sys
import os
import signal
from gi.repository import Gtk, Gdk,GObject
from subprocess import call
import subprocess
import time
import threading

# Some values
signal.signal(signal.SIGINT, signal.SIG_DFL)

class LliurexMirror:

	def close_window(self,widget):

		Gtk.main_quit()
		sys.exit(0)

	#def close_window

	def update_mirror_thread(self,widget,pbar):
		
		print("[LliureX Mirror] Update Mirror ")
		pipe=subprocess.Popen(["/usr/share/n4d/binary-plugins/lliurex_mirror_non_gtk","n4dupdate"],stdout=subprocess.PIPE)
		text=pipe.stdout.readline()

		while len(text)>0:
			print text.strip("\n")
			time.sleep(0.5)
			try:
				tmp=text.split(":")[1]
				tmp=tmp.replace(" ","")
				tmp=tmp.split("%")[0]
				tmp=int(tmp)*0.01
				Gdk.threads_init()
				pbar.set_fraction(tmp)
				Gdk.threads_leave()
			except Exception as e:
				pass
			
			text=pipe.stdout.readline()
		

		Gdk.threads_init()
		widget.set_sensitive(True)
		Gdk.threads_leave()
		
		print ("[LliureX Mirror] * ")
		
		# Now update the text Area info
		
		
	#def update_mirror_thread

	def check_thread(self,widget,thread):

		print thread

		if not thread.is_alive():
			
			widget.set_sensitive(True)
			
			
		return thread.is_alive()

	#def check_thread

	def update_mirror(self,widget,thread,pbar):

		#GObject.timeout_add_seconds(1,self.check_thread,widget,thread)
		
		if not thread.is_alive():
			widget.set_sensitive(False)
			pbar.set_fraction(0)
			thread=threading.Thread(target=self.update_mirror_thread,args=(widget,pbar,))
			thread.start()
			
		else:
			print 1
		
	#def update_mirror

	def load_abstract(self,widget):
		
		print("[LliureX Mirror] Load Abstract ")
		if os.path.exists("/var/log/lliurex/lliurex-mirror.log"):
			abstract = open('/var/log/lliurex/lliurex-mirror.log', 'r').read()
		else:
			abstract = ""
		#Reset the buffer
		buffer = Gtk.TextBuffer()
		widget.set_buffer(buffer)
		buffer.set_text(abstract)
		widget.set_buffer(buffer)
		
		
	#def load_abstract(widget):

	def save_mirror(self,widget):

		print("[LliureX Mirror] Save Mirror")

	#def save_mirror(widget):

if __name__== "__main__":

	lliurexMirror=LliurexMirror()
	builder = Gtk.Builder()
	
	builder.add_from_file("/usr/share/lliurex-mirror/gui/lliurex-mirror-gui.glade")
	window=builder.get_object("windowLliureXMirror")
	window.connect("destroy",lliurexMirror.close_window)

	#progress bar
	pbar=builder.get_object("progressbar")
	
	
	# Button Update
	button=builder.get_object("buttonUpdate")
	thread=threading.Thread(target=lliurexMirror.update_mirror_thread)
	button.connect("clicked",lliurexMirror.update_mirror,thread,pbar)
	
	# Abstract
	textviewAbstract = builder.get_object("textviewAbstract")
	lliurexMirror.load_abstract(textviewAbstract)
	
	window.show_all()

	GObject.threads_init()
	Gtk.main()
	GObject.threads_leave()
	



