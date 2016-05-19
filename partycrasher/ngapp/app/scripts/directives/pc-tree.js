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
    templateUrl: 'views/pc-tree.html',

    /* Set up the scope with an ID an a function */
    link(scope) {
      scope.id = _.uniqueId('disclosure-');
      scope.type = valueType;
    }
  };

  function valueType(value) {
    if (typeof value === 'object') {
      if (value instanceof Array) {
        return 'array';
      } else {
        return 'object';
      }
    } else {
      return 'primitive';
    }
    /* TODO: check link. */
  }
});
