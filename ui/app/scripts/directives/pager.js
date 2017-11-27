angular.module('PartyCrasherApp')
.directive('pager', function ($log
                                ) {
  return {
    templateUrl: 'views/pager.html',
    scope: false
  };
});
