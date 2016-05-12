'use strict';

describe('Service: homeService', function () {

  // load the service's module
  beforeEach(module('ngappApp'));

  // instantiate service
  var homeService;
  beforeEach(inject(function (_homeService_) {
    homeService = _homeService_;
  }));

  it('should do something', function () {
    expect(!!homeService).toBe(true);
  });

});
