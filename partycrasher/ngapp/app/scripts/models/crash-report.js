/**
 * Instantiate by dependency injection.
 *
 * function (CrashReport, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.provider('CrashReport', function (StackFrame, propertyByPath) {
  var $log; /* $log must be injected in $get(). */

  class CrashReport {
    constructor(rawCrash) {
      this._raw = rawCrash;
    }

    /**
     * Grab some info by its path in the raw report data.
     */
    propertyByPath(...path) {
      return propertyByPath(this._raw, ...path);
    }

    get id() {
      return this._raw['database_id'];
    }

    get project() {
      return this._raw['project'];
    }

    get href() {
      return this._raw['href'];
    }

    get date() {
      var isoDate = this._raw['date'].replace(/z$/i, '') + 'Z';
      return new Date(Date.parse(isoDate));
    }

    get stackTrace() {
      var stackTrace = this._raw['stacktrace'];

      if (!stackTrace) {
        return undefined;
      }

      if (!(stackTrace instanceof Array)) {
        $log.error(`Stack trace found in ${this.project}/${this.id} but it's
                   not an array!`);
        return undefined;
      }

      return this._raw['stacktrace'].map(rawFrame => new StackFrame(rawFrame));
    }

    get contextData() {
      /* Return a clone that selectively copies fields from the crash.  */
      return _.pickBy(this._raw, (_value, key) => {
        return !(key in {buckets:1, stacktrace:1});
      });
    }

    /**
     * @return an object of { report_id, project, score, href }.
     */
    get topMatch() {
      return this.propertyByPath('buckets', 'top_match');
    }

    get buckets() {
      return _.pickBy(this._raw['buckets'], (_value, key) => {
        /* Get THRESHOLDS only (the key `top_match` will coerce to NaN, hence
         * be non-finite). */
        return isFinite(key);
      });
    }
  }

  return {
    $get: function (_$log_) {
      $log = _$log_;
      return CrashReport;
    }
  };
});
