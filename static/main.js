(function() {
  var app = angular.module('app', []);

  // Controller handling dataset loading as well as setting the currently
  // viewed dataset.
  app.controller('ConfigCtrl', function($scope, APIService, $rootScope) {
    // Load dataset on startup
    APIService.configure().then(function(dataset) {
      $rootScope.dataset = dataset;
    });

    // Change focused dataset
    $scope.setCurrentDataset = function(name) {
      $scope.currentDataset = name;
      $rootScope.$broadcast('currentDatasetChanged', name);
    };
  });

  // Controller handling representation of the map (can be SVG, Canvas, etc...)
  app.controller('MapCtrl', function($scope, $rootScope) {
    $rootScope.$on('currentDatasetChanged', function(_, datasetName) {
      $scope.cities = $rootScope.dataset.citymaps[datasetName];
      $scope.bounds = $scope.updateBounds();
    });

    // Default value for bounds
    $scope.defaultBounds = function() {
      return {
        minX: 0, minY: 0,
        maxX: 0, maxY: 0,
        width: 0, height: 0
      };
    };
    // set default value on startup (needed for view box)
    $scope.bounds = $scope.defaultBounds();

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

    // Cities should be represented as a circle, and therefore will have a
    // radius depending on their size and the world's area (taken as sqrt).
    //
    // FIXME
    $scope.cityCircleRadius = function(city) {
      var area = $scope.bounds.width * $scope.bounds.height / 10;
      return Math.floor(Math.sqrt(area) / $scope.cities.length);
    };
  });

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


  // Service handling HTTP requests to the API
  app.service('APIService', function($http, $q) {
    return {
      configure: function() {
        var deferred = $q.defer();
        $http.get('/api/config')
          .success(function(data) { deferred.resolve(data); })
          .error(function() { /* TODO */ })
        ;
        return deferred.promise;
      }
    };
  });
})();
