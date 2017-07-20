angular.module('PartyCrasherApp')
.directive('dateTip', function($compile) {
  return {
    restrict: 'A',
    link: function(scope, element, attributes) {
      var container = angular.element("<span class='dateparent'></span>");
      var old = element;
      element = element.clone();
      element.removeAttr('date-tip');
      container.append(element);
      var tipdiv = angular.element("<div class='datetip'></div>");
      container.append(tipdiv);
      element.on("focus", function() {
        tipdiv.css("display", "block");
      });
      element.on("blur", function() {
        tipdiv.css("display", "none");
      });
      old.replaceWith($compile(container)(scope));
    },
  };
});

