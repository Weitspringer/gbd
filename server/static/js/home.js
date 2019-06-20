var app = angular.module('homeApp', []);

app.controller('homeController', ['$scope', '$location',
    function($scope, $location) {
        $scope.url = $location.absUrl();
    }
  ]);