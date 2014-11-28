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
    return bounds;
  };

  // Set value on startup (needed for view box)
  $scope.bounds = $scope.updateBounds();

  // Cities should be represented as a circle, and therefore will have a
  // radius depending on their size and the world's area (taken as sqrt).
  //
  // FIXME
  $scope.cityCircleRadius = function(city) {
    var area = $scope.bounds.width * $scope.bounds.height / 10;
    return Math.floor(Math.sqrt(area) / $scope.cities.length);
  };
});
