var app = angular.module("groupsApp", []);
app.controller("groupsController", ['$scope', '$location', '$http',
    function($scope, $location, $http) {
        $scope.url = $location.absUrl();
        $http.get("/groups/getall")
            .then(function(response) {
                scope.listOfAllGroups = response.data()
            });
    }
  ]);
app.directive("listOfGroups", function() {
  return {
    template :  "<ul>\n" +
                "  <li ng-repeat=\"x in listOfAllGroups\">{{ x }}</li>\n" +
                "</ul>"
  };
});