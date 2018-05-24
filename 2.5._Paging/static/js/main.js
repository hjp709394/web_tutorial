// ngSanitize is necessary for ng-bind-html
var app = angular.module('main_app', ['ngSanitize', 'infinite-scroll']);

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


app.controller('home_controller', function($scope, $http) {
  $http.get('/api/v1.0/post_list?user_id=0&display_at_home=true').
    then(function(response) {
      $scope.post_list = response.data;
    });
});


app.controller('post_list_controller', function($scope, $http) {
  $scope.page_index = 0;
  $scope.post_list = [];
  $scope.busy = false
  //$http.get('/api/v1.0/post_list?user_id=0&display_at_home=false').
  //  then(function(response) {
  //    $scope.post_list = response.data;
  //  });

  $scope.loadMorePost = function() {
    $scope.busy = true;
    $http.get('/api/v1.0/post_list?user_id=0&display_at_home=false&page_index=' + $scope.page_index).
      then(function(response) {
        var new_post_list = response.data;
        if (new_post_list.length != 0) {
          for (var i = 0; i < new_post_list.length; i++) {
            $scope.post_list.push( new_post_list[i] );
          }
        }
	$scope.page_index = $scope.page_index + 1
        $scope.busy = false;
      });
  };
});

