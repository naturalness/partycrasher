/**
 * Takes in the object, and a category, and spits out a URL suitable for use
 * in whatever context.
 *
 * Examples:
 * Where bucket = {
 *    id: "06080d73-1d33-4969-9d5e-69263cc01752",
 *    project: "alan_parsons",
 *    threshold: "4.0",
 * }
 *
 *   {{ bucket | uiUrl:"bucket" }}
 *
 *   => 'ui/alan_parsons/buckets/4.0/06080d73-1d33-4969-9d5e-69263cc01752'
 *
 * Requires moment().
 */
angular.module('PartyCrasherApp')
  .filter('uiUrl', function () {
    return function (obj, category) {
      switch (category) {
        case 'bucket':
          return `${obj.project}/buckets/${obj.threshold}/${obj.id}`;
        default:
          throw new Error(`Unknown category: ${category}`);
      }
    };
  });
