/**
 * Instantiate by dependency injection.
 *
 * function (StackFrame, $scope) { ... }
 */
angular.module('PartyCrasherApp')
.constant('StackFrame', class StackFrame {
  constructor(rawFrame) {
    this._raw = rawFrame;
  }

  get address() {
    return this._raw['address'];
  }

  get filename() {
    /* Remove line information. */
    var filename = this._raw['file'];
    if (!filename) {
      return undefined;
    }
    return filename.replace(/:\d+$/, '');
  }

  get line() {
    var filename = this._raw['file'];
    if (!filename) {
      return undefined;
    }

    /* Return only line information. */
    var matches = filename.match(/:(\d+)$/);
    if (!matches) {
      return undefined;
    }

    return matches[1];
  }

  get module() {
    return undefined;
  }

  get func() {
    return this._raw['function'];
  }
});
