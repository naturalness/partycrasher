/** 
 * Instantiate by dependency injection.
 *
 * function (Crash, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.factory('CrashReport', function () {
  return class Crash {
    constructor(rawCrash) {
      this._raw = rawCrash;
    }

    get stack() {
      return this._raw['stacktrace'];
    }

    /* TODO: add os, version, date. */
  };
});
