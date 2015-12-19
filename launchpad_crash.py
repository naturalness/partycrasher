#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright (C) 2015 Jshua Charles Campbell

#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from crash import Crash, Stacktrace, Stackframe

import os, re, io, chardet
import dateutil.parser as dateparser
import unicodedata

class LaunchpadFrame(Stackframe):
    
    @classmethod
    def load_from_strings(cls, line_raw, extras=None):
        frame = LaunchpadFrame()
        matched = False
        line = u""
        for ch in line_raw:
            if unicodedata.category(ch)[0] == 'C':
                ch = u'?'
                #raise ValueError("Bad encoding %s in: %s" % (ch.encode('unicode_escape'), line.encode('utf-8')))
            elif ch == u'\ufffd':
                ch = u'?'
            line += ch
        if not matched: #number address in function (args) at file from lib
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(.+?)\s+\(([^\)]*)\)\s+at\s+(\S+)\sfrom\s+(\S+)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                frame['file'] = match.group(5)
                frame['dylib'] = match.group(6)
                matched = True
        if not matched: #number address in function (args) from lib
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(.+?)\s+\(([^\)]*)\)\s+from\s+(.+?)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                frame['dylib'] = match.group(5)
                matched = True
        if not matched:  #number address in function (args) at file
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(.+?)\s+\((.*?)\)\s+at\s+(\S+)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                frame['file'] = match.group(5)
                matched = True
        if not matched: #number function (args) at file
            match = re.match('^#(\d+)\s+(.+?)\s+\((.*?)\)\s+at\s+(\S+)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['function'] = match.group(2)
                frame['args'] = match.group(3)
                frame['file'] = match.group(4)
                matched = True
        if not matched: #number address in function (args
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(.+?)\s*\((.*?)\)?\s*$', line)
            if match is not None:
                assert (not re.search(' at ', line))
                assert (not re.search(' from ', line))
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                matched = True
        if not matched: #number address in function
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(.+?)\s*$', line)
            if match is not None:
                assert (not re.search(' at ', line))
                assert (not re.search(' from ', line))
                assert (not re.search('\(.*?\)', line))
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                matched = True
        if not matched: #number function (args
            match = re.match('^#(\d+)\s+(.+?)\s+\((.*?)\)?\s*$', line)
            if match is not None:
                assert (not re.search(' at ', line))
                assert (not re.search(' from ', line))
                assert (not re.search(' ()\s*$', line))
                frame['depth'] = int(match.group(1))
                frame['function'] = match.group(2)
                frame['args'] = match.group(3)
                matched = True
        if not matched: #number <function>
            match = re.match('^#(\d+)\s+(<.*?>)\s*$', line)
            if match is not None:
                assert (not re.search(' at ', line))
                assert (not re.search(' from ', line))
                assert (not re.search('\(.*?\)', line))
                frame['depth'] = int(match.group(1))
                frame['function'] = match.group(2)
                matched = True
        leftover_extras = []
        if extras is not None:
            for extra in extras:
                extra_matched = False
                if not extra_matched:
                    match = re.match('^\s*at\s+([^\s:]+):(\d+)\s*$', extra)
                    if match is not None:
                        frame['file'] = match.group(1)
                        frame['fileline'] = match.group(2)
                        extra_matched = True
                if not extra_matched:
                    leftover_extras.append(extra)
        if len(leftover_extras) > 0:
            frame['extra'] = leftover_extras
        if matched:
            return frame
        else:
            raise RuntimeError("Couldn't recognize stack frame format: %s" % (line.encode('unicode_escape')))

class LaunchpadStack(Stacktrace):
    
    @classmethod
    def load_from_file(cls, path):
        
        #with io.open(path, mode="r+b") as stackfile:
            #encoding_guess = chardet.detect(stackfile.read())['encoding']
        #with open(path) as stackfile:
        encoding_guess = 'utf-8'
        with io.open(path, encoding=encoding_guess, errors='replace') as stackfile:
            stacklines = stackfile.readlines()
        stack = LaunchpadStack()
        extras = []
        prevline = None
        for line in  stacklines:
            line = line.rstrip()
            #for ch in line.lstrip():
                #if ch != '\t' and unicodedata.category(ch)[0] == 'C':
                    #raise ValueError("Bad encoding %s %s: %s" % (encoding_guess, ch.encode('unicode_escape'), line.encode('unicode_escape')))
            if re.match('^#', line):
                if prevline is not None:
                    stack.append(LaunchpadFrame.load_from_strings(prevline,extras))
                prevline = line
                extras = []
            else:
                extras.append(line.rstrip())
        stack.append(LaunchpadFrame.load_from_strings(prevline,extras))
        
        return stack


class LaunchpadCrash(Crash):
    
    synonyms = Crash.synonyms
    synonyms['ProblemType'] = 'type'
    synonyms['DistroRelease'] = 'os'
    synonyms['ProcVersionSignature'] = 'os_version'
    synonyms['Architecture'] = 'cpu'
    synonyms['Date'] = 'date'
    
    def __setitem__(self, key, val):
        if key == 'Date': # Apport
            return super(LaunchpadCrash, self).__setitem__('date', dateparser.parse(val))
        else:
            return super(LaunchpadCrash, self).__setitem__(key, val)
        
    
    @classmethod
    def load_from_file(cls, path):
        crash = LaunchpadCrash()
        if os.path.isdir(path):
            post_path = os.path.join(path, "Post.txt")
            if not os.path.isfile(post_path):
                raise NotImplementedError("Missing %s, I don't know how to load this." % (post_path))
            with open(post_path) as postfile: post = postfile.read()
            matches = re.findall('^\s*(\S+):\s+(\S+(?:\s+\S+)*?)\s*$', post, re.MULTILINE)
            if matches is not None:
                for match in matches:
                    crash[match[0]] = match[1]
            stack_path = None
            if os.path.isfile(os.path.join(path, "Stacktrace.txt (retraced)")):
                stack_path = os.path.join(path, "Stacktrace.txt (retraced)")
            elif os.path.isfile(os.path.join(path, "StacktraceSource.txt")):
                stack_path = os.path.join(path, "StacktraceSource.txt")
            elif os.path.isfile(os.path.join(path, "Stacktrace.txt")):
                stack_path = os.path.join(path, "Stacktrace.txt")
            elif os.path.isfile(os.path.join(path, "Stacktrace")):
                stack_path = os.path.join(path, "Stacktrace")
            assert (stack_path is not None)
            crash['stacktrace'] = LaunchpadStack.load_from_file(stack_path)
        else:
            raise NotImplementedError("Not a directory, I don't know how to load this.")
        return crash

import unittest
class TestCrash(unittest.TestCase):
    
    # Example from https://bugs.launchpad.net/ubuntu/+source/audacious/+bug/216088
    example_ubuntu_post = \
        'ProblemType: Crash\n'\
        'Architecture: i386\n'\
        'Date: Fri Apr 11 22:12:11 2008\n'\
        'DistroRelease: Ubuntu 8.04\n'\
        'ExecutablePath: /usr/bin/audacious\n'\
        'NonfreeKernelModules: nvidia\n'\
        'Package: audacious 1.5.0-2\n'\
        'PackageArchitecture: i386\n'\
        'ProcCmdline: audacious\n'\
        'ProcEnviron:\n'\
        ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n'\
        ' LANG=es_UY.UTF-8\n'\
        ' SHELL=/bin/bash\n'\
        'Signal: 11\n'\
        'SourcePackage: audacious\n'\
        'StacktraceTop:\n'\
        ' free () from /lib/tls/i686/cmov/libc.so.6\n'\
        ' g_free () from /usr/lib/libglib-2.0.so.0\n'\
        ' ?? ()\n'\
        ' ?? ()\n'\
        ' ?? ()\n'\
        'Title: audacious crashed with SIGSEGV in free()\n'\
        'Uname: Linux 2.6.24-16-generic i686\n'\
        'UserGroups: adm admin audio cdrom dialout dip floppy fuse lpadmin plugdev video\n'
    example_ubuntu_stacktrace = \
        '#0  0xb77404c7 in free () from /lib/tls/i686/cmov/libc.so.6\n'\
        '#1  0xb78e78b1 in IA__g_free (mem=0x80bcf84) at /build/buildd/glib2.0-2.16.3/glib/gmem.c:190\n'\
        '  [Error: /build/buildd/glib2.0-2.16.3/glib/gmem.c was not found in source tree]\n'\
        '#2  0x0805c594 in bmp_config_free () at main.c:610\n'\
        '  605: {\n'\
        '  606:   gint i;\n'\
        '  607:   for (i = 0; i < ncfgsent; ++i) {\n'\
        '  608:     if ( *(bmp_strents[i].se_vloc) != NULL )\n'\
        '  609:     {\n'\
        '  610:       g_free( *(bmp_strents[i].se_vloc) );\n'\
        '  611:       *(bmp_strents[i].se_vloc) = NULL;\n'\
        '  612:     }\n'\
        '  613:   }\n'\
        '  614: }\n'\
        '  615: \n'\
        '#3  0x08094565 in on_reload_plugins_clicked (button=0x85d9a68, data=0x0) at ui_preferences.c:1325\n'\
        '  1320:      * symbol sizes change.                       - nenolod\n'\
        '  1321:      */\n'\
        '  1322: \n'\
        '  1323:     bmp_config_save();\n'\
        '  1324:     plugin_system_cleanup();\n'\
        '  1325:     bmp_config_free();\n'\
        '  1326:     bmp_config_load();\n'\
        '  1327:     plugin_system_init();\n'\
        '  1328: }\n'\
        '  1329: \n'\
        '  1330: void\n'\
        '#4  0xb7979a4f in IA__g_cclosure_marshal_VOID__VOID (closure=0x85d47a8, return_value=0x0, n_param_values=1, \n'\
        '#5  0xb796c759 in IA__g_closure_invoke (closure=0x85d47a8, return_value=0x0, n_param_values=1, \n'\
        '#6  0xb7980d1d in signal_emit_unlocked_R (node=0x8369788, detail=0, instance=0x85d9a68, emission_return=0x0, \n'\
        '#7  0xb7982916 in IA__g_signal_emit_valist (instance=0xb781d168, signal_id=127, detail=0, \n'\
        '#8  0xb7982c59 in IA__g_signal_emit (instance=0x85d9a68, signal_id=127, detail=0)\n'\
        '#9  0xb7b9501a in IA__gtk_button_clicked (button=0x85d9a68)\n'\
        '#10 0xb7b96b7e in gtk_real_button_released (button=0x85d9a68)\n'\
        '#11 0xb7979a4f in IA__g_cclosure_marshal_VOID__VOID (closure=0x8366a18, return_value=0x0, n_param_values=1, \n'\
        '#12 0xb796b079 in g_type_class_meta_marshal (closure=0x8366a18, return_value=0x0, n_param_values=1, \n'\
        '#13 0xb796c759 in IA__g_closure_invoke (closure=0x8366a18, return_value=0x0, n_param_values=1, \n'\
        '#14 0xb7980975 in signal_emit_unlocked_R (node=0x8369720, detail=0, instance=0x85d9a68, emission_return=0x0, \n'\
        '#15 0xb7982916 in IA__g_signal_emit_valist (instance=0xb781d168, signal_id=126, detail=0, \n'\
        '#16 0xb7982c59 in IA__g_signal_emit (instance=0x85d9a68, signal_id=126, detail=0)\n'\
        '#17 0xb7b950aa in IA__gtk_button_released (button=0x85d9a68)\n'\
        '#18 0xb7b950d1 in gtk_button_button_release (widget=0x85d9a68, event=0x860cb28)\n'\
        '#19 0xb7c6e8b4 in _gtk_marshal_BOOLEAN__BOXED (closure=0x8150148, return_value=0xbfdbbc50, n_param_values=2, \n'\
        '#20 0xb796b079 in g_type_class_meta_marshal (closure=0x8150148, return_value=0xbfdbbc50, n_param_values=2, \n'\
        '#21 0xb796c759 in IA__g_closure_invoke (closure=0x8150148, return_value=0xbfdbbc50, n_param_values=2, \n'\
        '#22 0xb7980ea0 in signal_emit_unlocked_R (node=0x8150230, detail=0, instance=0x85d9a68, \n'\
        '#23 0xb798264e in IA__g_signal_emit_valist (instance=0x85d9a68, signal_id=34, detail=0, \n'\
        '#24 0xb7982c59 in IA__g_signal_emit (instance=0x85d9a68, signal_id=34, detail=0)\n'\
        '#25 0xb7d8d5f7 in gtk_widget_event_internal (widget=0x85d9a68, event=0x860cb28)\n'\
        '#26 0xb7c67b01 in IA__gtk_propagate_event (widget=0x85d9a68, event=0x860cb28)\n'\
        '#27 0xb7c68d68 in IA__gtk_main_do_event (event=0x860cb28) at /build/buildd/gtk+2.0-2.12.9/gtk/gtkmain.c:1556\n'\
        '  [Error: /build/buildd/gtk+2.0-2.12.9/gtk/gtkmain.c was not found in source tree]\n'\
        '#28 0xb7ae1a9a in gdk_event_dispatch (source=0x8147ba0, callback=0, user_data=0x0)\n'\
        '#29 0xb78dfbf8 in IA__g_main_context_dispatch (context=0x8147be8)\n'\
        '#30 0xb78e2e5e in g_main_context_iterate (context=0x8147be8, block=1, dispatch=1, self=0x811e3e8)\n'\
        '#31 0xb78e31e7 in IA__g_main_loop_run (loop=0x860db40) at /build/buildd/glib2.0-2.16.3/glib/gmain.c:2850\n'\
        '  [Error: /build/buildd/glib2.0-2.16.3/glib/gmain.c was not found in source tree]\n'\
        '#32 0xb7c69244 in IA__gtk_main () at /build/buildd/gtk+2.0-2.12.9/gtk/gtkmain.c:1163\n'\
        '  [Error: /build/buildd/gtk+2.0-2.12.9/gtk/gtkmain.c was not found in source tree]\n'\
        '#33 0x0805e407 in main (argc=1, argv=0xbfdbc264) at main.c:1572\n'\
        '  1567:                 playback_seek(cfg.resume_playback_on_startup_time / 1000);\n'\
        '  1568:                 output_set_volume(l, r);\n'\
        '  1569:             }\n'\
        '  1570:         }\n'\
        '  1571:         \n'\
        '  1572:         gtk_main();\n'\
        '  1573: \n'\
        '  1574:         GDK_THREADS_LEAVE();\n'\
        '  1575: \n'\
        '  1576:         g_cond_free(cond_scan);\n'\
        '  1577:         g_mutex_free(mutex_scan);\n'

    def test_ubuntu(self):
        import tempfile
        import os
        import shutil
        import datetime
        dirpath=tempfile.mkdtemp()
        try:
            # Test setup
            stacktrace_path = os.path.join(dirpath, "Stacktrace.txt")
            with open(stacktrace_path, 'w') as stacktrace_file:
                stacktrace_file.write(self.example_ubuntu_stacktrace)
            post_path = os.path.join(dirpath, "Post.txt")
            with open(post_path, 'w') as post_file:
                post_file.write(self.example_ubuntu_post)
            
            # Test crash loader
            crash = Crash.load_from_file(dirpath)
            
            # test that contents are loaded correctly
            assert (isinstance(crash, Crash))
            assert (crash['cpu'] == 'i386')
            assert (crash['date'] == datetime.datetime(2008, 4, 11, 22, 12, 11))
            stacktrace = crash['stacktrace']
            assert (isinstance(stacktrace, Stacktrace))
            assert (isinstance(stacktrace[0], Stackframe))
            assert (stacktrace[0]['depth'] == 0)
            assert (stacktrace[0]['function'] == 'free')
            assert (stacktrace[1]['depth'] == 1)
            assert (stacktrace[1]['address'] == '0xb78e78b1')
            
        finally:
            shutil.rmtree(dirpath)
            
            
    example_ubuntu_post2 = \
        'Binary package hint: evince\n'\
        '\n'\
        'This happens immediately when trying to mark text with the mouse.\n'\
        '\n'\
        'ProblemType: Crash\n'\
        'Architecture: amd64\n'\
        'Date: Wed Jun 20 10:27:06 2007\n'\
        'DistroRelease: Ubuntu 7.10\n'\
        'ExecutablePath: /usr/bin/evince\n'\
        'NonfreeKernelModules: vmnet vmmon\n'\
        'Package: evince 0.9.0-1ubuntu4\n'\
        'PackageArchitecture: amd64\n'\
        'ProcCmdline: evince ./expenses-uds-sevilla.pdf\n'\
        'ProcCwd: /home/martin\n'\
        'ProcEnviron:\n'\
        ' SHELL=/bin/bash\n'\
        ' PATH=/home/martin/bin:/usr/lib/ccache:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n'\
        ' LANG=de_DE.UTF-8\n'\
        ' LANGUAGE=de_DE.UTF-8\n'\
        'Signal: 11\n'\
        'SourcePackage: evince\n'\
        'StacktraceTop:\n'\
        ' cairo_transform () from /usr/lib/libcairo.so.2\n'\
        ' CairoOutputDev::setDefaultCTM () from /usr/lib/libpoppler-glib.so.1\n'\
        ' TextSelectionPainter::TextSelectionPainter () from /usr/lib/libpoppler.so.1\n'\
        ' TextPage::drawSelection () from /usr/lib/libpoppler.so.1\n'\
        ' poppler_page_render_selection () from /usr/lib/libpoppler-glib.so.1\n'\
        'Title: evince crashed with SIGSEGV in cairo_transform()\n'\
        'Uname: Linux donald 2.6.20-15-generic #2 SMP Sun Apr 15 06:17:24 UTC 2007 x86_64 GNU/Linux\n'\
        'UserGroups: adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video'

    example_ubuntu_stacktrace2 = \
        '#0  cairo_transform (cr=0x0, matrix=0x7fff69ce7c40) at /build/buildd/libcairo-1.4.6/src/cairo.c:1222\n'\
        '\tstatus = <value optimized out>\n'\
        '#1  0x00002b344498a150 in CairoOutputDev::setDefaultCTM () from /usr/lib/libpoppler-glib.so.1\n'\
        '#2  0x00002b344ae2cefc in TextSelectionPainter::TextSelectionPainter () from /usr/lib/libpoppler.so.1\n'\
        '#3  0x00002b344ae2cff0 in TextPage::drawSelection () from /usr/lib/libpoppler.so.1\n'\
        '#4  0x00002b344498684a in poppler_page_render_selection () from /usr/lib/libpoppler-glib.so.1\n'\
        '#5  0x000000000045be48 in pdf_selection_render_selection (selection=<value optimized out>, rc=0xc53a40, pixbuf=<value optimized out>, points=0xbf4a90, old_points=0x0, \n'\
        '    text=0xb77bf8, base=0xb77c34) at /build/buildd/evince-0.9.0/./backend/pdf/ev-poppler.cc:1632\n'\
        '\twidth_points = 612\n'\
        '\theight_points = 792\n'\
        '#6  0x0000000000430a9e in ev_pixbuf_cache_get_selection_pixbuf (pixbuf_cache=0xd738a0, page=<value optimized out>, scale=<value optimized out>, region=0x7fff69ce8010)\n'\
        '    at /build/buildd/evince-0.9.0/./shell/ev-pixbuf-cache.c:906\n'\
        '\told_points = (EvRectangle *) 0x0\n'\
        '\ttext = (GdkColor *) 0xb77bf8\n'\
        '\tbase = (GdkColor *) 0xb77c34\n'\
        '\tjob_info = (CacheJobInfo *) 0xbf4a40\n'\
        '\t__PRETTY_FUNCTION__ = "ev_pixbuf_cache_get_selection_pixbuf"\n'\
        '#7  0x000000000043acd1 in selection_update_idle_cb (view=0x6e41d0) at /build/buildd/evince-0.9.0/./shell/ev-view.c:4555\n'\
        'No locals.\n'\
        '#8  0x00002b34478c9fd3 in IA__g_main_context_dispatch (context=0x6eea30) at /build/buildd/glib2.0-2.13.5/glib/gmain.c:2061\n'\
        'No locals.\n'\
        '#9  0x00002b34478cd2dd in g_main_context_iterate (context=0x6eea30, block=1, dispatch=1, self=<value optimized out>) at /build/buildd/glib2.0-2.13.5/glib/gmain.c:2694\n'\
        '\tgot_ownership = <value optimized out>\n'\
        '\tmax_priority = 200\n'\
        '\ttimeout = 0\n'\
        '\tsome_ready = 1\n'\
        '\tnfds = <value optimized out>\n'\
        '\tallocated_nfds = <value optimized out>\n'\
        '\tfds = (GPollFD *) 0x7367e0\n'\
        '\t__PRETTY_FUNCTION__ = "g_main_context_iterate"\n'\
        '#10 0x00002b34478cd5ea in IA__g_main_loop_run (loop=0x72c990) at /build/buildd/glib2.0-2.13.5/glib/gmain.c:2898\n'\
        '\tgot_ownership = <value optimized out>\n'\
        '\tself = (GThread *) 0x6b2940\n'\
        '\t__PRETTY_FUNCTION__ = "IA__g_main_loop_run"\n'\
        '#11 0x00002b344355a623 in IA__gtk_main () at /build/buildd/gtk+2.0-2.11.3/gtk/gtkmain.c:1143\n'\
        '\ttmp_list = (GList *) 0x6da580\n'\
        '\tfunctions = (GList *) 0x0\n'\
        '\tinit = (GtkInitFunction *) 0x72c990\n'\
        '\tloop = (GMainLoop *) 0x72c990\n'\
        '#12 0x000000000044c710 in main (argc=7185800, argv=<value optimized out>) at /build/buildd/evince-0.9.0/./shell/main.c:382\n'\
        '\tvalue = <value optimized out>\n'\
        '\tscreen = <value optimized out>\n'\
        '\tdisplay_name = (const gchar *) 0x0\n'\
        '\tmode = 7185792\n'\
        '\tdisplay = <value optimized out>\n'\
        '\tscreen_number = 7563232\n'\
        '\tenable_metadata = 0\n'\
        '\tcontext = <value optimized out>\n'\
        '\targs = (GHashTable *) 0x6f4cc0\n'\
        '\tprogram = (GnomeProgram *) 0x6c1050'

    def test_ubuntu2(self):
        import tempfile
        import os
        import shutil
        import datetime
        dirpath=tempfile.mkdtemp()
        try:
            # Test setup
            stacktrace_path = os.path.join(dirpath, "Stacktrace.txt (retraced)")
            with open(stacktrace_path, 'w') as stacktrace_file:
                stacktrace_file.write(self.example_ubuntu_stacktrace2)
            post_path = os.path.join(dirpath, "Post.txt")
            with open(post_path, 'w') as post_file:
                post_file.write(self.example_ubuntu_post2)
            
            # Test crash loader
            crash = Crash.load_from_file(dirpath)
            
            # test that contents are loaded correctly
            assert (isinstance(crash, Crash))
            assert (crash['cpu'] == 'amd64')
            assert (crash['date'] == datetime.datetime(2007, 6, 20, 10, 27, 6))
            stacktrace = crash['stacktrace']
            assert (isinstance(stacktrace, Stacktrace))
            assert (isinstance(stacktrace[0], Stackframe))
            assert (stacktrace[0]['depth'] == 0)
            assert (stacktrace[0]['function'] == 'cairo_transform')
            assert (not 'address' in stacktrace[0])
            assert (stacktrace[1]['depth'] == 1)
            assert (stacktrace[1]['address'] == '0x00002b344498a150')
            
        finally:
            shutil.rmtree(dirpath)
    
    example_ubuntu_post3 = \
        'Binary package hint: beryl-core\n'\
        '\n'\
        'Login in\n'\
        '\n'\
        'ProblemType: Crash\n'\
        'Architecture: amd64\n'\
        'Date: Wed Jun 27 14:22:11 2007\n'\
        'DistroRelease: Ubuntu 7.10\n'\
        'ExecutablePath: /usr/bin/beryl\n'\
        'NonfreeKernelModules: nvidia\n'\
        'Package: beryl-core 0.2.1.dfsg+git20070318-0ubuntu3\n'\
        'PackageArchitecture: amd64\n'\
        'ProcCmdline: beryl --skip-gl-yield\n'\
        'ProcCwd: /home/svajda\n'\
        'ProcEnviron:\n'\
        ' LANGUAGE=en_US.UTF-8\n'\
        ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/bin/X11:/usr/games\n'\
        ' LANG=en_US.UTF-8\n'\
        ' SHELL=/bin/bash\n'\
        'Signal: 11\n'\
        'SourcePackage: beryl-core\n'\
        'StacktraceTop:\n'\
        ' nanosleep () from /lib/libc.so.6\n'\
        ' sleep () from /lib/libc.so.6\n'\
        ' IceOpenConnection () from /usr/lib/libICE.so.6\n'\
        ' SmcOpenConnection () from /usr/lib/libSM.so.6\n'\
        ' initSession ()\n'\
        'Title: beryl crashed with SIGSEGV in nanosleep()\n'\
        'Uname: Linux blackstone 2.6.22-7-generic #1 SMP Mon Jun 25 17:07:55 GMT 2007 x86_64 GNU/Linux\n'\
        'UserGroups: adm admin audio cdrom dialout dip floppy lpadmin plugdev scanner video'

            
    example_ubuntu_stacktrace3 = \
        '#0  XQueryExtension (dpy=0x0, name=0x2b9e31057f11 "MIT-SHM", major_opcode=0x7fff7bd6cc54, first_event=0x7fff7bd6cc58, first_error=0x7fff7bd6cc5c)\n'\
        '    at ../../src/QuExt.c:46\n'\
        '\trep = {type = 144 \'\\220\', pad1 = 106 \'j\', sequenceNumber = 12447, length = 11166, present = 0 \'\\0\', major_opcode = 96 \'`\', first_event = 158 \'\\236\', \n'\
        '  first_error = 48 \'0\', pad3 = 11166, pad4 = 822392720, pad5 = 11166, pad6 = 815688040, pad7 = 11166}\n'\
        '#1  0x00002b9e30d6faa4 in XInitExtension (dpy=0x0, name=0x2b9e31057f11 "MIT-SHM") at ../../src/InitExt.c:49\n'\
        '\tcodes = {extension = 1, major_opcode = 0, first_event = 816156333, first_error = 11166}\n'\
        '\text = <value optimized out>\n'\
        '#2  0x00002b9e31057c09 in XextAddDisplay (extinfo=0x2b9e3125ab80, dpy=0x0, ext_name=0x2b9e31057f11 "MIT-SHM", hooks=0x2b9e3125a840, nevents=1, data=0x0)\n'\
        '    at ../../src/extutil.c:108\n'\
        '\tdpyinfo = (XExtDisplayInfo *) 0x647cb0\n'\
        '#3  0x00002b9e3105328e in XShmDetach (dpy=0x0, shminfo=0x2b9e31057f11) at ../../src/XShm.c:254\n'\
        '\tinfo = <value optimized out>\n'\
        '#4  0x000000000040fb0b in releaseDisplay () at display.c:2390\n'\
        'No locals.\n'\
        '#5  0x000000000040be25 in signalHandler (sig=0) at main.c:128\n'\
        '\tstatus = 11166\n'\
        '#6  <signal handler called>\n'\
        '#7  0x00002b9e30a7d750 in __nanosleep_nocancel () from /lib/libc.so.6\n'\
        '#8  0x00002b9e30a7d5a4 in sleep () from /lib/libc.so.6\n'\
        '#9  0x00002b9e2fb9d2e9 in IceOpenConnection (networkIdsList=<value optimized out>, context=0x0, mustAuthenticate=0, majorOpcodeCheck=1, errorLength=1024, \n'\
        '    errorStringRet=0x7fff7bd6d770 "") at ../../src/connect.c:510\n'\
        '\tdelim = <value optimized out>\n'\
        '\tlen = <value optimized out>\n'\
        '\taddress_size = <value optimized out>\n'\
        '\taddrbuf = "local/blackstone:/tmp/.ICE-unix/24847\\000\\000\\000\\bl!\\000\\000\\000\\000\\000\\023\\000\\000\\000\\000\\000\\000\\000\xe0|d\\000\\000\\000\\000\\000\\001\\000\\000\\000\\000\\000\\000\\000H\xd4c\\000\\000\\000\\000\\000\\000p\xb9/\\236+\\000\\000D\\206\xd4.\\236+\\000\\000\xc8\\206\xb9/\\236+\\000\\000pyx/\\236+\\000\\000\\000\\000\\000\\000\\000\\000\\000\\000\xff\xff\xff\xff\\000\\000\\000\\000\xb0\\v\\2370\\236+\\000\\000@w ", \'\\0\' <repeats 13 times>, "\xa4h\xb9/\\236+\\000\\000\\000\\000\\000\\000\\000\\000\\000\\000H\xd4c\\000\\000\\000\\000\\000\\000\xf0\\230/\\236+\\000\\000D\\206\xd4.\\236+\\000\\000\\001", \'\\0\' <repeats 15 times>...\n'\
        '\taddress = 0x7fff7bd6d500 "local/blackstone:/tmp/.ICE-unix/24847"\n'\
        '\tmadeConnection = 0\n'\
        '\tretry = 2\n'\
        '\tconnect_stat = -2\n'\
        '\ttrans_conn = (XtransConnInfo) 0x643360\n'\
        '\ticeConn = (IceConn) 0x643220\n'\
        '\textra = <value optimized out>\n'\
        '\ti = <value optimized out>\n'\
        '\tj = <value optimized out>\n'\
        '\tendian = <value optimized out>\n'\
        '\tgotReply = <value optimized out>\n'\
        '\tioErrorOccured = <value optimized out>\n'\
        '\tsetup_sequence = <value optimized out>\n'\
        '\tpByteOrderMsg = <value optimized out>\n'\
        '\tpSetupMsg = <value optimized out>\n'\
        '\tpData = <value optimized out>\n'\
        '\treplyWait = {sequence_of_request = 47958401250488, major_opcode_of_request = 798556531, minor_opcode_of_request = 11166, reply = 0x7fff7bd6d678}\n'\
        '\treply = {type = 650271786, connection_reply = {type = 650271786, version_index = 0, vendor = 0x12ed448d4 <Address 0x12ed448d4 out of bounds>, \n'\
        '    release = 0x2b9e2f787818 "\xb8\\202\xd5.\\236+"}, connection_error = {type = 650271786, error_message = 0x12ed448d4 <Address 0x12ed448d4 out of bounds>}, \n'\
        '  protocol_reply = {type = 650271786, major_opcode = 0, version_index = 785664212, vendor = 0x2b9e2f787818 "\xb8\\202\xd5.\\236+", \n'\
        '    release = 0x7fff7bd6d5e0 "\xc8\\206\xb9/\\236+"}, protocol_error = {type = 650271786, error_message = 0x12ed448d4 <Address 0x12ed448d4 out of bounds>}}\n'\
        '\tauthUsableCount = <value optimized out>\n'\
        '\tauthUsableFlags = {1, 32767, 796424216, 11166, 2077676976, 32767, 2077676896, 32767, 2077676920, 32767, 918218968, 0, 0, 0, 785664755, 11166, 0, 0, \n'\
        '  0, 0, 1, 16777216, 0, 0, 1, 0, 842738704, 11166, 6, 0, 0, 0}\n'\
        '\tauthIndices = {918218968, 0, 785664212, 11166, 0, 1, 2077676528, 32767, 918218968, 0, 2077676896, 32767, 2077676920, 32767, 800685248, 11166, 0, 0, \n'\
        '  0, 0, 796424560, 11166, 798556531, 11166, 800690648, 11166, 798553744, 11166, 0, 1, 107, 1}\n'\
        '#10 0x00002b9e2f991bc4 in SmcOpenConnection (networkIdsList=0x0, context=0x0, xsmpMajorRev=<value optimized out>, xsmpMinorRev=<value optimized out>, \n'\
        '    mask=15, callbacks=0x640a00, previousId=0x0, clientIdRet=0x640a58, errorLength=1024, errorStringRet=0x7fff7bd6d770 "") at ../../src/sm_client.c:135\n'\
        '\tsmcConn = <value optimized out>\n'\
        '\ticeConn = <value optimized out>\n'\
        '\tids = 0x7fff7bd6d310 ""\n'\
        '\tsetupstat = <value optimized out>\n'\
        '\tmajorVersion = <value optimized out>\n'\
        '\tminorVersion = <value optimized out>\n'\
        '\tvendor = 0x0\n'\
        '\trelease = 0x0\n'\
        '\tpMsg = <value optimized out>\n'\
        '\treplyWait = {sequence_of_request = 2, major_opcode_of_request = 0, minor_opcode_of_request = 0, reply = 0x0}\n'\
        '\treply = {status = 1, client_id = 0x0}\n'\
        '\tgotReply = <value optimized out>\n'\
        '\tauth_names = {0x2b9e2f995800 "MIT-MAGIC-COOKIE-1"}\n'\
        '\tauth_procs = {0x2b9e2fb9f350 <_IcePoMagicCookie1Proc>}\n'\
        '\tversions = {{major_version = 1, minor_version = 0, process_msg_proc = 0x2b9e2f994a00 <_SmcProcessMessage>}}\n'\
        '#11 0x000000000042a2f5 in initSession (smPrevClientId=0x0) at session.c:126\n'\
        '\terrorBuffer = "\\000\xd9\xd6{\xff\\177\\000\\000\xb0\\036\xd40\\236+", \'\\0\' <repeats 18 times>, "\xb0d\\2360\\236+\\000\\000\xc3\xa2\xd40\\236+\\000\\000\\200\\237\xd40\\236+\\000\\000\\030\\230\xd40\\236+\\000\\000\\000\\000\\000\\000\\001\\000\\000\\000\\017\\005\\000\\000\\001", \'\\0\' <repeats 11 times>, "\\020h\\2360\\236+\\000\\000@\xd9\xd6{\xff\\177\\000\\000\xf0\xd8\xd6{\xff\\177\\000\\000\\b\xd9\xd6{\xff\\177\\000\\000`\\211\xd30\\236+\\000\\000\xa8\\211\xd30\\236+\\000\\000\xa8\\211\xd30\\236+\\000\\000\\000\\000\\000\\000\\000\\000\\000\\000\xc0\\211\xd30\\236+\\000\\000\\001\\000\\000\\000\\236+\\000\\000\\000\\000\\000\\000\\000\\000\\000\\000\\001\\000\\000\\000\\236+\\000\\000@\xd9\xd6{\xff\\177\\000\\000\xb0d\\2360\\236+\\000\\000\xb0}d\\000\\000\\000\\000\\000P"...\n'\
        '\tcallbacks = {save_yourself = {callback = 0x42a4c0 <saveYourselfCallback>, client_data = 0x0}, die = {callback = 0x42a4b0 <dieCallback>, \n'\
        '    client_data = 0x0}, save_complete = {callback = 0x42a170 <saveCompleteCallback>, client_data = 0x0}, shutdown_cancelled = {\n'\
        '    callback = 0x42a180 <shutdownCancelledCallback>, client_data = 0x0}}\n'\
        '#12 0x000000000040bbbe in main (argc=2, argv=0x7fff7bd6e818) at main.c:365\n'\
        '\tdisplayName = <value optimized out>\n'\
        '\tplugin = {0x7fff7bd6e3c0 "", 0x2b9e2ed471dc <Address 0x2b9e2ed471dc out of bounds>, 0x2b9e2ed5a900 "", 0x2b9e309e64b0 "", 0x2b9e309e6000 "", 0x0, \n'\
        '  0x0, 0x7fff7bd6dce0 "\xb0d\\2360\\236+", 0x3 <Address 0x3 out of bounds>, 0x7fff7bd6dbb0 "\xf0\xe6\xd6{\xff\\177", 0x2b9e2ed4877b <Address 0x2b9e2ed4877b out of bounds>, \n'\
        '  0x0, 0xe <Address 0xe out of bounds>, 0x7fff7bd6e350 "\xab\xec\xd6{\xff\\177", 0x7fff7bd6e3c0 "", 0x2b9e2f17d058 "\\016", 0x0, 0x7fff7bd6de00 "P\xde\xd6{\xff\\177", \n'\
        '  0x2 <Address 0x2 out of bounds>, 0x2b9e2ed469fd <Address 0x2b9e2ed469fd out of bounds>, 0x0, 0x2b9e2f17d038 "\\001", 0x0, \n'\
        '  0x2b9e2ed48796 <Address 0x2b9e2ed48796 out of bounds>, 0x7fff7bd6e350 "\xab\xec\xd6{\xff\\177", 0x2b9e2ed469c0 <Address 0x2b9e2ed469c0 out of bounds>, \n'\
        '  0x7fff7bd6e38f "", 0x7fff7bd6e380 "", 0x7fff7bd6e378 "\\222\xe2\xd4.\\236+", 0x5 <Address 0x5 out of bounds>, 0x7fff7bd6e3c0 "", \n'\
        '  0x2b9e2ed471dc <Address 0x2b9e2ed471dc out of bounds>, 0x2b9e309e64b0 "", 0x2b9e2ed5a900 "", 0x2b9e309e6968 "", 0x2b9e309e6000 "", 0x0, \n'\
        '  0x7fff7bd6de00 "P\xde\xd6{\xff\\177", 0x2 <Address 0x2 out of bounds>, 0x7fff7bd6dca0 "P\xe3\xd6{\xff\\177", 0x2b9e2ed4877b <Address 0x2b9e2ed4877b out of bounds>, \n'\
        '  0x2b9e2f17d038 "\\001", 0x7fff7bd6e498 "\\004", 0x7fff7bd6dd80 "5", 0x0, 0x1 <Address 0x1 out of bounds>, 0x7fff7bd6e4e0 "\'\\031C", \n'\
        '  0x2b9e304194f1 <Address 0x2b9e304194f1 out of bounds>, 0x7fff7bd6dd80 "5", 0x7fff7bd6e4f0 "\\\\\xd4c", 0x0, \n'\
        '  0x2b9e30a3997b "D\\213\\205\xb8\xfc\xff\xffH\\211\xc1H\\213\xb5P\xfe\xff\xffH;u\xb8\\017\\204K\xf9\xff\xff\xf6\\205$\xfd\xff\xff\\b\\017\\205\xe3", 0xa000300000035 <Address 0xa000300000035 out of bounds>, \n'\
        '  0x7fff7bd6e810 "\\002", 0x2b9e3125b4a8 "/lib/libdl.so.2", 0x0, 0x8000300000000 <Address 0x8000300000000 out of bounds>, 0x7fff7bd6e350 "\xab\xec\xd6{\xff\\177", \n'\
        '  0x7fff7bd6e3c0 "", 0x4 <Address 0x4 out of bounds>, 0x7fff7bd6e3c0 "", 0x2b9e2ed471dc <Address 0x2b9e2ed471dc out of bounds>, \n'\
        '  0x1 <Address 0x1 out of bounds>, 0x2b9e3125b968 "", 0x7fff7bd6d430 "\\001", 0x0, 0x2b9e2ef5c6ed "libz.so.1", \n'\
        '  0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, 0x7fff7bd6de50 "\xc0\xe3\xd6{\xff\\177", 0x2b9e303884b8 "", 0x2b <Address 0x2b out of bounds>, \n'\
        '  0x60 <Address 0x60 out of bounds>, 0x7fff7bd6e378 "\\222\xe2\xd4.\\236+", 0x2b9e2ef58c18 "", 0x7fff7bd6e350 "\xab\xec\xd6{\xff\\177", 0x0, \n'\
        '  0x87bd6e38f <Address 0x87bd6e38f out of bounds>, 0x4063ca "libdl.so.2", 0x7fff7bd6e3c0 "", 0x63c5c0 "\\f", 0x0, 0x0, 0x0, 0x2b9e30d38960 "", \n'\
        '  0x2b <Address 0x2b out of bounds>, 0x7fff7bd6ecab "beryl", 0x7fff7bd6e390 " ", 0x0, 0x6 <Address 0x6 out of bounds>, \n'\
        '  0x2b9e30a58ead "H\\205\xc0I\\211\xc4tJ\\203=\xcc/.", 0x7fff7bd6e5e0 "\\203\\031C", 0x25 <Address 0x25 out of bounds>, 0x7fff7bd6ecab "beryl", \n'\
        '  0x2b9e2ed48903 <Address 0x2b9e2ed48903 out of bounds>, 0x0, 0x7fff7bd6de60 "", 0x2b9e2ed4877b <Address 0x2b9e2ed4877b out of bounds>, 0x63c590 "\\001", \n'\
        '  0x0, 0x0, 0x1 <Address 0x1 out of bounds>, 0x2b9e3125b4b8 "", 0x7fff7bd6ddd0 "\\001", 0x2b9e2ed493a5 <Address 0x2b9e2ed493a5 out of bounds>, \n'\
        '  0x4063ca "libdl.so.2", 0x2b9e2ed58000 "", 0x2b9e31466a1f "", 0x2b9e2ed433c0 <Address 0x2b9e2ed433c0 out of bounds>, 0x7fff7bd6df00 "\\001", 0x0, \n'\
        '  0x406334 "libXrender.so.1", 0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, 0x1 <Address 0x1 out of bounds>, 0x2b9e309e6968 "", \n'\
        '  0x7fff7bd6df30 "\\037jF1\\236+", 0x90000101 <Address 0x90000101 out of bounds>, 0x2 <Address 0x2 out of bounds>, \n'\
        '  0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, 0x1 <Address 0x1 out of bounds>, 0x2b9e309e64b0 "", 0x7fff7bd6df60 "\\001", 0x0, \n'\
        '  0x405e86 "libX11.so.6", 0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, 0x1 <Address 0x1 out of bounds>, 0x2b9e309e6000 "", 0x7fff7bd6df90 "\\001", \n'\
        '  0x0, 0x405cd6 "libc.so.6", 0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, 0x1 <Address 0x1 out of bounds>, 0x2b9e30388970 "", \n'\
        '  0x7fff7bd6dfc0 "\\001", 0x0, 0x4059d0 "libberylsettings.so.0", 0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, 0x1 <Address 0x1 out of bounds>, \n'\
        '  0x2b9e303884b8 "", 0x7fff7bd6dff0 "\\001", 0x0, 0x4059c2 "libm.so.6", 0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, \n'\
        '  0x1 <Address 0x1 out of bounds>, 0x2b9e30388000 "", 0x7fff7bd6e020 "\\001", 0x0, 0x405610 "libGL.so.1", \n'\
        '  0x2b9e2ed470cc <Address 0x2b9e2ed470cc out of bounds>, 0x1 <Address 0x1 out of bounds>, 0x2b9e2fdb29b8 "", 0x7fff7bd6e050 "\\001", 0x0, \n'\
        '  0x4055cf "libglib-2.0.so.0", 0x2b9e2ed4448b <Address 0x2b9e2ed4448b out of bounds>, 0x1 <Address 0x1 out of bounds>, 0x2b9e323b2c50 "", \n'\
        '  0xe <Address 0xe out of bounds>, 0x19 <Address 0x19 out of bounds>, 0x7c96f087 <Address 0x7c96f087 out of bounds>, \n'\
        '  0x2b9e2ed448d4 <Address 0x2b9e2ed448d4 out of bounds>, 0x1 <Address 0x1 out of bounds>, 0x7fff7bd6e110 "", 0x7c96f086 <Address 0x7c96f086 out of bounds>, \n'\
        '  0x7fff7bd6e280 "", 0x7fff7bd6e298 "\xb5\xd8\\006", 0x2b9e2ed4448b <Address 0x2b9e2ed4448b out of bounds>, 0x0, 0x2b9e323b2c50 "", \n'\
        '  0xe <Address 0xe out of bounds>, 0x19 <Address 0x19 out of bounds>, 0xd827590 <Address 0xd827590 out of bounds>, \n'\
        '  0x2b9e2ed448d4 <Address 0x2b9e2ed448d4 out of bounds>, 0x0, 0x7fff7bd6e170 "", 0xd827590 <Address 0xd827590 out of bounds>, 0x7fff7bd6e2e0 "\xb0\\v\\2370", \n'\
        '  0x7fff7bd6e2f8 "y:<\\a", 0x2b9e309eaa78 "", 0x0, 0x2b9e327ba150 "\xae\\207:0\\236+", 0x64 <Address 0x64 out of bounds>, \n'\
        '  0x2b9e30a391d6 "D\\213\\205\xb8\xfc\xff\xff\\215C\xdbM\\215e\\001<S\\017\\207\xf5", 0x2b9e309f6bb0 "", 0x2b9effffffff <Address 0x2b9effffffff out of bounds>, \n'\
        '  0x100000000 <Address 0x100000000 out of bounds>, 0x10000040d <Address 0x10000040d out of bounds>, 0x7fff00000001 <Address 0x7fff00000001 out of bounds>, \n'\
        '  0x2b9e30388368 "\xb8\\202\xd5.\\236+", 0x7fff7bd6e330 "\\200\xdd\xd6{\xff\\177", 0x7fff7bd6e2e0 "\xb0\\v\\2370", 0x7fff7bd6e2f8 "y:<\\a", 0x0, 0x7fff7bd6e610 "\xf8\xd1c", \n'\
        '  0x2b9e2ed44af3 <Address 0x2b9e2ed44af3 out of bounds>, 0x200000000 <Address 0x200000000 out of bounds>, 0x2b9e327ba150 "\xae\\207:0\\236+", \n'\
        '  0xffffffff <Address 0xffffffff out of bounds>, 0x2b9e30d37560 "@M\xd30\\236+", 0x2b9e30d34d40 ",*\xb00\\236+", 0x0...}\n'\
        '\tscreenNum = -1\n'\
        '\tnPlugin = 0\n'\
        '\tresult = <value optimized out>\n'\
        '\tclientId = <value optimized out>\n'\
        '\tforceNvidia = 0\n'\
        '\tforceXgl = 0\n'\
        '\tforceAiglx = 0\n'\
        '\toptch = <value optimized out>\n'\
        '\tsopts = "hv"\n'\
        '\tlopts = {{name = 0x4318ef "help", has_arg = 0, flag = 0x0, val = 104}, {name = 0x4318f4 "version", has_arg = 0, flag = 0x0, val = 118}, {\n'\
        '    name = 0x4318fc "display", has_arg = 1, flag = 0x0, val = 1}, {name = 0x4347e9 "screen", has_arg = 1, flag = 0x0, val = 2}, {\n'\
        '    name = 0x4318de "skip-gl-yield", has_arg = 0, flag = 0x63d454, val = 1}, {name = 0x431904 "force-nvidia", has_arg = 0, flag = 0x0, val = 4}, {\n'\
        '    name = 0x431911 "force-xgl", has_arg = 0, flag = 0x0, val = 5}, {name = 0x43191b "force-aiglx", has_arg = 0, flag = 0x0, val = 6}, {\n'\
        '    name = 0x431927 "use-tfp", has_arg = 0, flag = 0x63d45c, val = 0}, {name = 0x43192f "use-copy", has_arg = 0, flag = 0x0, val = 7}, {\n'\
        '    name = 0x431938 "indirect-rendering", has_arg = 0, flag = 0x63d448, val = 1}, {name = 0x43194b "xgl-rendering", has_arg = 0, flag = 0x63d448, val = 0}, {\n'\
        '    name = 0x431959 "strict-binding", has_arg = 0, flag = 0x63d44c, val = 1}, {name = 0x431968 "xgl-binding", has_arg = 0, flag = 0x63d44c, val = 0}, {\n'\
        '    name = 0x431974 "use-cow", has_arg = 0, flag = 0x63d450, val = 1}, {name = 0x43197c "no-cow", has_arg = 0, flag = 0x63d450, val = 0}, {\n'\
        '    name = 0x431983 "no-replace", has_arg = 0, flag = 0x63d1f8, val = 0}, {name = 0x431986 "replace", has_arg = 0, flag = 0x63d1f8, val = 1}, {\n'\
        '    name = 0x43198e "sm-disable", has_arg = 0, flag = 0x63d474, val = 1}, {name = 0x431999 "skip-tests", has_arg = 0, flag = 0x63d464, val = 1}, {\n'\
        '    name = 0x4319a4 "test-only", has_arg = 0, flag = 0x63d470, val = 1}, {name = 0x4319ae "no-context-share", has_arg = 0, flag = 0x63d46c, val = 1}, {\n'\
        '    name = 0x433bec "sm-client-id", has_arg = 1, flag = 0x0, val = 8}, {name = 0x0, has_arg = 0, flag = 0x0, val = 0}}'


    def test_ubuntu3(self):
        import tempfile
        import os
        import shutil
        import datetime
        dirpath=tempfile.mkdtemp()
        try:
            # Test setup
            stacktrace_path = os.path.join(dirpath, "Stacktrace.txt (retraced)")
            with open(stacktrace_path, 'w') as stacktrace_file:
                stacktrace_file.write(self.example_ubuntu_stacktrace3)
            post_path = os.path.join(dirpath, "Post.txt")
            with open(post_path, 'w') as post_file:
                post_file.write(self.example_ubuntu_post3)
            
            # Test crash loader
            crash = Crash.load_from_file(dirpath)
            
            # test that contents are loaded correctly
            assert (isinstance(crash, Crash))
            stacktrace = crash['stacktrace']
            assert (isinstance(stacktrace, Stacktrace))
            assert (isinstance(stacktrace[0], Stackframe))
            assert (stacktrace[0]['depth'] == 0)
            assert (stacktrace[1]['depth'] == 1)
            assert (stacktrace[6]['function'] == 'signal handler called')
            assert (stacktrace[4]['extra'][0] == 'No locals.')
            assert (stacktrace[0]['file'] == '../../src/QuExt.c')
            assert (stacktrace[0]['fileline'] == '46')
            assert (len(stacktrace[0]['extra']) == 2)
            
        finally:
            shutil.rmtree(dirpath)


if __name__ == '__main__':
    unittest.main()