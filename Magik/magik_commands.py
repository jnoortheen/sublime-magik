#!/usr/bin/python
# To format magik code

import sublime, sublime_plugin, re

class PrintDocCommand(sublime_plugin.TextCommand):
    def run(self, edit, **args):
    	self.view.set_syntax_file("Packages/Magik/magik.tmLanguage")
    	# clear the text
    	self.view.erase(edit, sublime.Region(0, self.view.size()))
    	# insert the docstring
        self.view.insert(edit, self.view.size(), args['docstring'])

class PutWriteTraceCommand(sublime_plugin.TextCommand):
	"""puts write("+++ the text at the line +++") like the emacs command f2+t before or after the line"""
	def run(self, edit, **args):
		for region in self.view.sel():
			line = self.view.line(region)
			contnt = self.view.substr(line)
			line_contents = ("\t" * contnt.rstrip().count('\t')) + 'write("+++ ' + contnt.strip().replace('"', "'") + ' +++")'
			if args["after"]:
				# after the current line
				self.view.insert(edit, line.end(), "\n" +  line_contents)
			else:
				self.view.insert(edit, line.begin(), line_contents + "\n")

# class WriteMagikOutputCommand(sublime_plugin.WindowCommand):
# 	"""to write the output to the panel"""
# 	def run(self, edit):
# 		opanel = self.window.get_output_panel("magik_opanel")
# 		self.panel.set_syntax_file("Packages/Magik/magik.tmLanguage")
# 		opanel.set_read_only(True)
# 		opedit = opanel.begin_edit()
# 		opanel.insert(opedit, opanel.size(), "not a magik file")
# 		opanel.show(self.output_view.size())
# 		opanel.end_edit(opedit)
# 		opanel.set_read_only(True)


class FormatMagikCommand(sublime_plugin.TextCommand):
		def run(self, edit):
			# if it called from magik session forget it.
			# print "file name : ", self.view.file_name()
			# if self.view.file_name():
			# 	#"file name is not none"
			# 	if not (self.view.file_name()[-5:].lower() == "magik"):
			# 		self.panel = self.view.window().get_output_panel('magik_opanel')
			# 		self.view.window().run_command('show_panel', { 'panel': 'output.magik_opanel' })
			# 		self.panel.run_command("print_doc", { 'docstring': 'some docstring' })
			# 		return 
			print "format magik called"
			# determine if applying to a selection or applying to the whole document
			if self.view.sel()[0].empty():
				# nothing selected: process the entire file
				region = sublime.Region(0, self.view.size())
				sublime.status_message('Formatting Entire Magik File')
				rawcode = self.view.substr(region)
				# print region
			else:
				# process only selected region
				region = self.view.line(self.view.sel()[0])
				sublime.status_message('Formatting selection only')
				# rawcode = self.view.substr(self.view.sel()[0])
				# select the entire line to process
				rawcode = self.view.substr(region)
				# print region

			# print rawcode
			indent_level = 0
			beautified_code = ""

			for line_content in rawcode.split("\n"):
				linecon = line_content.strip()

				# checking empty lines
				if linecon == "":
					continue

				beautified_code += linecon + '\n'

			# remove leading and trailing white space
			beautified_code = beautified_code.strip()

			# print beautified_code

			# replace the code in Sublime Text
			self.view.replace(edit, region, beautified_code)

			# done

# class TstCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		name = self.view.file_name()
# 		self.view.insert(edit, 0, str(name))
#         sublime.status_message("Copied file path")

# class AutocompleteAll(sublime_plugin.EventListener):
#     def on_query_completions(self, view, prefix, locations):
# 		# """autocomplete suggestions from all opened tabs"""
#         window = sublime.active_window()
#         # get results from each tab
#         results = [v.extract_completions(prefix) for v in window.views() if v.buffer_id() != view.buffer_id()]
#         results = [(item,item) for sublist in results for item in sublist] #flatten
#         results = list(set(results)) # make unique
#         results.sort() # sort
#         return results
