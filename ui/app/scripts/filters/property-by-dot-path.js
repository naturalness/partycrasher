angular.module('PartyCrasherApp')
  .filter('propertyByDotPath', function (propertyByPath) {
    return function(path, report) {
      path = path.split('.');
      return propertyByPath(report, ...path);
    };
  });
