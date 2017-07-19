/**
 * Fetches a property deep into the object. If at any point, the property
 * cannot be found, returns undefined.
 *
 * Usage:
 *
 *  > propertyByPath({some: ['deep', {object: 'path'}]}, 'some', 1, 'object')
 *  'path'
 *
 */
angular.module('PartyCrasherApp')
.constant('propertyByPath', function (root, ...fullPath) {
  return propertyByPath(root, fullPath);

  function propertyByPath(obj, path) {
    var [head, ...rest] = path;
    if (path.length === 0) {
      return undefined;
    } else if (nullOrUndefined(obj)) {
      return undefined;
    } else if (path.length === 1) {
      return obj[head];
    } else if (nullOrUndefined(obj[head])) {
      return undefined;
    } else {
      return propertyByPath(obj[head], rest);
    }
  }

  function nullOrUndefined(value) {
    return value === null || value === undefined;
  }
});
