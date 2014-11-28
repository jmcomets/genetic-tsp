// Directive for setting the "viewBox" for an SVG tag
app.directive('vbox', function() {
  return {
    link: function(scope, element, attrs) {
      attrs.$observe('vbox', function(value) {
        element.attr('viewBox', value);
      })
    }
  };
});
