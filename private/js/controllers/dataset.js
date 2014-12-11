// Controller handling representation of the map (can be SVG, Canvas, etc...)
app.controller('DatasetCtrl', function($scope, $routeParams) {
  $scope.currentDataset = $routeParams.name;
  $scope.cities = $scope.datasets.citymaps[$scope.currentDataset];

  // Default value for bounds
  $scope.defaultBounds = function() {
    return {
      minX: 0, minY: 0,
      maxX: 0, maxY: 0,
      width: 0, height: 0
    };
  };

  // Update the bounds of the citymap, given the cities
  $scope.updateBounds = function() {
    var bounds = $scope.defaultBounds();
    angular.forEach($scope.cities, function(city) {
      // Update minimum boundary
      if (!bounds.minX || city.position.x < bounds.minX) { bounds.minX = city.position.x; }
      if (!bounds.minY || city.position.y < bounds.minY) { bounds.minY = city.position.y; }

      // Update maximum boundary
      if (!bounds.maxX || city.position.x > bounds.maxX) { bounds.maxX = city.position.x; }
      if (!bounds.maxY || city.position.y > bounds.maxY) { bounds.maxY = city.position.y; }
    });

    // Keep width/height
    bounds.width = bounds.maxX - bounds.minX;
    bounds.height = bounds.maxY - bounds.minY;

    // Zoom out a bit
    var scale = .1;
    bounds.minX -= bounds.width * scale;
    bounds.maxX += bounds.width * scale;
    bounds.minY -= bounds.height * scale;
    bounds.maxY += bounds.height * scale;
    bounds.width = bounds.maxX - bounds.minX;
    bounds.height = bounds.maxY - bounds.minY;
    return bounds;
  };

  // Set value on startup (needed for view box)
  $scope.bounds = $scope.updateBounds();
});
