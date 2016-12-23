# -*- coding: ascii -*-
# Extends Sublime Text autocompletion to find matches in all open
# files. By default, Sublime only considers words from the current file.

import sublime_plugin
import sublime
import re
import time
from os.path import basename
from .magik_comp_methods import magik_methods
from .magik_comp_snippets import magik_snippets

# limits to prevent bogging down the system
MIN_WORD_SIZE = 3
MAX_WORD_SIZE = 50

magik_completions_set = frozenset(k for sublist in magik_snippets.keys() for k in sublist.split('\t'))
magik_methods_set = frozenset(k for sublist in magik_methods.keys() for k in sublist.split('\t'))


class AllAutocomplete(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.magik"):
            return []
        # Limit number of views but always include the active view. This
        # view goes first to prioritize matches close to cursor position.
        # other_views = [v for v in sublime.active_window().views() if v.id != view.id]
        views = sublime.active_window().views()
        words = calc_cpmletions_time(views, prefix)
        pt = locations[0] - len(prefix) - 1
        ch = view.substr(sublime.Region(pt, pt + 1))  # the character before the trigger
        words_vals = words.values()
        # adding words from completion file.
        matches = [(trig, magik_methods[trig]) for trig in magik_methods if trig.startswith(prefix)] \
            if ch == '.' \
            else [(trig, magik_snippets[trig]) for trig in magik_snippets if trig.startswith(prefix)]

        for w, v in words_vals:
            if w in magik_completions_set or w in magik_methods_set: continue
            trigger = w
            contents = w.replace('$', '\\$')

            if v.file_name() and v.file_name() != view.file_name():
                trigger += '\t(%s)' % basename(v.file_name())
            matches.append((trigger, contents))
        matches.sort()
        return matches

def calc_cpmletions_time(views, prefix):
    words = {}
    for v in views:
        view_words = v.extract_completions(prefix)
        view_words = [w for w in view_words if MIN_WORD_SIZE <= len(w) <= MAX_WORD_SIZE]
        # view_words = fix_truncation(v, view_words)
        for w in view_words:
            words[w] = (w, v)
    return words
