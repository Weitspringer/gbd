var app = angular.module("groupsApp", []);
app.controller("groupsController", ['$scope', '$http',
    function($scope, $http) {
        $http.get("/groups/getall")
            .then(function(response) {
                $scope.listOfAllGroups = response.data;
            });
    }
  ]);