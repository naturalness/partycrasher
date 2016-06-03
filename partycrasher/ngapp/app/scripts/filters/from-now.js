/**
 * Filters the input: a date, or an ISO string, and returns an English
 * relative time expression as in "two days ago".
 *
 * Requires moment().
 */
angular.module('PartyCrasherApp')
  .filter('fromNow', function ($log) {
    return function (input) {
      if (input === undefined || input === null) {
        return undefined;
      }

      var date = moment(input);
      if (!date.isValid()) {
        $log.warn(`Tried to parse an invalid date: ${input}`);
        return undefined;
      }

      return moment(input).fromNow();
    };
  });
