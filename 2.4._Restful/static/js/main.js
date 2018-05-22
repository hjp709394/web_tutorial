var app = angular.module('main_app', ['ngSanitize']);

app.controller('user_controller', function($scope, $http) {
  $http.get('/api/v1.0/user_info?user_id=0').
    then(function(response) {
      $scope.name = response.data.name;
      $scope.quote = response.data.quote;
      $scope.about = response.data.about;
      $scope.portrait = response.data.portrait;
      $scope.profile_photo = response.data.profile_photo;
    });
});

app.controller('post_list_controller', function($scope, $http) {
  $http.get('/api/v1.0/post_list?user_id=0&page_index=0').
    then(function(response) {
      $scope.post_list = response.data;
    });
});

