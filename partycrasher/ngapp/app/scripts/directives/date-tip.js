angular.module('PartyCrasherApp')
.directive('dateTip', function() {
  return {
    restrict: 'A',
    link: function(scope, element, attributes) {
      var container = angular.element("<span class='dateparent'></span>");
      var old = element;
      element = element.clone();
      container.append(element);
      var tipdiv = angular.element("<div class='datetip'>Examples:<br/>MM/DD/YY<br/>2 hours ago<br/>Fri, 12 Dec 2014 10:55:50<br/>2016<br/>8 am</div>");
      container.append(tipdiv);
      element.on("focus", function() {
        tipdiv.css("display", "block");
      });
      element.on("blur", function() {
        tipdiv.css("display", "none");
      });
      container = old.replaceWith(container);
    },
    scope: {
      false
    }
  };
});

