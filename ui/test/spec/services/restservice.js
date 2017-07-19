'use strict';

describe('Service: restService', function () {

  // load the service's module
  beforeEach(module('ngappApp'));

  // instantiate service
  var restService;
  beforeEach(inject(function (_restService_) {
    restService = _restService_;
  }));

  it('should do something', function () {
    expect(!!restService).toBe(true);
  });

});
