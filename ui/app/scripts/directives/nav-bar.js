angular.module('PartyCrasherApp')
.directive('pcNavBar', function ($log, 
                                 DEFAULT_THRESHOLD, 
                                 THRESHOLDS,
                                 COG_IMAGE
                                ) {
  function link(scope, element, _attrs) {
    scope.COG_IMAGE=COG_IMAGE
    scope.example_projects = [
      'ubuntu',
      'arch',
      'fedora',
      'debian'
      ];
    scope.example_types = [
      'SEGV',
      'ABRT',
      'other'
      ];
    scope.groupings = [
      { value: "report", name: "report (no grouping)" },
      { value: "bucket", name: "automatic bucket" },
    ];
  }
  
  return {
    templateUrl: 'views/nav-bar.html',
    link: link,
    scope: false
  };
});
