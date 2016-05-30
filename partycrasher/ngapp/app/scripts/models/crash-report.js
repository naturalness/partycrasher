/**
 * Instantiate by dependency injection.
 *
 * function (CrashReport, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.provider('CrashReport', function (StackFrame) {
  class CrashReport {
    constructor(rawCrash) {
      this._raw = rawCrash;
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
      return this._raw['buckets']['top_match'];
    }

    get buckets() {
      return _.pickBy(this._raw['buckets'], (_value, key) => {
        return (isFinite(key));
      });
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
  }

  return {
    $get: function() {
      return CrashReport;
    }
  };
});
