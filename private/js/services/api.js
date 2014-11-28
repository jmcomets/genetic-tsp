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
