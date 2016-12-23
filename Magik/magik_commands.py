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
            line_contents = ("\t" * contnt.rstrip().count('\t')) + 'write("+++ ' + contnt.strip().replace('"',
                                                                                                          "'") + ' +++")'
            if args["after"]:
                # after the current line
                self.view.insert(edit, line.end(), "\n" + line_contents)
            else:
                self.view.insert(edit, line.begin(), line_contents + "\n")

