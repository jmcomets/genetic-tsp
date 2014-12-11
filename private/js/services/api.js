// Service handling HTTP requests to the API
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
