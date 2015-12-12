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


import UserDict, UserList

class Stackframe(dict):
  pass
  
class Stacktrace(list):
  """A list which can only contain stackframes..."""
  
  def __init__(self, value=[], **kwargs):
    if isinstance(value, list):
      if len(value) == 0:
        return
      else:
        self.extend(map(Stackframe, value))
    else:
      raise AttributeError
  
  def extend(self, arg):
    for a in arg:
      assert isinstance(a, Stackframe)
    return super(ucSource, self).extend(arg)

  def append(self, *args):
    return self.extend(args)

  def __setitem__(self, index, value):
    for v in value:
      assert isinstance(v, Stackframe)
    return super(Stacktrace, self).__setitem__(index, value)
  
  def __setslice__(self, i, j, seq):
    for v in seq:
      assert isinstance(v, Stackframe)
    return super(Stacktrace, self).__setitem__(i, j, seq)

class Crash(dict):
  
  synonyms = {
    'crash_id': 'database_id', # Mozilla
    'ProblemType' : 'type', # Apport
    'DistroRelease' : 'os', # Apport
    'ProcVersionSignature' : 'os_version', # Apport
    'os_ver' : 'os_version', # Mozilla
    'cpu_arch' : 'cpu', # Mozilla
    'Architecture' : 'cpu', # Apport
    'frames' : 'stacktrace', # Mozilla
  }
  breakapart = {
    'crash_info' : 1, # Mozilla
    'system_info' : 1, # Mozilla
  }

  def __init__(self, *args):
    super(Crash, self).__init__(*args)
    self.normalize()
  
  @classmethod
  def load_from_file(cls, path):
      if os.path.isdir(path):
          raise NotImplementedError()
      else:
          raise NotImplementedError()
  
   
  def __setitem__(self, key, val):
    if key in synonyms:
       super(Crash, self).__setitem__(synonyms[key], val)
    elif key in breakapart:
      if isinstance(val, dict):
        for key2 in val:
          self.__setitem__(key2, val[key2])
      else:
        raise ValueError("Expected a dict!")
    elif key == 'Date': # Apport
      self.__setitem__('date', datetime('val'))
    elif key == 'crashing_thread': # Mozilla
      if (isinstance(val, dict)):
        for key2 in val:
          self.__setitem__(key2, val[key2])
      else:
        super(Crash, self).__setitem__(key, val)
      
  def normalize(self):
    for key in self.keys():
      value = self[value]
      del self[value]
      self.__setitem__(key, value)
      

import unittest
class TestCrash(unittest.TestCase):
    
    # Example from https://bugs.launchpad.net/ubuntu/+source/audacious/+bug/216088
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
        dirpath=tempfile.mkdtemp()
        try:
            # Test setup
            stacktrace_path = os.path.join(dirpath, "Stacktrace.txt")
            with open(stacktrace_path, 'w') as stacktrace_file:
                stacktrace_file.write(self.example_ubuntu_stacktrace)
            
            # Test crash loader
            crash = Crash.load_from_file(dirpath)
            
            # TODO: test that contents are loaded correctly
            
        finally:
            shutil.rmtree(dirpath)
            
if __name__ == '__main__':
    unittest.main()