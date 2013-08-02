function ctrl($scope, $http, $templateCache) {
    $scope.list = function(type) {
        $http({method: 'GET', url: './api/'+type, cache: $templateCache}).
            success(function(data, status, headers, config) {
                $scope.items = data;                  //set view model
                $scope.view = './Partials/list.html'; //set to list view
            }).
            error(function(data, status, headers, config) {
                $scope.items = data || "Request failed";
                $scope.status = status;
                $scope.view = './Partials/list.html';
            });
  }
                        
  $scope.show = function('panel', id) {
      $http({method: 'GET', url: './api/' + type + '/' + id, cache: $templateCache}).
          success(function(data, status, headers, config) {
              $scope.detail = data;                   //set view model
              $scope.view = './Partials/detail.html'; //set to detail view
          }).
          error(function(data, status, headers, config) {
              $scope.appDetail = data || "Request failed";
              $scope.status = status;
              $scope.view = './Partials/detail.html';
          });
  }
                
  $scope.view = './Partials/list.html'; //set default view
  $scope.list('panel');
}
AppListCtrl.$inject = ['$scope', '$http', '$templateCache'];