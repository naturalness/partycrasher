angular.module('PartyCrasherApp')
.directive('selectator', function ($document, $timeout) {
  function link(scope, element, attrs) {
    var field = attrs['field'];
    var element = element;
    scope.field = field;
    scope.drop = false;
    scope.number_selected = scope.value.length;
    scope.optors = [];
    for (let o of scope.options) {
      scope.optors.push({
        selected: (
          scope.value.indexOf(o) >= 0
        ),
        id: `${field}_${o}`,
        name: o
      });
    }
    function watcher(newValue, oldValue, scope) {
      if (newValue === oldValue) { // On init
//         return;
      }
      n = 0;
      l = [];
      for (let o of scope.optors) {
        if (o.selected) {
          n += 1;
          l.push(o.name);
        }
      }
      if (n > 1) {
        scope.number_selected = n;
      } else if (n == 1) {
        scope.number_selected = l[0];
      } else {
        scope.number_selected = "any";
      }
      console.log("selectator: " + l);
      scope.value = l;
    }
    for (var i = 0; i < scope.optors.length; i++) {
      var model = `optors[${i}].selected`;
      scope.$watch(model, watcher);
    }
    var statorId = `${field}_stator`;
    function checkFocus() {
      var focused = false;
      var ae = $document[0].activeElement;
      if (ae.tagName == "BODY") {
        console.log("body");
//         return; // return without chaning drop
      }
      var children = element.find("input");
      children.push(element.find("label"));
      for (var child in children) {
        child = children[child];
        if (ae === child) {
          focused = true;
        }
      }
      scope.drop=focused;
      return focused;
    }
    scope.checkFocus=() => {
      $timeout(checkFocus, 100);
    };
    scope.forceFocus=($event) => {
      element.find("input")[0].focus();
    };
    scope.toggle=($event) => {
      console.log(scope.drop);
      if (scope.drop) {
        null;
      } else {
        $timeout(() => {
          element.find("input")[0].focus();
        }, 0);
      }
    };
  }

  return {
    templateUrl: 'views/selectator.html',
    link: link,
    restrict: 'E',
    scope: {
      value: '=',
      options: '<'
    }
  };
});
