app.directive('stopClick', function () {
  return {
      restrict: 'A',
      link: function (scope, element, attr) {
          element.bind('click', function (e) {
              e.stopPropagation();
          });
      }
  };
});
