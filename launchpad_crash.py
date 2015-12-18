#!/usr/bin/env python

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

import os, re
import dateutil.parser as dateparser

class LaunchpadFrame(Stackframe):
    
    @classmethod
    def load_from_strings(cls, line, extras=None):
        frame = LaunchpadFrame()
        matched = False
        if not matched:
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(\S+)\s+\(([^\)]*)\)\s+from\s+(\S+)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                frame['dylib'] = match.group(5)
                matched = True
        if not matched:
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(\S+)\s+\(([^\)]*)\)\s+at\s+(\S+)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                frame['file'] = match.group(5)
                matched = True
        if not matched: # Missing address
            match = re.match('^#(\d+)\s+(\S+)\s+\(([^\)]*)\)\s+at\s+(\S+)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['function'] = match.group(2)
                frame['args'] = match.group(3)
                frame['file'] = match.group(4)
                matched = True
        if not matched:
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(\S+)\s+\(([^\)]*)\)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                matched = True
        if not matched: # sometimes args list is cut off?
            match = re.match('^#(\d+)\s+(\S+)\s+in\s+(\S+)\s+\(([^\)]*)\s*$', line)
            if match is not None:
                frame['depth'] = int(match.group(1))
                frame['address'] = match.group(2)
                frame['function'] = match.group(3)
                frame['args'] = match.group(4)
                matched = True
        if extras is not None:
            frame['extra'] = extras
        if matched:
            return frame
        else:
            raise RuntimeError("Couldn't recognize stack frame format: %s" % (line))

class LaunchpadStack(Stacktrace):
    
    @classmethod
    def load_from_file(cls, path):
        with open(path) as stackfile: stacklines = stackfile.readlines()
        stack = LaunchpadStack()
        map(str.rstrip, stacklines)
        extras = []
        prevline = None
        for line in  stacklines:
            if re.match('^\s+', line):
                extras.append(line.rstrip())
            elif re.match('^No locals.', line):
                extras.append(line.rstrip())
            else:
                if prevline is not None:
                    stack.append(LaunchpadFrame.load_from_strings(prevline,extras))
                prevline = line
                extras = []
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
            elif os.path.isfile(os.path.join(path, "Stacktrace.txt")):
                stack_path = os.path.join(path, "Stacktrace.txt")
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

if __name__ == '__main__':
    unittest.main()