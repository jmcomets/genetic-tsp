'use strict';

var app = angular.module('app', ['ngRoute']);
;app.config(function($routeProvider) {
  var partial = function(name) {
    return '/partials/' + name + '.html';
  };

  $routeProvider
    .when('/datasets/:name', {
      controller: 'DatasetCtrl',
      templateUrl: partial('dataset')
    })
    .when('/home', {
      templateUrl: partial('home')
    })
    .otherwise({
      redirectTo: '/home'
    })
});
;// Controller handling representation of the map (can be SVG, Canvas, etc...)
app.controller('DatasetCtrl', function($scope, $routeParams, APIService) {
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

  // Path for currently viewed solution
  $scope.path = [];

  // Solve for the current startingCity (does not work otherwise)
  $scope.solve = function() {
    $scope.path = [];
    APIService.solve({
      starting_city: $scope.startingCity.name,
      dataset: $scope.currentDataset
    }).then(function(data) {
      angular.forEach(data.path, function(cityName) {
        angular.forEach($scope.cities, function(city) {
          if (city.name == cityName) {
            var prevcity = ($scope.path[$scope.path.length-1])
              ? $scope.path[$scope.path.length-1][1] : $scope.startingCity;
            $scope.path.push([prevcity, city]);
            return;
          }
        });
      });
    }, function() {
      console.log('error');
      $scope.path = [];
    });
  };
  // shortcut
  $scope.setStartingCity = function(city) { $scope.startingCity = city; };

});
;// Main controller handling dataset loading as well as other global stuff
app.controller('MainCtrl', function($scope, $location, APIService) {
  // Load dataset on startup
  APIService.configure().then(function(datasets) {
    $scope.datasets = datasets;
  });

  $scope.isActive = function(viewLocation) {
    //console.log(viewLocation, $location.path());
    return viewLocation == $location.path();
  };
});
;app.directive('stopClick', function () {
  return {
      restrict: 'A',
      link: function (scope, element, attr) {
          element.bind('click', function (e) {
              e.stopPropagation();
          });
      }
  };
});
;// Directive for setting the "viewBox" for an SVG tag
app.directive('vbox', function() {
  return {
    link: function(scope, element, attrs) {
      attrs.$observe('vbox', function(value) {
        element.attr('viewBox', value);
      })
    }
  };
});
;// Service handling HTTP requests to the API
app.service('APIService', function($http, $q) {
  return {
    configure: function() {
      var deferred = $q.defer();
      $http.get('/api/config')
        .success(function(data) { deferred.resolve(data); })
        .error(function() { deferred.reject(); })
      ;
      return deferred.promise;
    }, solve: function(params) {
      var deferred = $q.defer();
      $http.post('/api/solution', params)
        .success(function(data) { deferred.resolve(data); })
        .error(function() { deferred.reject(); })
      ;
      return deferred.promise;
    }
  };
});
