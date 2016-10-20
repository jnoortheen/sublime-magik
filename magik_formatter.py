import sublime, sublime_plugin, re

# creating sets
UNARY_OPS = [
    ">>", "_abstract", "_allresults", "_constant", "_dynamic", "_gather", "_gather", "_global", "_import", "_iter",
    "_local", "_not", "_optional", "_private", "_recursive", "_return", "~"
]
BINARY_OPS = [
    # "*",
    # "**", "*<<",
    # "+", "+<<", "+^<<",
    # "-", "-<<", "-^<<",
    # "/", "/<<", "/^<<",
    # "<<", "<=", "<>", "^<<",
    # "=",
    # ">", ">=",
    "_andif", "_cf", "_div", "_isnt", "_mod", "_orif", "_xor", "~="
]
# UNARY_OPS = re.compile(
#     "(\s+)?((>>)|(_return)|(_not)|(~)|(_private)|(_iter)|(,)|(_abstract)|(_optional)|(_gather)|(_allresults)|(_gather)|(_recursive)|(_constant)|(_local)|(_dynamic)|(_global)|(_import))(\s+)?")
# BINARY_OPS = re.compile(
#     "((\*\*)|(\*)|(\/)|(_div)|(_mod)|(\+)|(\-)|(<)|(<=)|(>)|(>=)|(_cf)|(=)|(~=)|(<>)|(_is)|(_isnt)|(_and)|(_andif)|(_xor)|(_or)|(_orif)|(<<)|(^<<)|(\+<<)|(-<<)|(/<<)|(\*<<)|(\+^<<)|(-^<<)|(/^<<)|(\*^<<))(\s+)?")

BLOCK_STARTERS = {"_block", "_catch", "_if", "_lock", "_loop", "_method", "_proc", "_protect", "_try"}
BLOCK_ENDERS = {"_endmethod", "_endloop", "_endif", "_endblock", "_endcatch", "_endblock", "_endproc",
                "_endtry", "_endprotect"}
BLOCK_ELSES = {"_else", "_when", "_then", "_finally", "_protection", "_using", "_elif"}
KEYSPATTERN = re.compile("(_[a-z]+)")


class FormatMagikCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        if self.view.file_name():
            # if it called from magik session forget it.
            # "file name is not none"
            if not (self.view.file_name()[-5:].lower() == "magik"):
                self.panel = self.view.window().get_output_panel('magik_opanel')
                self.view.window().run_command('show_panel', {'panel': 'output.magik_opanel'})
                self.panel.run_command("print_doc", {'docstring': 'some docstring'})
                return

        # variables to help formatting
        block_level = 0
        beautified_code = ""
        indent = None
        location = self.view.sel()

        # determine if applying to a selection or applying to the whole document
        if self.view.sel()[0].empty():
            # nothing selected: process the entire file
            region = sublime.Region(0, self.view.size())
            sublime.status_message('Formatting Entire Magik File')
            rawcode = self.view.substr(region)
        else:
            # process only selected region's most recent block
            region = self.view.line(self.view.sel()[0])
            sublime.status_message('Formatting selection only')
            rawcode = self.view.substr(region)
            block_level = rawcode.split("\n")[0].count('\t')
            indent = '\t' * block_level

        line_cons = rawcode.split("\n")
        for line_content in line_cons:
            linecon = line_content.strip()  # type: str

            if len(linecon) == 0:
                # checking empty lines
                pass
                # continue
            elif linecon.startswith("#%"):
                # checking for encode type
                pass
            elif linecon.startswith("##"):
                # checking for docstring
                pass
            elif linecon.startswith("#"):
                # checking for comments
                if linecon.split()[0] != "#":
                    linecon = linecon.replace("#", "# ", 1)
            else:
                # checking for block method start/end
                keyWords = set(key for key in KEYSPATTERN.findall(linecon))
                if len(keyWords) > 0:
                    if len(keyWords.intersection(BLOCK_STARTERS)) > 0 or linecon.endswith('<<'):
                        indent = '\t' * block_level
                        block_level += 1
                    if len(keyWords.intersection(BLOCK_ENDERS)) > 0:
                        block_level -= 1
                    if len(keyWords.intersection(BLOCK_ELSES)) > 0:
                        indent = '\t' * (block_level - 1)
                for unop in UNARY_OPS:
                    if unop in linecon:
                        linecon = re.sub(("(" + re.escape(unop) + ")(\s+)?"), (unop + " "), linecon)
                for biop in BINARY_OPS:
                    if biop in linecon:
                        linecon = re.sub(("(\s+)?(" + re.escape(biop) + ")(\s+)"), (" " + biop + " "), linecon)
                for op in [',']:
                    if op in linecon:
                        linecon = ", ".join(i.strip() for i in linecon.split(','))

            if indent is None:
                indent = '\t' * block_level
            beautified_code += indent + linecon + '\n'
            indent = None

        # remove leading and trailing white space
        beautified_code = beautified_code.rstrip()

        # replace the code in Sublime Text
        self.view.replace(edit, region, beautified_code)
        # self.view.sel().clear()
        # self.view.sel().add(sublime.Region(location))
