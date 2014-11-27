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
    });

    // Hardcoded graph size, world coordinates
    $scope.graph = {
      width: 500,
      height: 500,
    };

    // Cities should be represented as a circle, and therefore will have a
    // radius depending on their size and the world's area (taken as sqrt).
    $scope.cityCircleRadius = function(city) {
      var area = $scope.graph.width * $scope.graph.height;
      return Math.floor(Math.sqrt(area) / $scope.cities.length);
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
