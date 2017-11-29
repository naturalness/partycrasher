angular.module('PartyCrasherApp')
.directive('radiotator', function ($document, $timeout) {
  function link(scope, element, attrs) {
    var field = attrs['field'];
    var element = element;
    scope.field = field;
    scope.drop = false;
    scope.optors = [];
    var names_by_value = {};
    for (let o of scope.options) {
      if (o.name) {
        null;
      } else {
        o.name = o.value;
      }
      scope.optors.push({
        id: `${field}_${o.value}`,
        value: o.value,
        name: o.name
      });
      names_by_value[o.value] = o.name;
    }
    function watcher(newValue, oldValue, scope) {
      scope.display_name = names_by_value[scope.value];
    }
    scope.$watch("value", watcher);
    function checkFocus() {
      var focused = false;
      var ae = $document[0].activeElement;
      if (ae.tagName == "BODY") {
        var selection = window.getSelection()
        if (selection) {
          ae = selection.focusNode;
        }
      }
      console.log(ae.tagName);
      
      parent = ae;
      children = element.children();
      
      while (parent.tagName != "BODY") {
        console.log(parent.tagName);
        for (child of children) {
          if (parent === child) {
            focused = true;
          }
        }
        parent = parent.parentNode;
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
    scope.click=($event) =>{
      $event.stopPropagation();
    };
    scope.buttonClick=($event) => {
      if (scope.drop) {
        element.find("input")[0].focus();
        element.find("input")[0].blur();
      } else {
        element.find("input")[0].focus();
      }
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
    templateUrl: 'views/radiotator.html',
    link: link,
    restrict: 'E',
    scope: {
      value: '=',
      options: '<',
    }
  };
});
