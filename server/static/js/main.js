var app = angular.module('App', []);

app.controller('Controller', ['$scope',
    function($scope) {
      $scope.firstName= "John";
      $scope.lastName= "Doe";
    }
  ]);