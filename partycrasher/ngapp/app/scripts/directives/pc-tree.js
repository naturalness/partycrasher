/**
 * Defines a tree component for displaying JSON.
 */
angular.module('PartyCrasherApp')
.directive('pcTree', function () {
  return {
    restrict: 'E',
    /* Use the value, but set-up only a one-way binding. */
    scope: {
      value: '<'
    },
    templateUrl: 'views/pc-tree.html'
  };
});
