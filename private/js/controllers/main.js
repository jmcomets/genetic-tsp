// Main controller handling dataset loading as well as other global stuff
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
