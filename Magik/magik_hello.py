
class TstCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		name = self.view.file_name()
		self.view.insert(edit, 0, str(name))
        sublime.status_message("Copied file path")

# from xml.etree import ElementTree as ET
# from urllib import urlopen

# GOOGLE_AC = r"http://google.com/complete/search?output=toolbar&q=%s"

# class GoogleAutocomplete(sublime_plugin.EventListener):
#     def on_query_completions(self, view, prefix, locations):
#         elements = ET.parse(
#                         urlopen(GOOGLE_AC % prefix)
#                     ).getroot().findall("./CompleteSuggestion/suggestion")

#         sugs = [(x.attrib["data"],) * 2 for x in elements]

#         return sugs