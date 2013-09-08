# -*- coding: utf-8 -*-

import re, os
import sublime, sublime_plugin

PACKAGE_NAME = 'HeadTemplate'
PACKAGES_PATH = sublime.packages_path()


def get_syntax_name(s):
    r = r'Packages/.*/(.*).tmLanguage'
    match = re.match(r, s)
    if match:
        return match.group(1)


def get_syntax_vars(view):
    s = sublime.load_settings('HeadTemplate.sublime-settings')
    syntax_name = get_syntax_name(view.settings().get('syntax')).lower()
    syntax_settings = s.get(syntax_name)
    return s, syntax_name, syntax_settings

def get_tpl_file(settings, filename):
    template_root = os.path.join(
                    PACKAGES_PATH,
                    PACKAGE_NAME,
                    settings.get('template_root'))
    return os.path.join(template_root, filename)


def check_start(v, flag):
    return v.substr(0) == flag[0]


class WriteHeader(sublime_plugin.EventListener):
    def on_pre_save(self, view):
        s, syntax_name, syntax_settings = get_syntax_vars(view)
        if syntax_settings and \
            syntax_settings.get('on_save') and \
            not check_start(view, syntax_settings.get('first_character')):
                with open(get_tpl_file(s, '%s.tpl' % syntax_name)) as f:
                    template = f.read()
                edit = view.begin_edit()
                view.insert(edit, 0, template.strip() + '\n\n')
                view.end_edit(edit)


class WriteHeaderCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        s, syntax_name, syntax_settings = get_syntax_vars(self.view)
        if syntax_settings and \
            not check_start(view, syntax_settings.get('first_character')):
            with open(get_tpl_file(s, '%s.tpl' % syntax_name)) as f:
                    template = f.read()
            self.view.insert(edit, 0, template.strip() + '\n\n')
