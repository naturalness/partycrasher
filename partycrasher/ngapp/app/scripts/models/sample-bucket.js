angular.module('PartyCrasherApp')
.constant('SAMPLE_BUCKET', {
  'href': 'http://localhost:49263/ubuntu/buckets/4.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
  'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
  'project': 'ubuntu',
  'threshold': '4.0',
  'top_reports': [
    {
      'ApportVersion': '2.12-0ubuntu3',
      'ExecutablePath': '/usr/bin/compiz',
      'InstallationDate': 'Installed on 2013-02-05 (194 days ago)',
      'InstallationMedia': 'Ubuntu 12.10 "Quantal Quetzal" - Release amd64 (20121017.5)',
      'MarkForUpload': 'True',
      'NonfreeKernelModules': 'nvidia',
      'Package': 'unity 7.1.0+13.10.20130816.3-0ubuntu1',
      'ProcCmdline': 'compiz',
      'ProcEnviron': ' LANGUAGE=en_AU:en\n PATH=(custom, user)\n XDG_RUNTIME_DIR=<set>\n LANG=en_AU.UTF-8\n SHELL=/bin/bash\n',
      'SegvAnalysis': ' Segfault happened at: 0x7fd116c07289 <_int_free+217>:?mov    0x8(%rdx),%esi\n PC (0x7fd116c07289) ok\n source "0x8(%rdx)" (0x100000007) not located in a known VMA region (needed readable region)!\n destination "%esi" ok\n',
      'SegvReason': 'reading unknown VMA',
      'Signal': '11',
      'SourcePackage': 'unity',
      'Title': 'compiz crashed with SIGSEGV in _int_free()',
      'Uname': 'Linux 3.11.0-2-generic x86_64',
      'UpgradeStatus': 'Upgraded to saucy on 2013-08-13 (5 days ago)',
      'UserGroups': 'adm cdrom dip games lpadmin plugdev sambashare sudo vboxusers',
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/1.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '1.0',
          'total': null
        },
        '1.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/1.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '1.5',
          'total': null
        },
        '2.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/2.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '2.0',
          'total': null
        },
        '2.75': {
          'href': 'http://localhost:49263/ubuntu/buckets/2.75/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '2.75',
          'total': null
        },
        '3.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.0',
          'total': null
        },
        '3.25': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.25/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.25',
          'total': null
        },
        '3.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.5',
          'total': null
        },
        '3.75': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.75/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.75',
          'total': null
        },
        '4.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/4.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '4.0',
          'total': null
        },
        '4.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/4.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '4.5',
          'total': null
        },
        '5.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/5.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '5.0',
          'total': null
        },
        '5.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/5.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '5.5',
          'total': null
        },
        '6.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/6.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '6.0',
          'total': null
        },
        '7.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/7.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '7.0',
          'total': null
        },
        'top_match': {
          'href': 'http://localhost:49263/ubuntu/reports/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'report_id': 'ubuntu:14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'score': 7.442582
        }
      },
      'cpu': 'amd64',
      'database_id': 'ubuntu:18d7a97f-5574-407e-9439-63263fc938c8',
      'date': '2013-08-19T08:58:36',
      'extra': 'I was searching for an ODT document, and accidentally opened the preview for it, but then when I went the close the preview, Unity froze, and then after about 5 secs, crashed and restarted.\n\nStacktraceTop:  _int_free (av=0x7fd116f47740 <main_arena>, p=0x7d9da60, have_lock=0) at malloc.c:3832\n XDestroyRegion () from /usr/lib/x86_64-linux-gnu/libX11.so.6\n CompRegion::intersects(CompRegion const&) const () from /usr/lib/libcompiz_core.so.ABI-20130125\n unity::UnityScreen::compizDamageNux(CompRegion const&) () from /usr/lib/compiz/libunityshell.so\n unity::UnityScreen::preparePaint(int) () from /usr/lib/compiz/libunityshell.so\n\n',
      'href': 'http://localhost:49263/ubuntu/reports/18d7a97f-5574-407e-9439-63263fc938c8',
      'os': 'Ubuntu 13.10',
      'os_version': 'Ubuntu 3.11.0-2.5-generic 3.11.0-rc5',
      'project': 'ubuntu',
      'stacktrace': [
        {
          'args': 'av=0x7fd116f47740 <main_arena>, p=0x7d9da60, have_lock=0',
          'depth': 0,
          'extra': [
            '#0  _int_free (av=0x7fd116f47740 <main_arena>, p=0x7d9da60, have_lock=0) at malloc.c:3832',
            '        idx = 1',
            '        fd = <optimized out>',
            '        old = 0xffffffff',
            '        old_idx = <optimized out>',
            '        size = <optimized out>',
            '        fb = 0x7fd116f47750 <main_arena+16>',
            '        nextchunk = <optimized out>',
            '        nextsize = <optimized out>',
            '        nextinuse = <optimized out>',
            '        prevsize = <optimized out>',
            '        bck = <optimized out>',
            '        fwd = <optimized out>',
            '        errstr = 0x0',
            '        locked = 0',
            '        __func__ = "_int_free"'
          ],
          'file': 'malloc.c:3832',
          'function': '_int_free'
        },
        {
          'address': '0x00007fd1164574c5',
          'args': 'r=0x7d9da70',
          'depth': 1,
          'extra': [
            '#1  0x00007fd1164574c5 in XDestroyRegion (r=0x7d9da70) at ../../src/Region.c:288',
            'No locals.'
          ],
          'file': '../../src/Region.c:288',
          'function': 'XDestroyRegion'
        },
        {
          'address': '0x00007fd1174f5c85',
          'args': '',
          'depth': 2,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/libcompiz_core.so.ABI-20130125',
          'extra': [
            '#2  0x00007fd1174f5c85 in CompRegion::intersected(CompRect const&) const () from /tmp/apport_sandbox_HssgYB/usr/lib/libcompiz_core.so.ABI-20130125',
            'No symbol table info available.'
          ],
          'function': 'CompRegion::intersected(CompRect const&) const'
        },
        {
          'address': '0x00007fd0f8432280',
          'args': '',
          'depth': 3,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
          'extra': [
            '#3  0x00007fd0f8432280 in unity::UnityScreen::compizDamageNux(CompRegion const&) () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
            'No symbol table info available.'
          ],
          'function': 'unity::UnityScreen::compizDamageNux(CompRegion const&)'
        },
        {
          'address': '0x00007fd0f8432884',
          'args': '',
          'depth': 4,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
          'extra': [
            '#4  0x00007fd0f8432884 in unity::UnityScreen::preparePaint(int) () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
            'No symbol table info available.'
          ],
          'function': 'unity::UnityScreen::preparePaint(int)'
        },
        {
          'address': '0x00007fd110194f25',
          'args': '',
          'depth': 5,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
          'extra': [
            '#5  0x00007fd110194f25 in ?? () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x00000000020a77e0',
          'args': '',
          'depth': 6,
          'extra': [
            '#6  0x00000000020a77e0 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x0000000002122670',
          'args': '',
          'depth': 7,
          'extra': [
            '#7  0x0000000002122670 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x0000000007ea80b0',
          'args': '',
          'depth': 8,
          'extra': [
            '#8  0x0000000007ea80b0 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x00007fd1101966b8',
          'args': '',
          'depth': 9,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
          'extra': [
            '#9  0x00007fd1101966b8 in CompositeScreen::compositingActive() () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
            'No symbol table info available.'
          ],
          'function': 'CompositeScreen::compositingActive()'
        },
        {
          'address': '0x0000000000000000',
          'args': '',
          'depth': 10,
          'extra': [
            '#10 0x0000000000000000 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        }
      ],
      'type': 'Crash'
    },
    {
      'ApportVersion': '2.12-0ubuntu3',
      'ExecutablePath': '/usr/bin/compiz',
      'InstallationDate': 'Installed on 2013-02-05 (194 days ago)',
      'InstallationMedia': 'Ubuntu 12.10 "Quantal Quetzal" - Release amd64 (20121017.5)',
      'MarkForUpload': 'True',
      'NonfreeKernelModules': 'nvidia',
      'Package': 'unity 7.1.0+13.10.20130816.3-0ubuntu1',
      'ProcCmdline': 'compiz',
      'ProcEnviron': ' LANGUAGE=en_AU:en\n PATH=(custom, user)\n XDG_RUNTIME_DIR=<set>\n LANG=en_AU.UTF-8\n SHELL=/bin/bash\n',
      'SegvAnalysis': ' Segfault happened at: 0x7fd116c07289 <_int_free+217>:?mov    0x8(%rdx),%esi\n PC (0x7fd116c07289) ok\n source "0x8(%rdx)" (0x100000007) not located in a known VMA region (needed readable region)!\n destination "%esi" ok\n',
      'SegvReason': 'reading unknown VMA',
      'Signal': '11',
      'SourcePackage': 'unity',
      'Title': 'compiz crashed with SIGSEGV in _int_free()',
      'Uname': 'Linux 3.11.0-2-generic x86_64',
      'UpgradeStatus': 'Upgraded to saucy on 2013-08-13 (5 days ago)',
      'UserGroups': 'adm cdrom dip games lpadmin plugdev sambashare sudo vboxusers',
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/1.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '1.0',
          'total': null
        },
        '1.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/1.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '1.5',
          'total': null
        },
        '2.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/2.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '2.0',
          'total': null
        },
        '2.75': {
          'href': 'http://localhost:49263/ubuntu/buckets/2.75/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '2.75',
          'total': null
        },
        '3.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.0',
          'total': null
        },
        '3.25': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.25/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.25',
          'total': null
        },
        '3.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.5',
          'total': null
        },
        '3.75': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.75/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.75',
          'total': null
        },
        '4.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/4.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '4.0',
          'total': null
        },
        '4.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/4.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '4.5',
          'total': null
        },
        '5.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/5.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '5.0',
          'total': null
        },
        '5.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/5.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '5.5',
          'total': null
        },
        '6.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/6.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '6.0',
          'total': null
        },
        '7.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/7.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '7.0',
          'total': null
        },
        'top_match': null
      },
      'cpu': 'amd64',
      'database_id': 'ubuntu:14fcce75-2b56-4976-bc55-d7d058bcea7b',
      'date': '2013-08-19T08:58:36',
      'extra': 'I was searching for an ODT document, and accidentally opened the preview for it, but then when I went the close the preview, Unity froze, and then after about 5 secs, crashed and restarted.\n\nStacktraceTop:  _int_free (av=0x7fd116f47740 <main_arena>, p=0x7d9da60, have_lock=0) at malloc.c:3832\n XDestroyRegion () from /usr/lib/x86_64-linux-gnu/libX11.so.6\n CompRegion::intersects(CompRegion const&) const () from /usr/lib/libcompiz_core.so.ABI-20130125\n unity::UnityScreen::compizDamageNux(CompRegion const&) () from /usr/lib/compiz/libunityshell.so\n unity::UnityScreen::preparePaint(int) () from /usr/lib/compiz/libunityshell.so\n\n',
      'href': 'http://localhost:49263/ubuntu/reports/14fcce75-2b56-4976-bc55-d7d058bcea7b',
      'os': 'Ubuntu 13.10',
      'os_version': 'Ubuntu 3.11.0-2.5-generic 3.11.0-rc5',
      'project': 'ubuntu',
      'stacktrace': [
        {
          'args': 'av=0x7fd116f47740 <main_arena>, p=0x7d9da60, have_lock=0',
          'depth': 0,
          'extra': [
            '#0  _int_free (av=0x7fd116f47740 <main_arena>, p=0x7d9da60, have_lock=0) at malloc.c:3832',
            '        idx = 1',
            '        fd = <optimized out>',
            '        old = 0xffffffff',
            '        old_idx = <optimized out>',
            '        size = <optimized out>',
            '        fb = 0x7fd116f47750 <main_arena+16>',
            '        nextchunk = <optimized out>',
            '        nextsize = <optimized out>',
            '        nextinuse = <optimized out>',
            '        prevsize = <optimized out>',
            '        bck = <optimized out>',
            '        fwd = <optimized out>',
            '        errstr = 0x0',
            '        locked = 0',
            '        __func__ = "_int_free"'
          ],
          'file': 'malloc.c:3832',
          'function': '_int_free'
        },
        {
          'address': '0x00007fd1164574c5',
          'args': 'r=0x7d9da70',
          'depth': 1,
          'extra': [
            '#1  0x00007fd1164574c5 in XDestroyRegion (r=0x7d9da70) at ../../src/Region.c:288',
            'No locals.'
          ],
          'file': '../../src/Region.c:288',
          'function': 'XDestroyRegion'
        },
        {
          'address': '0x00007fd1174f5c85',
          'args': '',
          'depth': 2,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/libcompiz_core.so.ABI-20130125',
          'extra': [
            '#2  0x00007fd1174f5c85 in CompRegion::intersected(CompRect const&) const () from /tmp/apport_sandbox_HssgYB/usr/lib/libcompiz_core.so.ABI-20130125',
            'No symbol table info available.'
          ],
          'function': 'CompRegion::intersected(CompRect const&) const'
        },
        {
          'address': '0x00007fd0f8432280',
          'args': '',
          'depth': 3,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
          'extra': [
            '#3  0x00007fd0f8432280 in unity::UnityScreen::compizDamageNux(CompRegion const&) () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
            'No symbol table info available.'
          ],
          'function': 'unity::UnityScreen::compizDamageNux(CompRegion const&)'
        },
        {
          'address': '0x00007fd0f8432884',
          'args': '',
          'depth': 4,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
          'extra': [
            '#4  0x00007fd0f8432884 in unity::UnityScreen::preparePaint(int) () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libunityshell.so',
            'No symbol table info available.'
          ],
          'function': 'unity::UnityScreen::preparePaint(int)'
        },
        {
          'address': '0x00007fd110194f25',
          'args': '',
          'depth': 5,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
          'extra': [
            '#5  0x00007fd110194f25 in ?? () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x00000000020a77e0',
          'args': '',
          'depth': 6,
          'extra': [
            '#6  0x00000000020a77e0 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x0000000002122670',
          'args': '',
          'depth': 7,
          'extra': [
            '#7  0x0000000002122670 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x0000000007ea80b0',
          'args': '',
          'depth': 8,
          'extra': [
            '#8  0x0000000007ea80b0 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0x00007fd1101966b8',
          'args': '',
          'depth': 9,
          'dylib': '/tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
          'extra': [
            '#9  0x00007fd1101966b8 in CompositeScreen::compositingActive() () from /tmp/apport_sandbox_HssgYB/usr/lib/compiz/libcomposite.so',
            'No symbol table info available.'
          ],
          'function': 'CompositeScreen::compositingActive()'
        },
        {
          'address': '0x0000000000000000',
          'args': '',
          'depth': 10,
          'extra': [
            '#10 0x0000000000000000 in ?? ()',
            'No symbol table info available.'
          ],
          'function': null
        }
      ],
      'type': 'Crash'
    },
    {
      'ApportVersion': '2.4-0ubuntu5',
      'ExecutablePath': '/usr/lib/i386-linux-gnu/colord/colord-sane',
      'NonfreeKernelModules': 'nvidia',
      'Package': 'colord 0.1.21-1',
      'ProcCmdline': '/usr/lib/i386-linux-gnu/colord/colord-sane',
      'ProcEnviron': ' \n',
      'SegvAnalysis': ' Segfault happened at: 0xb54dca12:?mov    (%edx),%esi\n PC (0xb54dca12) ok\n source "(%edx)" (0x625f6d65) not located in a known VMA region (needed readable region)!\n destination "%esi" ok\n',
      'SegvReason': 'reading unknown VMA',
      'Signal': '11',
      'SourcePackage': 'colord',
      'Title': 'colord-sane crashed with SIGSEGV',
      'Uname': 'Linux 3.5.0-6-generic i686',
      'UpgradeStatus': 'No upgrade log present (probably fresh install)',
      'UserGroups': 'scanner',
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/1.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '1.0',
          'total': null
        },
        '1.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/1.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '1.5',
          'total': null
        },
        '2.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/2.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '2.0',
          'total': null
        },
        '2.75': {
          'href': 'http://localhost:49263/ubuntu/buckets/2.75/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '2.75',
          'total': null
        },
        '3.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.0',
          'total': null
        },
        '3.25': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.25/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.25',
          'total': null
        },
        '3.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.5',
          'total': null
        },
        '3.75': {
          'href': 'http://localhost:49263/ubuntu/buckets/3.75/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '3.75',
          'total': null
        },
        '4.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/4.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '4.0',
          'total': null
        },
        '4.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/4.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '4.5',
          'total': null
        },
        '5.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/5.0/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '5.0',
          'total': null
        },
        '5.5': {
          'href': 'http://localhost:49263/ubuntu/buckets/5.5/14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'id': '14fcce75-2b56-4976-bc55-d7d058bcea7b',
          'project': 'ubuntu',
          'threshold': '5.5',
          'total': null
        },
        '6.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/6.0/c2944bb6-0ebb-4570-9025-e91f5ab0080b',
          'id': 'c2944bb6-0ebb-4570-9025-e91f5ab0080b',
          'project': 'ubuntu',
          'threshold': '6.0',
          'total': null
        },
        '7.0': {
          'href': 'http://localhost:49263/ubuntu/buckets/7.0/c2944bb6-0ebb-4570-9025-e91f5ab0080b',
          'id': 'c2944bb6-0ebb-4570-9025-e91f5ab0080b',
          'project': 'ubuntu',
          'threshold': '7.0',
          'total': null
        },
        'top_match': {
          'href': 'http://localhost:49263/ubuntu/reports/18d7a97f-5574-407e-9439-63263fc938c8',
          'project': 'ubuntu',
          'report_id': 'ubuntu:18d7a97f-5574-407e-9439-63263fc938c8',
          'score': 5.797851
        }
      },
      'cpu': 'i386',
      'database_id': 'ubuntu:c2944bb6-0ebb-4570-9025-e91f5ab0080b',
      'date': '2012-07-26T07:20:50',
      'extra': 'crash at login time on quantal i386 logged as gnome-classic with nvidia-current graphic\n\nStacktraceTop:  ?? () from /lib/i386-linux-gnu/libdbus-1.so.3\n ?? () from /lib/i386-linux-gnu/libdbus-1.so.3\n ?? () from /lib/i386-linux-gnu/libdbus-1.so.3\n ?? () from /lib/i386-linux-gnu/libdbus-1.so.3\n ?? () from /lib/i386-linux-gnu/libdbus-1.so.3\n\n',
      'href': 'http://localhost:49263/ubuntu/reports/c2944bb6-0ebb-4570-9025-e91f5ab0080b',
      'os': 'Ubuntu 12.10',
      'os_version': 'Ubuntu 3.5.0-6.6-generic 3.5.0',
      'project': 'ubuntu',
      'stacktrace': [
        {
          'args': 'link=0x9992508, before_this_link=0x625f6d65, list=0x998f6fc',
          'depth': 0,
          'extra': [
            '#0  link_before (link=0x9992508, before_this_link=0x625f6d65, list=0x998f6fc) at ../../dbus/dbus-list.c:120',
            'No locals.'
          ],
          'file': '../../dbus/dbus-list.c:120',
          'function': 'link_before'
        },
        {
          'args': 'list=0x998f6fc, link=0x9992508',
          'depth': 1,
          'extra': [
            '#1  _dbus_list_prepend_link (list=0x998f6fc, link=0x9992508) at ../../dbus/dbus-list.c:313',
            'No locals.'
          ],
          'file': '../../dbus/dbus-list.c:313',
          'function': '_dbus_list_prepend_link'
        },
        {
          'address': '0xb54dca6a',
          'args': 'list=0x998f6fc, link=0x9992508',
          'depth': 2,
          'extra': [
            '#2  0xb54dca6a in _dbus_list_append_link (list=0x998f6fc, link=0x9992508) at ../../dbus/dbus-list.c:295',
            'No locals.'
          ],
          'file': '../../dbus/dbus-list.c:295',
          'function': '_dbus_list_append_link'
        },
        {
          'address': '0xb54cb568',
          'args': 'message=0x998f6a0, link=0x9992508',
          'depth': 3,
          'extra': [
            '#3  0xb54cb568 in _dbus_message_add_counter_link (message=0x998f6a0, link=0x9992508) at ../../dbus/dbus-message.c:249',
            'No locals.'
          ],
          'file': '../../dbus/dbus-message.c:249',
          'function': '_dbus_message_add_counter_link'
        },
        {
          'address': '0xb54cb606',
          'args': 'message=0x998f6a0, counter=0x9997090',
          'depth': 4,
          'extra': [
            '#4  0xb54cb606 in _dbus_message_add_counter (message=0x998f6a0, counter=0x9997090) at ../../dbus/dbus-message.c:278',
            '        link = 0x9992508'
          ],
          'file': '../../dbus/dbus-message.c:278',
          'function': '_dbus_message_add_counter'
        },
        {
          'address': '0xb54d8be7',
          'args': 'transport=0x9996d30',
          'depth': 5,
          'extra': [
            '#5  0xb54d8be7 in _dbus_transport_queue_messages (transport=0x9996d30) at ../../dbus/dbus-transport.c:1138',
            '        message = <optimized out>',
            '        link = 0x99924f0',
            '        status = <optimized out>'
          ],
          'file': '../../dbus/dbus-transport.c:1138',
          'function': '_dbus_transport_queue_messages'
        },
        {
          'address': '0xb54d9827',
          'args': 'transport=0x9996d30',
          'depth': 6,
          'extra': [
            '#6  0xb54d9827 in do_reading (transport=0x9996d30) at ../../dbus/dbus-transport-socket.c:851',
            '        buffer = 0x9996e24',
            '        bytes_read = 260',
            '        total = 260',
            '        oom = <optimized out>'
          ],
          'file': '../../dbus/dbus-transport-socket.c:851',
          'function': 'do_reading'
        },
        {
          'address': '0xb54d9f17',
          'args': 'transport=0x9996d30',
          'depth': 7,
          'extra': [
            '#7  0xb54d9f17 in do_reading (transport=0x9996d30) at ../../dbus/dbus-transport-socket.c:706',
            '        socket_transport = 0x9996d30'
          ],
          'file': '../../dbus/dbus-transport-socket.c:706',
          'function': 'do_reading'
        },
        {
          'args': 'transport=0x9996d30, flags=6, timeout_milliseconds=25000',
          'depth': 8,
          'extra': [
            '#8  socket_do_iteration (transport=0x9996d30, flags=6, timeout_milliseconds=25000) at ../../dbus/dbus-transport-socket.c:1162',
            '        need_read = 1',
            '        need_write = 0',
            '        authentication_completed = 0',
            '        socket_transport = 0x9996d30',
            '        poll_fd = {fd = 13, events = 1, revents = 1}',
            '        poll_res = <optimized out>',
            '        poll_timeout = <optimized out>'
          ],
          'file': '../../dbus/dbus-transport-socket.c:1162',
          'function': 'socket_do_iteration'
        },
        {
          'address': '0xb54d890d',
          'args': 'transport=0x9996d30, flags=6, timeout_milliseconds=25000',
          'depth': 9,
          'extra': [
            '#9  0xb54d890d in _dbus_transport_do_iteration (transport=0x9996d30, flags=6, timeout_milliseconds=25000) at ../../dbus/dbus-transport.c:974',
            'No locals.'
          ],
          'file': '../../dbus/dbus-transport.c:974',
          'function': '_dbus_transport_do_iteration'
        },
        {
          'address': '0xb54c0614',
          'args': 'connection=0x99971a8, pending=0x9996c58, flags=6, timeout_milliseconds=25000',
          'depth': 10,
          'extra': [
            '#10 0xb54c0614 in _dbus_connection_do_iteration_unlocked (connection=0x99971a8, pending=0x9996c58, flags=6, timeout_milliseconds=25000) at ../../dbus/dbus-connection.c:1215',
            'No locals.'
          ],
          'file': '../../dbus/dbus-connection.c:1215',
          'function': '_dbus_connection_do_iteration_unlocked'
        },
        {
          'address': '0xb54c1b14',
          'args': 'pending=0x9996c58',
          'depth': 11,
          'extra': [
            '#11 0xb54c1b14 in _dbus_connection_block_pending_call (pending=0x9996c58) at ../../dbus/dbus-connection.c:2404',
            '        start_tv_sec = 39',
            '        start_tv_usec = 526607',
            '        tv_sec = 161049688',
            '        tv_usec = -1079918980',
            '        status = <optimized out>',
            '        connection = 0x99971a8',
            '        client_serial = 1',
            '        timeout = 0x9997260',
            '        timeout_milliseconds = 25000',
            '        elapsed_milliseconds = <optimized out>'
          ],
          'file': '../../dbus/dbus-connection.c:2404',
          'function': '_dbus_connection_block_pending_call'
        },
        {
          'address': '0xb54d237f',
          'args': 'pending=0x9996c58',
          'depth': 12,
          'extra': [
            '#12 0xb54d237f in dbus_pending_call_block (pending=0x9996c58) at ../../dbus/dbus-pending-call.c:705',
            '        __FUNCTION__ = "dbus_pending_call_block"'
          ],
          'file': '../../dbus/dbus-pending-call.c:705',
          'function': 'dbus_pending_call_block'
        },
        {
          'address': '0xb54c0f4b',
          'args': 'connection=0x99971a8, message=0x998fa00, timeout_milliseconds=-1, error=0xb4cb116c',
          'depth': 13,
          'extra': [
            '#13 0xb54c0f4b in dbus_connection_send_with_reply_and_block (connection=0x99971a8, message=0x998fa00, timeout_milliseconds=-1, error=0xb4cb116c) at ../../dbus/dbus-connection.c:3515',
            '        reply = <optimized out>',
            '        pending = 0x9996c58',
            '        __FUNCTION__ = "dbus_connection_send_with_reply_and_block"'
          ],
          'file': '../../dbus/dbus-connection.c:3515',
          'function': 'dbus_connection_send_with_reply_and_block'
        },
        {
          'address': '0xb54bba34',
          'args': 'connection=0x99971a8, error=0xb4cb116c',
          'depth': 14,
          'extra': [
            '#14 0xb54bba34 in dbus_bus_register (connection=0x99971a8, error=0xb4cb116c) at ../../dbus/dbus-bus.c:698',
            '        message = <optimized out>',
            '        reply = <optimized out>',
            '        name = <optimized out>',
            '        bd = <optimized out>',
            '        retval = 0',
            '        __FUNCTION__ = "dbus_bus_register"'
          ],
          'file': '../../dbus/dbus-bus.c:698',
          'function': 'dbus_bus_register'
        },
        {
          'address': '0xb54bbd5f',
          'args': 'type=DBUS_BUS_SYSTEM, private=0, error=0xb4cb116c',
          'depth': 15,
          'extra': [
            '#15 0xb54bbd5f in internal_bus_get (type=DBUS_BUS_SYSTEM, private=0, error=0xb4cb116c) at ../../dbus/dbus-bus.c:491',
            '        address = <optimized out>',
            '        connection = 0x99971a8',
            '        bd = <optimized out>',
            '        address_type = DBUS_BUS_SYSTEM',
            '        __FUNCTION__ = "internal_bus_get"'
          ],
          'file': '../../dbus/dbus-bus.c:491',
          'function': 'internal_bus_get'
        },
        {
          'address': '0xb4c9166c',
          'args': '',
          'depth': 16,
          'dylib': '/tmp/tmpoqDoof/usr/lib/sane/libsane-hpaio.so.1',
          'extra': [
            '#16 0xb4c9166c in ?? () from /tmp/tmpoqDoof/usr/lib/sane/libsane-hpaio.so.1',
            'No symbol table info available.'
          ],
          'function': null
        },
        {
          'address': '0xb4c8da77',
          'args': '',
          'depth': 17,
          'dylib': '/tmp/tmpoqDoof/usr/lib/sane/libsane-hpaio.so.1',
          'extra': [
            '#17 0xb4c8da77 in sane_hpaio_init () from /tmp/tmpoqDoof/usr/lib/sane/libsane-hpaio.so.1',
            'No symbol table info available.'
          ],
          'function': 'sane_hpaio_init'
        },
        {
          'address': '0xb777b492',
          'args': 'be=be@entry=0x995a700',
          'depth': 18,
          'extra': [
            '#18 0xb777b492 in init (be=be@entry=0x995a700) at dll.c:612',
            '        status = <optimized out>',
            '        version = -1216876556'
          ],
          'file': 'dll.c:612',
          'function': 'init'
        },
        {
          'address': '0xb777bf40',
          'args': 'device_list=device_list@entry=0xbfa1c0ec, local_only=local_only@entry=1',
          'depth': 19,
          'extra': [
            '#19 0xb777bf40 in sane_dll_get_devices (device_list=device_list@entry=0xbfa1c0ec, local_only=local_only@entry=1) at dll.c:1053',
            '        be_list = 0xb55421d8',
            '        be = 0x995a700',
            '        status = <optimized out>',
            '        full_name = <optimized out>',
            '        i = <optimized out>',
            '        num_devs = <optimized out>',
            '        len = <optimized out>'
          ],
          'file': 'dll.c:1053',
          'function': 'sane_dll_get_devices'
        },
        {
          'address': '0xb77795f3',
          'args': 'dl=dl@entry=0xbfa1c0ec, local=local@entry=1',
          'depth': 20,
          'extra': [
            '#20 0xb77795f3 in sane_get_devices (dl=dl@entry=0xbfa1c0ec, local=local@entry=1) at dll-s.c:17',
            'No locals.'
          ],
          'file': 'dll-s.c:17',
          'function': 'sane_get_devices'
        },
        {
          'address': '0x08049dc9',
          'args': 'priv=priv@entry=0x994d6f0',
          'depth': 21,
          'extra': [
            '#21 0x08049dc9 in cd_sane_client_refresh (priv=priv@entry=0x994d6f0) at cd-main.c:303',
            '        tmp = <optimized out>',
            '        device_list = 0x0',
            '        i = <optimized out>',
            '        status = <optimized out>'
          ],
          'file': 'cd-main.c:303',
          'function': 'cd_sane_client_refresh'
        },
        {
          'address': '0x0804a1c5',
          'args': 'source_object=0x9954990, res=0x9957950, user_data=user_data@entry=0x994d6f0',
          'depth': 22,
          'extra': [
            '#22 0x0804a1c5 in cd_main_colord_connect_cb (source_object=0x9954990, res=0x9957950, user_data=user_data@entry=0x994d6f0) at cd-main.c:446',
            '        priv = 0x994d6f0',
            '        ret = <optimized out>',
            '        error = 0x0'
          ],
          'file': 'cd-main.c:446',
          'function': 'cd_main_colord_connect_cb'
        },
        {
          'address': '0xb767b1f0',
          'args': 'simple=0x9957950',
          'depth': 23,
          'extra': [
            '#23 0xb767b1f0 in g_simple_async_result_complete (simple=0x9957950) at /build/buildd/glib2.0-2.33.6/./gio/gsimpleasyncresult.c:775',
            '        current_source = <optimized out>',
            '        current_context = <optimized out>',
            '        __PRETTY_FUNCTION__ = "g_simple_async_result_complete"'
          ],
          'file': '/build/buildd/glib2.0-2.33.6/./gio/gsimpleasyncresult.c:775',
          'function': 'g_simple_async_result_complete'
        },
        {
          'address': '0xb767b31c',
          'args': 'data=data@entry=0x9957950',
          'depth': 24,
          'extra': [
            '#24 0xb767b31c in complete_in_idle_cb (data=data@entry=0x9957950) at /build/buildd/glib2.0-2.33.6/./gio/gsimpleasyncresult.c:787',
            '        simple = <optimized out>'
          ],
          'file': '/build/buildd/glib2.0-2.33.6/./gio/gsimpleasyncresult.c:787',
          'function': 'complete_in_idle_cb'
        },
        {
          'address': '0xb75071c0',
          'args': 'source=source@entry=0x995b368, callback=0xb767b2f0 <complete_in_idle_cb>, user_data=0x9957950',
          'depth': 25,
          'extra': [
            '#25 0xb75071c0 in g_idle_dispatch (source=source@entry=0x995b368, callback=0xb767b2f0 <complete_in_idle_cb>, user_data=0x9957950) at /build/buildd/glib2.0-2.33.6/./glib/gmain.c:4781',
            'No locals.'
          ],
          'file': '/build/buildd/glib2.0-2.33.6/./glib/gmain.c:4781',
          'function': 'g_idle_dispatch'
        },
        {
          'address': '0xb7509ef3',
          'args': 'context=0x994d738',
          'depth': 26,
          'extra': [
            '#26 0xb7509ef3 in g_main_dispatch (context=0x994d738) at /build/buildd/glib2.0-2.33.6/./glib/gmain.c:2691',
            '        dispatch = 0xb75071a0 <g_idle_dispatch>',
            '        was_in_call = 0',
            '        user_data = 0x9957950',
            '        callback = 0xb767b2f0 <complete_in_idle_cb>',
            '        cb_funcs = 0xb75bd4f8',
            '        cb_data = 0x995c6a8',
            '        current_source_link = {data = 0x995b368, next = 0x0}',
            '        need_destroy = <optimized out>',
            '        source = 0x995b368',
            '        current = 0x994c8a0',
            '        i = <optimized out>'
          ],
          'file': '/build/buildd/glib2.0-2.33.6/./glib/gmain.c:2691',
          'function': 'g_main_dispatch'
        },
        {
          'args': 'context=context@entry=0x994d738',
          'depth': 27,
          'extra': [
            '#27 g_main_context_dispatch (context=context@entry=0x994d738) at /build/buildd/glib2.0-2.33.6/./glib/gmain.c:3195',
            'No locals.'
          ],
          'file': '/build/buildd/glib2.0-2.33.6/./glib/gmain.c:3195',
          'function': 'g_main_context_dispatch'
        },
        {
          'address': '0xb750a290',
          'args': 'context=0x994d738, block=block@entry=1, dispatch=dispatch@entry=1, self=<error reading variable: Unhandled dwarf expression opcode 0xfa>',
          'depth': 28,
          'extra': [
            '#28 0xb750a290 in g_main_context_iterate (context=0x994d738, block=block@entry=1, dispatch=dispatch@entry=1, self=<error reading variable: Unhandled dwarf expression opcode 0xfa>) at /build/buildd/glib2.0-2.33.6/./glib/gmain.c:3266',
            '        max_priority = 0',
            '        timeout = 0',
            '        some_ready = 1',
            '        nfds = 2',
            '        allocated_nfds = <optimized out>',
            '        fds = <optimized out>'
          ],
          'file': '/build/buildd/glib2.0-2.33.6/./glib/gmain.c:3266',
          'function': 'g_main_context_iterate'
        },
        {
          'address': '0xb750a6eb',
          'args': 'loop=0x994d6d0',
          'depth': 29,
          'extra': [
            '#29 0xb750a6eb in g_main_loop_run (loop=0x994d6d0) at /build/buildd/glib2.0-2.33.6/./glib/gmain.c:3460',
            '        __PRETTY_FUNCTION__ = "g_main_loop_run"'
          ],
          'file': '/build/buildd/glib2.0-2.33.6/./glib/gmain.c:3460',
          'function': 'g_main_loop_run'
        },
        {
          'address': '0x080497d4',
          'args': 'argc=1, argv=0xbfa1c3f4',
          'depth': 30,
          'extra': [
            '#30 0x080497d4 in main (argc=1, argv=0xbfa1c3f4) at cd-main.c:617',
            '        priv = 0x994d6f0',
            '        immediate_exit = 0',
            '        timed_exit = 0',
            '        error = 0x0',
            '        context = <optimized out>',
            '        retval = 1',
            "        options = {{long_name = 0x804a609 \"timed-exit\", short_name = 0 '\\000', flags = 0, arg = G_OPTION_ARG_NONE, arg_data = 0xbfa1c2e0, description = 0x804a614 \"Exit after a small delay\", arg_description = 0x0}, {long_name = 0x804a62d \"immediate-exit\", short_name = 0 '\\000', flags = 0, arg = G_OPTION_ARG_NONE, arg_data = 0xbfa1c2dc, description = 0x804a6e4 \"Exit after the engine has loaded\", arg_description = 0x0}, {long_name = 0x0, short_name = 0 '\\000', flags = 0, arg = G_OPTION_ARG_NONE, arg_data = 0x0, description = 0x0, arg_description = 0x0}}"
          ],
          'file': 'cd-main.c:617',
          'function': 'main'
        }
      ],
      'type': 'Crash'
    }
  ],
  'total': 3
});
