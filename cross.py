"""
	OPTIONS
	"show_cross": true
		show cross.
	"show_multiple_cross":true
		show multiple cross

"""
import math
import sublime
import sublime_plugin
settings_cross = sublime.load_settings('Cross.sublime-settings')
class CrossCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		show_cross = int(bool(settings_cross.get('show_cross')))
		settings_cross.set('show_cross',not show_cross)

def unload_handler():
	for window in sublime.windows():
		for view in window.views():
			view.erase_regions('CrossListener')
class CrossListener(sublime_plugin.EventListener):
	def __init__(self):
		print '---------------------------------- 20130222 cross init'
	def update_cross(self, view):
		settings_index = view.settings()
		viewport = view.viewport_extent()
		if viewport[1]<30:
			settings_index.set('rulers','')
			return
		show_cross = int(bool(settings_cross.get('show_cross')))
		show_multiple_cross = int(bool(settings_cross.get('show_multiple_cross')))
		cross_width = int(settings_cross.get('cross_width'))
		if not show_cross:
			settings_index.set('rulers',[])
			return
		rulers = []
		gap = 0.5/view.em_width()
		start = -math.ceil(cross_width)*gap


		for sel in reversed(view.sel()):
			end_sel = sel.end()
			pos_xy = view.text_to_layout(end_sel)
			pos_x = pos_xy[0]
			pos = int(pos_x/view.em_width())
			rulers.append(pos)
			for i in range(0,cross_width*2):
				rulers.append(pos+start)
				start+=gap
			if not show_multiple_cross:
				break
		settings_index.set('rulers',rulers)
	def on_load(self, view):
		self.update_cross(view)
	def on_activated(self, view):
		self.update_cross(view)
	def on_modified(self, view):
		self.update_cross(view)
	def on_selection_modified(self, view):
		self.update_cross(view)
