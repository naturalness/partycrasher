/**
 * Takes in the object, and a category, and spits out a URL suitable for use
 * in whatever context.
 *
 * Examples:
 * 
 *   {{ report.href | uiUrl }}
 *
 */
angular.module('PartyCrasherApp')
  .filter('uiUrl', function (REST_BASE, BASE_HREF) {
    return function (href) {
      if (href instanceof String || typeof href == 'string') {
        if (href.startsWith(REST_BASE)) {
          return href.replace(REST_BASE, BASE_HREF);
        } else {
          throw new Error("Bad HREF " + href + " " + REST_BASE);
        }
      }
    };
  });
