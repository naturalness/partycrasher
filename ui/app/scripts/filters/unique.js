/* From
 * http://stackoverflow.com/questions/15914658/how-to-make-ng-repeat-filter-out-duplicate-results
 * Mon May 30 2016
 */
angular.module('PartyCrasherApp')
  .filter('unique', function () {
    return function (arr, field) {
        var r = _.uniqBy(arr, function(a) { return a[field]; });
        return r;
    };
  });