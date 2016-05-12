'use strict';

describe('Controller: TopbucketsCtrl', function () {

  // load the controller's module
  beforeEach(module('ngappApp'));

  var TopbucketsCtrl,
    scope;

  // Initialize the controller and a mock scope
  beforeEach(inject(function ($controller, $rootScope) {
    scope = $rootScope.$new();
    TopbucketsCtrl = $controller('TopbucketsCtrl', {
      $scope: scope
      // place here mocked dependencies
    });
  }));

  it('should attach a list of awesomeThings to the scope', function () {
    expect(TopbucketsCtrl.awesomeThings.length).toBe(3);
  });
});
