app.config(function($routeProvider) {
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
