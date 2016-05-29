/**
 * Instantiate by dependency injection.
 *
 * function (Bucket, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.provider('Bucket', function () {
  var _CrashReport;

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
        .sortBy(pair => {
          return pair[1];
        })
        .map('0')
        .value();
    }
  }

  class Bucket {
    constructor(rawBucket) {
      this._raw = rawBucket;
      this._reports = rawBucket['top_reports']
        .map(rawReport => new _CrashReport(rawReport));
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

    /*== Cool metadata. ==*/

    /**
     * TODO: make "count" public.
     */
    get oses() {
      return this._count('os');
    }

    get versions() {
      return this._count('version');
    }

    get builds() {
      return this._count('builds');
    }

    /**
     * Counts the properties and returns them in sorted order.
     */
    _count(property) {
      return new Counter(_.map(this.reports, property)).asSortedArray();
    }
  }

  return {
    $get: function(CrashReport) {
      /* Cannot inject CrashReport in provider definition; instead, inject it
       * here! */
      _CrashReport = CrashReport;
      return Bucket;
    }
  };
});
