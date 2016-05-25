angular.module('PartyCrasherApp')
.constant('SAMPLE_BUCKET', {
  'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
  'id': 'Ubuntu:launchpad:0000139026', 
  'project': 'Ubuntu', 
  'threshold': '4.0', 
  'top_reports': [
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'fglrx', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/techno', 
      'ProcEnviron': ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=de_DE.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux Schrott 2.6.22-13-generic #1 SMP Thu Oct 4 17:18:44 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000147400', 
          'id': 'Ubuntu:launchpad:0000147400', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000150570', 
          'id': 'Ubuntu:launchpad:0000150570', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000150522', 
          'score': 6.283423
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000150570', 
      'date': '2007-10-08T07:33:56', 
      'extra': 'Strigidaemon often crashes on startup.\n\nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\n', 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbfd7bb3c, field=0x730a001c', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbfd7bb3c, field=0x730a001c) at /build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h:120', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h:120', 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7ec04a4', 
          'args': 'this=0x8097360, idx=0xb6190224, field=0x730a001c, value=@0xb618ff64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7ec04a4 in CLuceneIndexWriter::addValue (this=0x8097360, idx=0xb6190224, field=0x730a001c, value=@0xb618ff64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7ec1e5f', 
          'args': 'this=0x8097360, idx=0xb6190224, field=0x730a001c, value=11', 
          'depth': 2, 
          'extra': [
            '#2  0xb7ec1e5f in CLuceneIndexWriter::addValue (this=0x8097360, idx=0xb6190224, field=0x730a001c, value=11)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7eee4c0', 
          'args': 'this=0xb6190224, field=0x730a001c, value=11', 
          'depth': 3, 
          'extra': [
            '#3  0xb7eee4c0 in Strigi::AnalysisResult::addValue (this=0xb6190224, field=0x730a001c, value=11) at /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:269', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:269', 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7effc43', 
          'args': 'this=0xb7f24928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7effc43 in M3uLineAnalyzer::endAnalysis (this=0xb7f24928, complete=true) at /build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp:80', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp:80', 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7eff909', 
          'args': 'this=0x8573e88, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7eff909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x8573e88, complete=true) at /build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp:108', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp:108', 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ef4b7e', 
          'args': 'this=0x8568138', 
          'depth': 6, 
          'extra': [
            '#6  0xb7ef4b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x8568138) at /build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp:84', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp:84', 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d8e5a4', 
          'args': 'this=0x8569d68', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d8e5a4 in Strigi::DataEventInputStream::finish (this=0x8569d68) at /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:109', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:109', 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d8eb22', 
          'args': 'this=0x8569d68, start=@0xb61900a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d8eb22 in Strigi::DataEventInputStream::read (this=0x8569d68, start=@0xb61900a4, min=20480, max=0) at /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:70', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:70', 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7f1e895', 
          'args': 'this=0x84031d0, idx=@0xb6190224, in=0x8569d68', 
          'depth': 9, 
          'extra': [
            '#9  0xb7f1e895 in TextEndAnalyzer::analyze (this=0x84031d0, idx=@0xb6190224, in=0x8569d68) at /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp:50', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp:50', 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f0c359', 
          'args': 'this=0x80b2778, idx=@0xb6190224, input=0x8569d68', 
          'depth': 10, 
          'extra': [
            '#10 0xb7f0c359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80b2778, idx=@0xb6190224, input=0x8569d68) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f0c6b1', 
          'args': 'this=0x80afc4c, idx=@0xb6190224, input=0xb61901e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7f0c6b1 in Strigi::StreamAnalyzer::analyze (this=0x80afc4c, idx=@0xb6190224, input=0xb61901e0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eee05d', 
          'args': 'this=0xb6190224, file=0xb61901e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7eee05d in Strigi::AnalysisResult::index (this=0xb6190224, file=0xb61901e0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:168', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:168', 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7ef36bd', 
          'args': 'this=0x80afc40, analyzer=0x80afc4c', 
          'depth': 13, 
          'extra': [
            '#13 0xb7ef36bd in Strigi::DirAnalyzer::Private::update (this=0x80afc40, analyzer=0x80afc4c) at /build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp:146', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp:146', 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7ef3d0c', 
          'args': 'this=0x80afc40, dirs=@0xb6190338, nthreads=1, c=0x808dbe4', 
          'depth': 14, 
          'extra': [
            '#14 0xb7ef3d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80afc40, dirs=@0xb6190338, nthreads=1, c=0x808dbe4)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7ef3dc8', 
          'args': 'this=0xb6190344, dirs=@0xb6190338, nthreads=1, caller=0x808dbe4', 
          'depth': 15, 
          'extra': [
            '#15 0xb7ef3dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb6190344, dirs=@0xb6190338, nthreads=1, caller=0x808dbe4)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x808dba8', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x808dba8) at /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:86', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:86', 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x808dba8', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x808dba8) at /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:64', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:64', 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x808dba8', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x808dba8) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7ed046b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7ed046b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a7473e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a7473e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'cdrom', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/edbash', 
      'ProcEnviron': ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=en_US.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux edbash-office-gateway 2.6.22-13-generic #1 SMP Thu Oct 4 17:18:44 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000147400', 
          'id': 'Ubuntu:launchpad:0000147400', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000150522', 
          'id': 'Ubuntu:launchpad:0000150522', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000147400', 
          'score': 6.019362
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000150522', 
      'date': '2007-10-08T05:44:50', 
      'extra': 'kde crashed while attempting to configure a screen-saver.\n\nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\n', 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbfb93d5c, field=0x0', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbfb93d5c, field=0x0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h:120', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h:120', 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7ec04a4', 
          'args': 'this=0x8095958, idx=0xb6190224, field=0x0, value=@0xb618ff64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7ec04a4 in CLuceneIndexWriter::addValue (this=0x8095958, idx=0xb6190224, field=0x0, value=@0xb618ff64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7ec1e5f', 
          'args': 'this=0x8095958, idx=0xb6190224, field=0x0, value=11', 
          'depth': 2, 
          'extra': [
            '#2  0xb7ec1e5f in CLuceneIndexWriter::addValue (this=0x8095958, idx=0xb6190224, field=0x0, value=11) at /build/buildd/strigi-0.5.5/src/luceneindexer/cluceneindexwriter.cpp:138', 
            '  [Error: /build/buildd/strigi-0.5.5/src/luceneindexer/cluceneindexwriter.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/luceneindexer/cluceneindexwriter.cpp:138', 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7eee4c0', 
          'args': 'this=0xb6190224, field=0x0, value=11', 
          'depth': 3, 
          'extra': [
            '#3  0xb7eee4c0 in Strigi::AnalysisResult::addValue (this=0xb6190224, field=0x0, value=11) at /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:269', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:269', 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7effc43', 
          'args': 'this=0xb7f24928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7effc43 in M3uLineAnalyzer::endAnalysis (this=0xb7f24928, complete=true) at /build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp:80', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp:80', 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7eff909', 
          'args': 'this=0x80a6548, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7eff909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x80a6548, complete=true) at /build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp:108', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp:108', 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ef4b7e', 
          'args': 'this=0x80b65b8', 
          'depth': 6, 
          'extra': [
            '#6  0xb7ef4b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x80b65b8) at /build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp:84', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp:84', 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d8e5a4', 
          'args': 'this=0x80c7488', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d8e5a4 in Strigi::DataEventInputStream::finish (this=0x80c7488) at /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:109', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:109', 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d8eb22', 
          'args': 'this=0x80c7488, start=@0xb61900a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d8eb22 in Strigi::DataEventInputStream::read (this=0x80c7488, start=@0xb61900a4, min=20480, max=0) at /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:70', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:70', 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7f1e895', 
          'args': 'this=0x80c7088, idx=@0xb6190224, in=0x80c7488', 
          'depth': 9, 
          'extra': [
            '#9  0xb7f1e895 in TextEndAnalyzer::analyze (this=0x80c7088, idx=@0xb6190224, in=0x80c7488) at /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp:50', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp:50', 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f0c359', 
          'args': 'this=0x80a1400, idx=@0xb6190224, input=0x80c7488', 
          'depth': 10, 
          'extra': [
            '#10 0xb7f0c359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80a1400, idx=@0xb6190224, input=0x80c7488) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f0c6b1', 
          'args': 'this=0x809e8d4, idx=@0xb6190224, input=0xb61901e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7f0c6b1 in Strigi::StreamAnalyzer::analyze (this=0x809e8d4, idx=@0xb6190224, input=0xb61901e0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eee05d', 
          'args': 'this=0xb6190224, file=0xb61901e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7eee05d in Strigi::AnalysisResult::index (this=0xb6190224, file=0xb61901e0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:168', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:168', 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7ef36bd', 
          'args': 'this=0x809e8c8, analyzer=0x809e8d4', 
          'depth': 13, 
          'extra': [
            '#13 0xb7ef36bd in Strigi::DirAnalyzer::Private::update (this=0x809e8c8, analyzer=0x809e8d4) at /build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp:146', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp:146', 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7ef3d0c', 
          'args': 'this=0x809e8c8, dirs=@0xb6190338, nthreads=1, c=0x808dd94', 
          'depth': 14, 
          'extra': [
            '#14 0xb7ef3d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x809e8c8, dirs=@0xb6190338, nthreads=1, c=0x808dd94)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7ef3dc8', 
          'args': 'this=0xb6190344, dirs=@0xb6190338, nthreads=1, caller=0x808dd94', 
          'depth': 15, 
          'extra': [
            '#15 0xb7ef3dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb6190344, dirs=@0xb6190338, nthreads=1, caller=0x808dd94)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x808dd58', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x808dd58) at /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:86', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:86', 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x808dd58', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x808dd58) at /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:64', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:64', 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x808dd58', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x808dd58) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7ed046b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7ed046b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a7473e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a7473e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'cdrom', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/clchauvin', 
      'ProcEnviron': ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=en_US.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux chuck-basement 2.6.22-13-generic #1 SMP Thu Oct 4 17:18:44 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000150534', 
          'id': 'Ubuntu:launchpad:0000150534', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000150534', 
          'id': 'Ubuntu:launchpad:0000150534', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000150534', 
          'id': 'Ubuntu:launchpad:0000150534', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000150534', 
          'id': 'Ubuntu:launchpad:0000150534', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000147400', 
          'score': 4.879227
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000150534', 
      'date': '2007-10-07T09:11:28', 
      'extra': "was typing numbers in a text box in firefox, using  the number pad, when strigi barfed up a lung. The only other things that had recently happened... I'd just awakened the computer from sleep. Well, the monitor anyway (even though I swear I keep turning \"Energy Saving\" off on the monitor, it keeps getting set back on). It's a little after 7: 00am, I haven't had any coffee yet, and strigi up and pulls a number on my like this? After all we'd been through?\n\nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\n", 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbf8e6a2c, field=0x0', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbf8e6a2c, field=0x0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h:120', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/fieldtypes.h:120', 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7eea4a4', 
          'args': 'this=0x80914e0, idx=0xb61ba010, field=0x0, value=@0xb61b9dd4', 
          'depth': 1, 
          'extra': [
            '#1  0xb7eea4a4 in CLuceneIndexWriter::addValue (this=0x80914e0, idx=0xb61ba010, field=0x0, value=@0xb61b9dd4)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7eebe5f', 
          'args': 'this=0x80914e0, idx=0xb61ba010, field=0x0, value=12', 
          'depth': 2, 
          'extra': [
            '#2  0xb7eebe5f in CLuceneIndexWriter::addValue (this=0x80914e0, idx=0xb61ba010, field=0x0, value=12) at /build/buildd/strigi-0.5.5/src/luceneindexer/cluceneindexwriter.cpp:138', 
            '  [Error: /build/buildd/strigi-0.5.5/src/luceneindexer/cluceneindexwriter.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/luceneindexer/cluceneindexwriter.cpp:138', 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7f184c0', 
          'args': 'this=0xb61ba010, field=0x0, value=12', 
          'depth': 3, 
          'extra': [
            '#3  0xb7f184c0 in Strigi::AnalysisResult::addValue (this=0xb61ba010, field=0x0, value=12) at /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:269', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:269', 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7f29c43', 
          'args': 'this=0xb7f4e928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7f29c43 in M3uLineAnalyzer::endAnalysis (this=0xb7f4e928, complete=true) at /build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp:80', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/m3ustreamanalyzer.cpp:80', 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7f29909', 
          'args': 'this=0x80a8710, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7f29909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x80a8710, complete=true) at /build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp:108', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/lineeventanalyzer.cpp:108', 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7f1eb7e', 
          'args': 'this=0x828cb40', 
          'depth': 6, 
          'extra': [
            '#6  0xb7f1eb7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x828cb40) at /build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp:84', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/eventthroughanalyzer.cpp:84', 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7db85a4', 
          'args': 'this=0x828b080', 
          'depth': 7, 
          'extra': [
            '#7  0xb7db85a4 in Strigi::DataEventInputStream::finish (this=0x828b080) at /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:109', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:109', 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7db8b22', 
          'args': 'this=0x828b080, start=@0xb61b9f14, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7db8b22 in Strigi::DataEventInputStream::read (this=0x828b080, start=@0xb61b9f14, min=20480, max=0) at /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:70', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streams/dataeventinputstream.cpp:70', 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7f48895', 
          'args': 'this=0x80cfb10, idx=@0xb61ba010, in=0x828b080', 
          'depth': 9, 
          'extra': [
            '#9  0xb7f48895 in TextEndAnalyzer::analyze (this=0x80cfb10, idx=@0xb61ba010, in=0x828b080) at /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp:50', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/textendanalyzer.cpp:50', 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f36359', 
          'args': 'this=0x80b98c0, idx=@0xb61ba010, input=0x828b080', 
          'depth': 10, 
          'extra': [
            '#10 0xb7f36359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80b98c0, idx=@0xb61ba010, input=0x828b080) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f366b1', 
          'args': 'this=0x80ab9f4, idx=@0xb61ba010, input=0x829f728', 
          'depth': 11, 
          'extra': [
            '#11 0xb7f366b1 in Strigi::StreamAnalyzer::analyze (this=0x80ab9f4, idx=@0xb61ba010, input=0x829f728) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f18cce', 
          'args': 'this=0xb61ba224, name=@0xb61ba068, mt=1187802606, file=0x829f728', 
          'depth': 12, 
          'extra': [
            '#12 0xb7f18cce in Strigi::AnalysisResult::indexChild (this=0xb61ba224, name=@0xb61ba068, mt=1187802606, file=0x829f728)'
          ], 
          'function': 'Strigi::AnalysisResult::indexChild'
        }, 
        {
          'address': '0xb7f48bcf', 
          'args': 'this=0x8293c40, idx=@0xb61ba224, in=0x82d2058', 
          'depth': 13, 
          'extra': [
            '#13 0xb7f48bcf in ZipEndAnalyzer::analyze (this=0x8293c40, idx=@0xb61ba224, in=0x82d2058) at /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/zipendanalyzer.cpp:51', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/zipendanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/endanalyzers/zipendanalyzer.cpp:51', 
          'function': 'ZipEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f36359', 
          'args': 'this=0x80b98c0, idx=@0xb61ba224, input=0x82d2058', 
          'depth': 14, 
          'extra': [
            '#14 0xb7f36359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80b98c0, idx=@0xb61ba224, input=0x82d2058) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:404', 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f366b1', 
          'args': 'this=0x80ab9f4, idx=@0xb61ba224, input=0xb61ba1e0', 
          'depth': 15, 
          'extra': [
            '#15 0xb7f366b1 in Strigi::StreamAnalyzer::analyze (this=0x80ab9f4, idx=@0xb61ba224, input=0xb61ba1e0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/streamanalyzer.cpp:351', 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f1805d', 
          'args': 'this=0xb61ba224, file=0xb61ba1e0', 
          'depth': 16, 
          'extra': [
            '#16 0xb7f1805d in Strigi::AnalysisResult::index (this=0xb61ba224, file=0xb61ba1e0) at /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:168', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/analysisresult.cpp:168', 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7f1d6bd', 
          'args': 'this=0x80ab9e8, analyzer=0x80ab9f4', 
          'depth': 17, 
          'extra': [
            '#17 0xb7f1d6bd in Strigi::DirAnalyzer::Private::update (this=0x80ab9e8, analyzer=0x80ab9f4) at /build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp:146', 
            '  [Error: /build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/streamanalyzer/diranalyzer.cpp:146', 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7f1dd0c', 
          'args': 'this=0x80ab9e8, dirs=@0xb61ba338, nthreads=1, c=0x8098bf4', 
          'depth': 18, 
          'extra': [
            '#18 0xb7f1dd0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80ab9e8, dirs=@0xb61ba338, nthreads=1, c=0x8098bf4)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7f1ddc8', 
          'args': 'this=0xb61ba344, dirs=@0xb61ba338, nthreads=1, caller=0x8098bf4', 
          'depth': 19, 
          'extra': [
            '#19 0xb7f1ddc8 in Strigi::DirAnalyzer::updateDirs (this=0xb61ba344, dirs=@0xb61ba338, nthreads=1, caller=0x8098bf4)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x8098bb8', 
          'depth': 20, 
          'extra': [
            '#20 0x080622ff in PollingListener::poll (this=0x8098bb8) at /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:86', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:86', 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x8098bb8', 
          'depth': 21, 
          'extra': [
            '#21 0x08062413 in PollingListener::run (this=0x8098bb8) at /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:64', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/eventlistener/pollinglistener.cpp:64', 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x8098bb8', 
          'depth': 22, 
          'extra': [
            '#22 0x0805b154 in threadstarter (d=0x8098bb8) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7efa46b', 
          'args': '', 
          'depth': 23, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#23 0xb7efa46b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a9e73e', 
          'args': '', 
          'depth': 24, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#24 0xb7a9e73e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'nvidia', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/john', 
      'ProcEnviron': ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=en_US.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux front13 2.6.22-13-generic #1 SMP Thu Oct 4 17:18:44 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000150069', 
          'id': 'Ubuntu:launchpad:0000150069', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000150069', 
          'id': 'Ubuntu:launchpad:0000150069', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000141639', 
          'score': 5.585655
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000150069', 
      'date': '2007-10-07T00:25:23', 
      'extra': "Went for a snack, when I came back the computer had crashed/rebooted.\nDon't know what to tell you, because I didn't witness it\n\nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\n", 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbfd6910c, field=0x0', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbfd6910c, field=0x0)'
          ], 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7ea14a4', 
          'args': 'this=0x8095a88, idx=0xb6170224, field=0x0, value=@0xb616ff64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7ea14a4 in CLuceneIndexWriter::addValue (this=0x8095a88, idx=0xb6170224, field=0x0, value=@0xb616ff64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7ea2e5f', 
          'args': 'this=0x8095a88, idx=0xb6170224, field=0x0, value=8', 
          'depth': 2, 
          'extra': [
            '#2  0xb7ea2e5f in CLuceneIndexWriter::addValue (this=0x8095a88, idx=0xb6170224, field=0x0, value=8)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7ece4c0', 
          'args': 'this=0xb6170224, field=0x0, value=8', 
          'depth': 3, 
          'extra': [
            '#3  0xb7ece4c0 in Strigi::AnalysisResult::addValue (this=0xb6170224, field=0x0, value=8)'
          ], 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7edfc43', 
          'args': 'this=0xb7f04928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7edfc43 in M3uLineAnalyzer::endAnalysis (this=0xb7f04928, complete=true)'
          ], 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7edf909', 
          'args': 'this=0x83c12d8, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7edf909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x83c12d8, complete=true)'
          ], 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ed4b7e', 
          'args': 'this=0x858aff0', 
          'depth': 6, 
          'extra': [
            '#6  0xb7ed4b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x858aff0)'
          ], 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d6f5a4', 
          'args': 'this=0x858b9e0', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d6f5a4 in Strigi::DataEventInputStream::finish (this=0x858b9e0)'
          ], 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d6fb22', 
          'args': 'this=0x858b9e0, start=@0xb61700a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d6fb22 in Strigi::DataEventInputStream::read (this=0x858b9e0, start=@0xb61700a4, min=20480, max=0)'
          ], 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7efe895', 
          'args': 'this=0x85a5708, idx=@0xb6170224, in=0x858b9e0', 
          'depth': 9, 
          'extra': [
            '#9  0xb7efe895 in TextEndAnalyzer::analyze (this=0x85a5708, idx=@0xb6170224, in=0x858b9e0)'
          ], 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eec359', 
          'args': 'this=0x80bbe78, idx=@0xb6170224, input=0x858b9e0', 
          'depth': 10, 
          'extra': [
            '#10 0xb7eec359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80bbe78, idx=@0xb6170224, input=0x858b9e0)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7eec6b1', 
          'args': 'this=0x80b934c, idx=@0xb6170224, input=0xb61701e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7eec6b1 in Strigi::StreamAnalyzer::analyze (this=0x80b934c, idx=@0xb6170224, input=0xb61701e0)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7ece05d', 
          'args': 'this=0xb6170224, file=0xb61701e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7ece05d in Strigi::AnalysisResult::index (this=0xb6170224, file=0xb61701e0)'
          ], 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7ed36bd', 
          'args': 'this=0x80b9340, analyzer=0x80b934c', 
          'depth': 13, 
          'extra': [
            '#13 0xb7ed36bd in Strigi::DirAnalyzer::Private::update (this=0x80b9340, analyzer=0x80b934c)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7ed3d0c', 
          'args': 'this=0x80b9340, dirs=@0xb6170338, nthreads=1, c=0x808dd44', 
          'depth': 14, 
          'extra': [
            '#14 0xb7ed3d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80b9340, dirs=@0xb6170338, nthreads=1, c=0x808dd44)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7ed3dc8', 
          'args': 'this=0xb6170344, dirs=@0xb6170338, nthreads=1, caller=0x808dd44', 
          'depth': 15, 
          'extra': [
            '#15 0xb7ed3dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb6170344, dirs=@0xb6170338, nthreads=1, caller=0x808dd44)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x808dd08', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x808dd08)'
          ], 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x808dd08', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x808dd08)'
          ], 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x808dd08', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x808dd08) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7eb046b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7eb046b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a5473e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a5473e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'nvidia', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/ramses', 
      'ProcEnviron': ' LANGUAGE=nl_NL:nl\n PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=nl_NL.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux ubuntutest 2.6.22-13-generic #1 SMP Thu Oct 4 17:18:44 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000146201', 
          'score': 5.1673417
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000150264', 
      'date': '2007-10-06T18:56:18', 
      'extra': "Every time I close this program I have the same problem,\nDisk is not full and not write protect so I really don't know what the problem might be.\n\nError displayed: \nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\nUnable to save bookmarks in /home/ramses/.kde/share/apps/d3lphin/bookmarks.xml. Reported error was: Permission denied. This error message will only be shown once. The cause of the error needs to be fixed as quickly as possible, which is most likely a full hard drive.\nGrtz. Ramses\n\n\n", 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbff518cc, field=0xa00006f', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbff518cc, field=0xa00006f)'
          ], 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7e7f4a4', 
          'args': 'this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=@0xb614df64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7e7f4a4 in CLuceneIndexWriter::addValue (this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=@0xb614df64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7e80e5f', 
          'args': 'this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=1', 
          'depth': 2, 
          'extra': [
            '#2  0xb7e80e5f in CLuceneIndexWriter::addValue (this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=1)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7eac4c0', 
          'args': 'this=0xb614e224, field=0xa00006f, value=1', 
          'depth': 3, 
          'extra': [
            '#3  0xb7eac4c0 in Strigi::AnalysisResult::addValue (this=0xb614e224, field=0xa00006f, value=1)'
          ], 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7ebdc43', 
          'args': 'this=0xb7ee2928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7ebdc43 in M3uLineAnalyzer::endAnalysis (this=0xb7ee2928, complete=true)'
          ], 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ebd909', 
          'args': 'this=0x849c7a8, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7ebd909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x849c7a8, complete=true)'
          ], 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7eb2b7e', 
          'args': 'this=0x8491950', 
          'depth': 6, 
          'extra': [
            '#6  0xb7eb2b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x8491950)'
          ], 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d4d5a4', 
          'args': 'this=0x84ab638', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d4d5a4 in Strigi::DataEventInputStream::finish (this=0x84ab638)'
          ], 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d4db22', 
          'args': 'this=0x84ab638, start=@0xb614e0a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d4db22 in Strigi::DataEventInputStream::read (this=0x84ab638, start=@0xb614e0a4, min=20480, max=0)'
          ], 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7edc895', 
          'args': 'this=0x84c8290, idx=@0xb614e224, in=0x84ab638', 
          'depth': 9, 
          'extra': [
            '#9  0xb7edc895 in TextEndAnalyzer::analyze (this=0x84c8290, idx=@0xb614e224, in=0x84ab638)'
          ], 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eca359', 
          'args': 'this=0x80ab530, idx=@0xb614e224, input=0x84ab638', 
          'depth': 10, 
          'extra': [
            '#10 0xb7eca359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80ab530, idx=@0xb614e224, input=0x84ab638)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7eca6b1', 
          'args': 'this=0x80a8a04, idx=@0xb614e224, input=0xb614e1e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7eca6b1 in Strigi::StreamAnalyzer::analyze (this=0x80a8a04, idx=@0xb614e224, input=0xb614e1e0)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eac05d', 
          'args': 'this=0xb614e224, file=0xb614e1e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7eac05d in Strigi::AnalysisResult::index (this=0xb614e224, file=0xb614e1e0)'
          ], 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7eb16bd', 
          'args': 'this=0x80a89f8, analyzer=0x80a8a04', 
          'depth': 13, 
          'extra': [
            '#13 0xb7eb16bd in Strigi::DirAnalyzer::Private::update (this=0x80a89f8, analyzer=0x80a8a04)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7eb1d0c', 
          'args': 'this=0x80a89f8, dirs=@0xb614e338, nthreads=1, c=0x809b224', 
          'depth': 14, 
          'extra': [
            '#14 0xb7eb1d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80a89f8, dirs=@0xb614e338, nthreads=1, c=0x809b224)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7eb1dc8', 
          'args': 'this=0xb614e344, dirs=@0xb614e338, nthreads=1, caller=0x809b224', 
          'depth': 15, 
          'extra': [
            '#15 0xb7eb1dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb614e344, dirs=@0xb614e338, nthreads=1, caller=0x809b224)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x809b1e8', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x809b1e8)'
          ], 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x809b1e8', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x809b1e8)'
          ], 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x809b1e8', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x809b1e8) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7e8e46b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7e8e46b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a3273e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a3273e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'nvidia', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/ramses', 
      'ProcEnviron': ' LANGUAGE=nl_NL:nl\n PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=nl_NL.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux ubuntutest 2.6.22-13-generic #1 SMP Thu Oct 4 17:18:44 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000150264', 
          'score': 8.342042
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000150265', 
      'date': '2007-10-06T18:56:18', 
      'extra': "Every time I close this program I have the same problem,\nDisk is not full and not write protect so I really don't know what the problem might be.\n\nError displayed: \nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\nUnable to save bookmarks in /home/ramses/.kde/share/apps/d3lphin/bookmarks.xml. Reported error was: Permission denied. This error message will only be shown once. The cause of the error needs to be fixed as quickly as possible, which is most likely a full hard drive.\nGrtz. Ramses\n\n\n", 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbff518cc, field=0xa00006f', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbff518cc, field=0xa00006f)'
          ], 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7e7f4a4', 
          'args': 'this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=@0xb614df64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7e7f4a4 in CLuceneIndexWriter::addValue (this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=@0xb614df64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7e80e5f', 
          'args': 'this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=1', 
          'depth': 2, 
          'extra': [
            '#2  0xb7e80e5f in CLuceneIndexWriter::addValue (this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=1)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7eac4c0', 
          'args': 'this=0xb614e224, field=0xa00006f, value=1', 
          'depth': 3, 
          'extra': [
            '#3  0xb7eac4c0 in Strigi::AnalysisResult::addValue (this=0xb614e224, field=0xa00006f, value=1)'
          ], 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7ebdc43', 
          'args': 'this=0xb7ee2928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7ebdc43 in M3uLineAnalyzer::endAnalysis (this=0xb7ee2928, complete=true)'
          ], 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ebd909', 
          'args': 'this=0x849c7a8, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7ebd909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x849c7a8, complete=true)'
          ], 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7eb2b7e', 
          'args': 'this=0x8491950', 
          'depth': 6, 
          'extra': [
            '#6  0xb7eb2b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x8491950)'
          ], 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d4d5a4', 
          'args': 'this=0x84ab638', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d4d5a4 in Strigi::DataEventInputStream::finish (this=0x84ab638)'
          ], 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d4db22', 
          'args': 'this=0x84ab638, start=@0xb614e0a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d4db22 in Strigi::DataEventInputStream::read (this=0x84ab638, start=@0xb614e0a4, min=20480, max=0)'
          ], 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7edc895', 
          'args': 'this=0x84c8290, idx=@0xb614e224, in=0x84ab638', 
          'depth': 9, 
          'extra': [
            '#9  0xb7edc895 in TextEndAnalyzer::analyze (this=0x84c8290, idx=@0xb614e224, in=0x84ab638)'
          ], 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eca359', 
          'args': 'this=0x80ab530, idx=@0xb614e224, input=0x84ab638', 
          'depth': 10, 
          'extra': [
            '#10 0xb7eca359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80ab530, idx=@0xb614e224, input=0x84ab638)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7eca6b1', 
          'args': 'this=0x80a8a04, idx=@0xb614e224, input=0xb614e1e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7eca6b1 in Strigi::StreamAnalyzer::analyze (this=0x80a8a04, idx=@0xb614e224, input=0xb614e1e0)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eac05d', 
          'args': 'this=0xb614e224, file=0xb614e1e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7eac05d in Strigi::AnalysisResult::index (this=0xb614e224, file=0xb614e1e0)'
          ], 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7eb16bd', 
          'args': 'this=0x80a89f8, analyzer=0x80a8a04', 
          'depth': 13, 
          'extra': [
            '#13 0xb7eb16bd in Strigi::DirAnalyzer::Private::update (this=0x80a89f8, analyzer=0x80a8a04)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7eb1d0c', 
          'args': 'this=0x80a89f8, dirs=@0xb614e338, nthreads=1, c=0x809b224', 
          'depth': 14, 
          'extra': [
            '#14 0xb7eb1d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80a89f8, dirs=@0xb614e338, nthreads=1, c=0x809b224)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7eb1dc8', 
          'args': 'this=0xb614e344, dirs=@0xb614e338, nthreads=1, caller=0x809b224', 
          'depth': 15, 
          'extra': [
            '#15 0xb7eb1dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb614e344, dirs=@0xb614e338, nthreads=1, caller=0x809b224)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x809b1e8', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x809b1e8)'
          ], 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x809b1e8', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x809b1e8)'
          ], 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x809b1e8', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x809b1e8) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7e8e46b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7e8e46b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a3273e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a3273e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'nvidia', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/ramses', 
      'ProcEnviron': ' LANGUAGE=nl_NL:nl\n PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=nl_NL.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux ubuntutest 2.6.22-13-generic #1 SMP Thu Oct 4 17:18:44 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000150264', 
          'id': 'Ubuntu:launchpad:0000150264', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000150265', 
          'score': 8.545265
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000150266', 
      'date': '2007-10-06T18:56:18', 
      'extra': "Every time I close this program I have the same problem,\nDisk is not full and not write protect so I really don't know what the problem might be.\n\nError displayed: \nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\nUnable to save bookmarks in /home/ramses/.kde/share/apps/d3lphin/bookmarks.xml. Reported error was: Permission denied. This error message will only be shown once. The cause of the error needs to be fixed as quickly as possible, which is most likely a full hard drive.\nGrtz. Ramses\n\n\n", 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbff518cc, field=0xa00006f', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbff518cc, field=0xa00006f)'
          ], 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7e7f4a4', 
          'args': 'this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=@0xb614df64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7e7f4a4 in CLuceneIndexWriter::addValue (this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=@0xb614df64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7e80e5f', 
          'args': 'this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=1', 
          'depth': 2, 
          'extra': [
            '#2  0xb7e80e5f in CLuceneIndexWriter::addValue (this=0x80971b8, idx=0xb614e224, field=0xa00006f, value=1)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7eac4c0', 
          'args': 'this=0xb614e224, field=0xa00006f, value=1', 
          'depth': 3, 
          'extra': [
            '#3  0xb7eac4c0 in Strigi::AnalysisResult::addValue (this=0xb614e224, field=0xa00006f, value=1)'
          ], 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7ebdc43', 
          'args': 'this=0xb7ee2928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7ebdc43 in M3uLineAnalyzer::endAnalysis (this=0xb7ee2928, complete=true)'
          ], 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ebd909', 
          'args': 'this=0x849c7a8, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7ebd909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x849c7a8, complete=true)'
          ], 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7eb2b7e', 
          'args': 'this=0x8491950', 
          'depth': 6, 
          'extra': [
            '#6  0xb7eb2b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x8491950)'
          ], 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d4d5a4', 
          'args': 'this=0x84ab638', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d4d5a4 in Strigi::DataEventInputStream::finish (this=0x84ab638)'
          ], 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d4db22', 
          'args': 'this=0x84ab638, start=@0xb614e0a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d4db22 in Strigi::DataEventInputStream::read (this=0x84ab638, start=@0xb614e0a4, min=20480, max=0)'
          ], 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7edc895', 
          'args': 'this=0x84c8290, idx=@0xb614e224, in=0x84ab638', 
          'depth': 9, 
          'extra': [
            '#9  0xb7edc895 in TextEndAnalyzer::analyze (this=0x84c8290, idx=@0xb614e224, in=0x84ab638)'
          ], 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eca359', 
          'args': 'this=0x80ab530, idx=@0xb614e224, input=0x84ab638', 
          'depth': 10, 
          'extra': [
            '#10 0xb7eca359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80ab530, idx=@0xb614e224, input=0x84ab638)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7eca6b1', 
          'args': 'this=0x80a8a04, idx=@0xb614e224, input=0xb614e1e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7eca6b1 in Strigi::StreamAnalyzer::analyze (this=0x80a8a04, idx=@0xb614e224, input=0xb614e1e0)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eac05d', 
          'args': 'this=0xb614e224, file=0xb614e1e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7eac05d in Strigi::AnalysisResult::index (this=0xb614e224, file=0xb614e1e0)'
          ], 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7eb16bd', 
          'args': 'this=0x80a89f8, analyzer=0x80a8a04', 
          'depth': 13, 
          'extra': [
            '#13 0xb7eb16bd in Strigi::DirAnalyzer::Private::update (this=0x80a89f8, analyzer=0x80a8a04)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7eb1d0c', 
          'args': 'this=0x80a89f8, dirs=@0xb614e338, nthreads=1, c=0x809b224', 
          'depth': 14, 
          'extra': [
            '#14 0xb7eb1d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80a89f8, dirs=@0xb614e338, nthreads=1, c=0x809b224)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7eb1dc8', 
          'args': 'this=0xb614e344, dirs=@0xb614e338, nthreads=1, caller=0x809b224', 
          'depth': 15, 
          'extra': [
            '#15 0xb7eb1dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb614e344, dirs=@0xb614e338, nthreads=1, caller=0x809b224)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x809b1e8', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x809b1e8)'
          ], 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x809b1e8', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x809b1e8)'
          ], 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x809b1e8', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x809b1e8) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7e8e46b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7e8e46b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a3273e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a3273e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'cdrom', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/ian', 
      'ProcEnviron': ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=en_GB.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux ian-laptop 2.6.22-12-generic #1 SMP Sun Sep 23 18:11:30 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000146201', 
          'id': 'Ubuntu:launchpad:0000146201', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000149548', 
          'id': 'Ubuntu:launchpad:0000149548', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000146201', 
          'score': 6.310311
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000149548', 
      'date': '2007-10-05T18:31:39', 
      'extra': 'Crashes on every startup\n\nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\n', 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbfcfc1ac, field=0x0', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbfcfc1ac, field=0x0)'
          ], 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7edd4a4', 
          'args': 'this=0x808be20, idx=0xb61ad224, field=0x0, value=@0xb61acf64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7edd4a4 in CLuceneIndexWriter::addValue (this=0x808be20, idx=0xb61ad224, field=0x0, value=@0xb61acf64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7edee5f', 
          'args': 'this=0x808be20, idx=0xb61ad224, field=0x0, value=1', 
          'depth': 2, 
          'extra': [
            '#2  0xb7edee5f in CLuceneIndexWriter::addValue (this=0x808be20, idx=0xb61ad224, field=0x0, value=1)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7f0b4c0', 
          'args': 'this=0xb61ad224, field=0x0, value=1', 
          'depth': 3, 
          'extra': [
            '#3  0xb7f0b4c0 in Strigi::AnalysisResult::addValue (this=0xb61ad224, field=0x0, value=1)'
          ], 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7f1cc43', 
          'args': 'this=0xb7f41928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7f1cc43 in M3uLineAnalyzer::endAnalysis (this=0xb7f41928, complete=true)'
          ], 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7f1c909', 
          'args': 'this=0x80a49e8, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7f1c909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x80a49e8, complete=true)'
          ], 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7f11b7e', 
          'args': 'this=0x80a4a50', 
          'depth': 6, 
          'extra': [
            '#6  0xb7f11b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x80a4a50)'
          ], 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7dab5a4', 
          'args': 'this=0x80c4ef0', 
          'depth': 7, 
          'extra': [
            '#7  0xb7dab5a4 in Strigi::DataEventInputStream::finish (this=0x80c4ef0)'
          ], 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7dabb22', 
          'args': 'this=0x80c4ef0, start=@0xb61ad0a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7dabb22 in Strigi::DataEventInputStream::read (this=0x80c4ef0, start=@0xb61ad0a4, min=20480, max=0)'
          ], 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7f3b895', 
          'args': 'this=0x80c4e28, idx=@0xb61ad224, in=0x80c4ef0', 
          'depth': 9, 
          'extra': [
            '#9  0xb7f3b895 in TextEndAnalyzer::analyze (this=0x80c4e28, idx=@0xb61ad224, in=0x80c4ef0)'
          ], 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f29359', 
          'args': 'this=0x80a2368, idx=@0xb61ad224, input=0x80c4ef0', 
          'depth': 10, 
          'extra': [
            '#10 0xb7f29359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80a2368, idx=@0xb61ad224, input=0x80c4ef0)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f296b1', 
          'args': 'this=0x809f83c, idx=@0xb61ad224, input=0xb61ad1e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7f296b1 in Strigi::StreamAnalyzer::analyze (this=0x809f83c, idx=@0xb61ad224, input=0xb61ad1e0)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f0b05d', 
          'args': 'this=0xb61ad224, file=0xb61ad1e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7f0b05d in Strigi::AnalysisResult::index (this=0xb61ad224, file=0xb61ad1e0)'
          ], 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7f106bd', 
          'args': 'this=0x809f830, analyzer=0x809f83c', 
          'depth': 13, 
          'extra': [
            '#13 0xb7f106bd in Strigi::DirAnalyzer::Private::update (this=0x809f830, analyzer=0x809f83c)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7f10d0c', 
          'args': 'this=0x809f830, dirs=@0xb61ad338, nthreads=1, c=0x808da9c', 
          'depth': 14, 
          'extra': [
            '#14 0xb7f10d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x809f830, dirs=@0xb61ad338, nthreads=1, c=0x808da9c)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7f10dc8', 
          'args': 'this=0xb61ad344, dirs=@0xb61ad338, nthreads=1, caller=0x808da9c', 
          'depth': 15, 
          'extra': [
            '#15 0xb7f10dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb61ad344, dirs=@0xb61ad338, nthreads=1, caller=0x808da9c)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x808da60', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x808da60)'
          ], 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x808da60', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x808da60)'
          ], 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x808da60', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x808da60) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7eed46b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7eed46b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a9173e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a9173e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'fglrx', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/goblin', 
      'ProcEnviron': ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=de_DE.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux Ridcully 2.6.22-12-generic #1 SMP Sun Sep 23 18:11:30 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000148917', 
          'id': 'Ubuntu:launchpad:0000148917', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000148917', 
          'id': 'Ubuntu:launchpad:0000148917', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000146435', 
          'score': 5.905002
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000148917', 
      'date': '2007-10-04T12:51:05', 
      'extra': 'After the upgrade from feisty to gutsy, the newly installed strigi daemon crashes on start-up. \n\nKubuntu Gutsy Beta.\n\nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\n', 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbfef0e9c, field=0x7300001c', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbfef0e9c, field=0x7300001c)'
          ], 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7ec44a4', 
          'args': 'this=0x80928a0, idx=0xb6193224, field=0x7300001c, value=@0xb6192f64', 
          'depth': 1, 
          'extra': [
            '#1  0xb7ec44a4 in CLuceneIndexWriter::addValue (this=0x80928a0, idx=0xb6193224, field=0x7300001c, value=@0xb6192f64)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7ec5e5f', 
          'args': 'this=0x80928a0, idx=0xb6193224, field=0x7300001c, value=23', 
          'depth': 2, 
          'extra': [
            '#2  0xb7ec5e5f in CLuceneIndexWriter::addValue (this=0x80928a0, idx=0xb6193224, field=0x7300001c, value=23)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7ef14c0', 
          'args': 'this=0xb6193224, field=0x7300001c, value=23', 
          'depth': 3, 
          'extra': [
            '#3  0xb7ef14c0 in Strigi::AnalysisResult::addValue (this=0xb6193224, field=0x7300001c, value=23)'
          ], 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7f02c43', 
          'args': 'this=0xb7f27928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7f02c43 in M3uLineAnalyzer::endAnalysis (this=0xb7f27928, complete=true)'
          ], 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7f02909', 
          'args': 'this=0x83f85d8, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7f02909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x83f85d8, complete=true)'
          ], 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ef7b7e', 
          'args': 'this=0x83ea5e0', 
          'depth': 6, 
          'extra': [
            '#6  0xb7ef7b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x83ea5e0)'
          ], 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d925a4', 
          'args': 'this=0x8501550', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d925a4 in Strigi::DataEventInputStream::finish (this=0x8501550)'
          ], 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d92b22', 
          'args': 'this=0x8501550, start=@0xb61930a4, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d92b22 in Strigi::DataEventInputStream::read (this=0x8501550, start=@0xb61930a4, min=20480, max=0)'
          ], 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7f21895', 
          'args': 'this=0x853e8a0, idx=@0xb6193224, in=0x8501550', 
          'depth': 9, 
          'extra': [
            '#9  0xb7f21895 in TextEndAnalyzer::analyze (this=0x853e8a0, idx=@0xb6193224, in=0x8501550)'
          ], 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f0f359', 
          'args': 'this=0x80b7658, idx=@0xb6193224, input=0x8501550', 
          'depth': 10, 
          'extra': [
            '#10 0xb7f0f359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80b7658, idx=@0xb6193224, input=0x8501550)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f0f6b1', 
          'args': 'this=0x80b4b2c, idx=@0xb6193224, input=0xb61931e0', 
          'depth': 11, 
          'extra': [
            '#11 0xb7f0f6b1 in Strigi::StreamAnalyzer::analyze (this=0x80b4b2c, idx=@0xb6193224, input=0xb61931e0)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7ef105d', 
          'args': 'this=0xb6193224, file=0xb61931e0', 
          'depth': 12, 
          'extra': [
            '#12 0xb7ef105d in Strigi::AnalysisResult::index (this=0xb6193224, file=0xb61931e0)'
          ], 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7ef66bd', 
          'args': 'this=0x80b4b20, analyzer=0x80b4b2c', 
          'depth': 13, 
          'extra': [
            '#13 0xb7ef66bd in Strigi::DirAnalyzer::Private::update (this=0x80b4b20, analyzer=0x80b4b2c)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7ef6d0c', 
          'args': 'this=0x80b4b20, dirs=@0xb6193338, nthreads=1, c=0x808df6c', 
          'depth': 14, 
          'extra': [
            '#14 0xb7ef6d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80b4b20, dirs=@0xb6193338, nthreads=1, c=0x808df6c)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7ef6dc8', 
          'args': 'this=0xb6193344, dirs=@0xb6193338, nthreads=1, caller=0x808df6c', 
          'depth': 15, 
          'extra': [
            '#15 0xb7ef6dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb6193344, dirs=@0xb6193338, nthreads=1, caller=0x808df6c)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x808df30', 
          'depth': 16, 
          'extra': [
            '#16 0x080622ff in PollingListener::poll (this=0x808df30)'
          ], 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x808df30', 
          'depth': 17, 
          'extra': [
            '#17 0x08062413 in PollingListener::run (this=0x808df30)'
          ], 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x808df30', 
          'depth': 18, 
          'extra': [
            '#18 0x0805b154 in threadstarter (d=0x808df30) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7ed346b', 
          'args': '', 
          'depth': 19, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#19 0xb7ed346b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a7773e', 
          'args': '', 
          'depth': 20, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#20 0xb7a7773e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }, 
    {
      'CrashCounter': '1', 
      'ExecutablePath': '/usr/bin/strigidaemon', 
      'NonfreeKernelModules': 'nvidia', 
      'Package': 'strigi-daemon 0.5.5-2ubuntu2', 
      'PackageArchitecture': 'i386', 
      'ProcCmdline': '/usr/bin/strigidaemon clucene', 
      'ProcCwd': '/home/richard', 
      'ProcEnviron': ' PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games\n LANG=en_US.UTF-8\n SHELL=/bin/bash\n', 
      'Signal': '11', 
      'SourcePackage': 'strigi', 
      'Title': 'strigidaemon crashed with SIGSEGV in Strigi::AnalyzerConfiguration::indexType()', 
      'Uname': 'Linux richard-desktop 2.6.22-12-generic #1 SMP Sun Sep 23 18:11:30 GMT 2007 i686 GNU/Linux', 
      'UserGroups': 'adm admin audio cdrom dialout dip floppy lpadmin netdev plugdev powerdev scanner video', 
      'buckets': {
        '1.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.0/Ubuntu:launchpad:0000116712', 
          'id': 'Ubuntu:launchpad:0000116712', 
          'project': 'Ubuntu', 
          'threshold': '1.0', 
          'total': null
        }, 
        '1.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/1.5/Ubuntu:launchpad:0000127694', 
          'id': 'Ubuntu:launchpad:0000127694', 
          'project': 'Ubuntu', 
          'threshold': '1.5', 
          'total': null
        }, 
        '2.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.0/Ubuntu:launchpad:0000132195', 
          'id': 'Ubuntu:launchpad:0000132195', 
          'project': 'Ubuntu', 
          'threshold': '2.0', 
          'total': null
        }, 
        '2.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/2.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '2.75', 
          'total': null
        }, 
        '3.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.0', 
          'total': null
        }, 
        '3.25': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.25/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.25', 
          'total': null
        }, 
        '3.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.5', 
          'total': null
        }, 
        '3.75': {
          'href': 'http://localhost:49263/Ubuntu/buckets/3.75/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '3.75', 
          'total': null
        }, 
        '4.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.0', 
          'total': null
        }, 
        '4.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/4.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '4.5', 
          'total': null
        }, 
        '5.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.0/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.0', 
          'total': null
        }, 
        '5.5': {
          'href': 'http://localhost:49263/Ubuntu/buckets/5.5/Ubuntu:launchpad:0000139026', 
          'id': 'Ubuntu:launchpad:0000139026', 
          'project': 'Ubuntu', 
          'threshold': '5.5', 
          'total': null
        }, 
        '6.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/6.0/Ubuntu:launchpad:0000148343', 
          'id': 'Ubuntu:launchpad:0000148343', 
          'project': 'Ubuntu', 
          'threshold': '6.0', 
          'total': null
        }, 
        '7.0': {
          'href': 'http://localhost:49263/Ubuntu/buckets/7.0/Ubuntu:launchpad:0000148343', 
          'id': 'Ubuntu:launchpad:0000148343', 
          'project': 'Ubuntu', 
          'threshold': '7.0', 
          'total': null
        }, 
        'top_match': {
          'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
          'project': 'Ubuntu', 
          'report_id': 'Ubuntu:launchpad:0000146435', 
          'score': 5.762886
        }
      }, 
      'cpu': 'i386', 
      'database_id': 'Ubuntu:launchpad:0000148343', 
      'date': '2007-10-02T19:55:35', 
      'extra': 'After logging into a user account (using Kubuntu desktop with kdm), if I try to plug in a flash mp3 player, strigi crashes.\n\nStacktraceTop:  Strigi::AnalyzerConfiguration::indexType ()\n CLuceneIndexWriter::addValue ()\n CLuceneIndexWriter::addValue ()\n Strigi::AnalysisResult::addValue ()\n ?? () from /usr/lib/libstreamanalyzer.so.0\n\n', 
      'href': 'http://localhost:49263/Ubuntu/reports/launchpad', 
      'os': 'Ubuntu 7.10', 
      'project': 'Ubuntu', 
      'stacktrace': [
        {
          'args': 'this=0xbf894a9c, field=0x67697274', 
          'depth': 0, 
          'extra': [
            '#0  Strigi::AnalyzerConfiguration::indexType (this=0xbf894a9c, field=0x67697274)'
          ], 
          'function': 'Strigi::AnalyzerConfiguration::indexType'
        }, 
        {
          'address': '0xb7ec14a4', 
          'args': 'this=0x8094790, idx=0xb6191010, field=0x67697274, value=@0xb6190dd4', 
          'depth': 1, 
          'extra': [
            '#1  0xb7ec14a4 in CLuceneIndexWriter::addValue (this=0x8094790, idx=0xb6191010, field=0x67697274, value=@0xb6190dd4)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7ec2e5f', 
          'args': 'this=0x8094790, idx=0xb6191010, field=0x67697274, value=16', 
          'depth': 2, 
          'extra': [
            '#2  0xb7ec2e5f in CLuceneIndexWriter::addValue (this=0x8094790, idx=0xb6191010, field=0x67697274, value=16)'
          ], 
          'function': 'CLuceneIndexWriter::addValue'
        }, 
        {
          'address': '0xb7eef4c0', 
          'args': 'this=0xb6191010, field=0x67697274, value=16', 
          'depth': 3, 
          'extra': [
            '#3  0xb7eef4c0 in Strigi::AnalysisResult::addValue (this=0xb6191010, field=0x67697274, value=16)'
          ], 
          'function': 'Strigi::AnalysisResult::addValue'
        }, 
        {
          'address': '0xb7f00c43', 
          'args': 'this=0xb7f25928, complete=true', 
          'depth': 4, 
          'extra': [
            '#4  0xb7f00c43 in M3uLineAnalyzer::endAnalysis (this=0xb7f25928, complete=true)'
          ], 
          'function': 'M3uLineAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7f00909', 
          'args': 'this=0x82e4358, complete=true', 
          'depth': 5, 
          'extra': [
            '#5  0xb7f00909 in Strigi::LineEventAnalyzer::endAnalysis (this=0x82e4358, complete=true)'
          ], 
          'function': 'Strigi::LineEventAnalyzer::endAnalysis'
        }, 
        {
          'address': '0xb7ef5b7e', 
          'args': 'this=0x82e8038', 
          'depth': 6, 
          'extra': [
            '#6  0xb7ef5b7e in Strigi::EventThroughAnalyzer::handleEnd (this=0x82e8038)'
          ], 
          'function': 'Strigi::EventThroughAnalyzer::handleEnd'
        }, 
        {
          'address': '0xb7d8f5a4', 
          'args': 'this=0x82e7ef8', 
          'depth': 7, 
          'extra': [
            '#7  0xb7d8f5a4 in Strigi::DataEventInputStream::finish (this=0x82e7ef8)'
          ], 
          'function': 'Strigi::DataEventInputStream::finish'
        }, 
        {
          'address': '0xb7d8fb22', 
          'args': 'this=0x82e7ef8, start=@0xb6190f14, min=20480, max=0', 
          'depth': 8, 
          'extra': [
            '#8  0xb7d8fb22 in Strigi::DataEventInputStream::read (this=0x82e7ef8, start=@0xb6190f14, min=20480, max=0)'
          ], 
          'function': 'Strigi::DataEventInputStream::read'
        }, 
        {
          'address': '0xb7f1f895', 
          'args': 'this=0x82db300, idx=@0xb6191010, in=0x82e7ef8', 
          'depth': 9, 
          'extra': [
            '#9  0xb7f1f895 in TextEndAnalyzer::analyze (this=0x82db300, idx=@0xb6191010, in=0x82e7ef8)'
          ], 
          'function': 'TextEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f0d359', 
          'args': 'this=0x80ae6a0, idx=@0xb6191010, input=0x82e7ef8', 
          'depth': 10, 
          'extra': [
            '#10 0xb7f0d359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80ae6a0, idx=@0xb6191010, input=0x82e7ef8)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f0d6b1', 
          'args': 'this=0x80abb74, idx=@0xb6191010, input=0x8304f28', 
          'depth': 11, 
          'extra': [
            '#11 0xb7f0d6b1 in Strigi::StreamAnalyzer::analyze (this=0x80abb74, idx=@0xb6191010, input=0x8304f28)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eefcce', 
          'args': 'this=0xb6191224, name=@0xb6191068, mt=1102251444, file=0x8304f28', 
          'depth': 12, 
          'extra': [
            '#12 0xb7eefcce in Strigi::AnalysisResult::indexChild (this=0xb6191224, name=@0xb6191068, mt=1102251444, file=0x8304f28)'
          ], 
          'function': 'Strigi::AnalysisResult::indexChild'
        }, 
        {
          'address': '0xb7f1fbcf', 
          'args': 'this=0x82ad100, idx=@0xb6191224, in=0x82ab260', 
          'depth': 13, 
          'extra': [
            '#13 0xb7f1fbcf in ZipEndAnalyzer::analyze (this=0x82ad100, idx=@0xb6191224, in=0x82ab260)'
          ], 
          'function': 'ZipEndAnalyzer::analyze'
        }, 
        {
          'address': '0xb7f0d359', 
          'args': 'this=0x80ae6a0, idx=@0xb6191224, input=0x82ab260', 
          'depth': 14, 
          'extra': [
            '#14 0xb7f0d359 in Strigi::StreamAnalyzerPrivate::analyze (this=0x80ae6a0, idx=@0xb6191224, input=0x82ab260)'
          ], 
          'function': 'Strigi::StreamAnalyzerPrivate::analyze'
        }, 
        {
          'address': '0xb7f0d6b1', 
          'args': 'this=0x80abb74, idx=@0xb6191224, input=0xb61911e0', 
          'depth': 15, 
          'extra': [
            '#15 0xb7f0d6b1 in Strigi::StreamAnalyzer::analyze (this=0x80abb74, idx=@0xb6191224, input=0xb61911e0)'
          ], 
          'function': 'Strigi::StreamAnalyzer::analyze'
        }, 
        {
          'address': '0xb7eef05d', 
          'args': 'this=0xb6191224, file=0xb61911e0', 
          'depth': 16, 
          'extra': [
            '#16 0xb7eef05d in Strigi::AnalysisResult::index (this=0xb6191224, file=0xb61911e0)'
          ], 
          'function': 'Strigi::AnalysisResult::index'
        }, 
        {
          'address': '0xb7ef46bd', 
          'args': 'this=0x80abb68, analyzer=0x80abb74', 
          'depth': 17, 
          'extra': [
            '#17 0xb7ef46bd in Strigi::DirAnalyzer::Private::update (this=0x80abb68, analyzer=0x80abb74)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::update'
        }, 
        {
          'address': '0xb7ef4d0c', 
          'args': 'this=0x80abb68, dirs=@0xb6191338, nthreads=1, c=0x809b254', 
          'depth': 18, 
          'extra': [
            '#18 0xb7ef4d0c in Strigi::DirAnalyzer::Private::updateDirs (this=0x80abb68, dirs=@0xb6191338, nthreads=1, c=0x809b254)'
          ], 
          'function': 'Strigi::DirAnalyzer::Private::updateDirs'
        }, 
        {
          'address': '0xb7ef4dc8', 
          'args': 'this=0xb6191344, dirs=@0xb6191338, nthreads=1, caller=0x809b254', 
          'depth': 19, 
          'extra': [
            '#19 0xb7ef4dc8 in Strigi::DirAnalyzer::updateDirs (this=0xb6191344, dirs=@0xb6191338, nthreads=1, caller=0x809b254)'
          ], 
          'function': 'Strigi::DirAnalyzer::updateDirs'
        }, 
        {
          'address': '0x080622ff', 
          'args': 'this=0x809b218', 
          'depth': 20, 
          'extra': [
            '#20 0x080622ff in PollingListener::poll (this=0x809b218)'
          ], 
          'function': 'PollingListener::poll'
        }, 
        {
          'address': '0x08062413', 
          'args': 'this=0x809b218', 
          'depth': 21, 
          'extra': [
            '#21 0x08062413 in PollingListener::run (this=0x809b218)'
          ], 
          'function': 'PollingListener::run'
        }, 
        {
          'address': '0x0805b154', 
          'args': 'd=0x809b218', 
          'depth': 22, 
          'extra': [
            '#22 0x0805b154 in threadstarter (d=0x809b218) at /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
            '  [Error: /build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp was not found in source tree]'
          ], 
          'file': '/build/buildd/strigi-0.5.5/src/daemon/strigithread.cpp:115', 
          'function': 'threadstarter'
        }, 
        {
          'address': '0xb7ed146b', 
          'args': '', 
          'depth': 23, 
          'dylib': '/lib/tls/i686/cmov/libpthread.so.0', 
          'extra': [
            '#23 0xb7ed146b in start_thread () from /lib/tls/i686/cmov/libpthread.so.0'
          ], 
          'function': 'start_thread'
        }, 
        {
          'address': '0xb7a7573e', 
          'args': '', 
          'depth': 24, 
          'dylib': '/lib/tls/i686/cmov/libc.so.6', 
          'extra': [
            '#24 0xb7a7573e in clone () from /lib/tls/i686/cmov/libc.so.6'
          ], 
          'function': 'clone'
        }
      ], 
      'type': 'Crash'
    }
  ], 
  'total': 26
});
