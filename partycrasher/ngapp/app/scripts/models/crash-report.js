/**
 * Instantiate by dependency injection.
 *
 * function (Crash, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.constant('CrashReport', class Crash {
  constructor(rawCrash) {
    this._raw = rawCrash;
  }

  get id() {
    return this._raw['database_id'];
  }

  get project() {
    return this._raw['project'];
  }

  get date() {
    return this._raw['date'];
  }

  get stacktrace() {
    return this._raw['stacktrace'];
  }

  /**
   * @return an object of { report_id, project, score, href }.
   */
  get topMatch() {
    return this._raw['buckets']['top_match'];
  }

  /*== Some fields used in aggregations. ==*/

  get os() {
    return this._raw['os'];
  }

  get version() {
    return undefined;
  }

  get build() {
    return undefined;
  }
});
