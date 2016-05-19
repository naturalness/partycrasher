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


  function looksLikeHref(value) {
    return !!value.match(/^http:\/\/[^\/]+\//);
  }
  
  /* Returns the type of the expression as a string. Note that the type is not
   * necessarily a JavaScript type. */
  function valueType(value) {
    if (value instanceof Array)
      return 'array';
    if (value === null)
      /* NOTE! typeof null === 'object', so do this check first! */
      return 'null';
    if (typeof value == 'object')
      return 'object';
    if (typeof value == 'number')
      return 'number';
    if (typeof value == 'boolean')
      return 'boolean';
    if (typeof value == 'string' && looksLikeHref(value))
      return 'href';
    if (typeof value == 'string')
      return 'string';

    return 'unknown';
  }
});
