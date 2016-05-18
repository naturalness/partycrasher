/**
 * Filters the input: a date, or an ISO string, and returns an English
 * relative time expression as in "two days ago".
 *
 * Requires moment().
 */
angular.module('PartyCrasherApp')
  .filter('fromNow', function () {
    return function (input) {
      return moment(input).fromNow();
    };
  });
