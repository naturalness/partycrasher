/**
 * Instantiate by dependency injection.
 *
 * function (Bucket, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.provider('Bucket', function () {
  var CrashReport;

  /**
   * Inner-class for counting distinct values.
   */
  class Counter {
    constructor(collection) {
      this._count = new Map();
      for (var thing of collection) {
        this.count(thing);
      }
    }

    count(thing) {
      /**
       * TODO: Add "unknown" symbol.
       */
      if (thing === null || thing === undefined) {
        return;
      }

      var previous = this._count.get(thing) || 0;
      this._count.set(thing, previous + 1);
    }

    asSortedArray() {
      var unsorted = Array.from(this._count);
      return _(unsorted)
        .sortBy(pair => pair[1])
        .map('0')
        .value();
    }
  }

  class Bucket {
    constructor(rawBucket) {
      this._raw = rawBucket;
      this._reports = rawBucket['top_reports']
        .map(rawReport => new CrashReport(rawReport));
    }

    get id() {
      return this._raw['id'];
    }

    get project() {
      return this._raw['project'];
    }

    get threshold() {
      return this._raw['threshold'];
    }

    get href() {
      return this._raw['href'];
    }

    get firstSeen() {
      return undefined;
    }

    get lastSeen() {
      return undefined;
    }

    get reports() {
      return this._reports;
    }

    /* TODO: what is this doing here? Remove? */
    get a_crash_id() {
      return this._raw['top_reports'][0]['database_id'];
    }

    /**
     * Counts the properties and returns them in descending order of
     * popularity.
     */
    summarize(property) {
      return new Counter(_.map(this.reports, property)).asSortedArray();
    }
  }

  return {
    $get: function(_CrashReport_) {
      /* Cannot inject CrashReport in provider definition; instead, inject it
       * here! */
      CrashReport = _CrashReport_;
      return Bucket;
    }
  };
});
