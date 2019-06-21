var app = angular.module('queryApp', []);

app.controller('queryController', ['$scope', '$location',
    function($scope, $location) {
        $scope.url = $location.absUrl();
    }
  ]);