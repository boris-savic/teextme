
angular.module('tm', []).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/contacts', {templateUrl: 'contacts.html',   controller: ContactListCtrl}).
      when('/contacts/add', {templateUrl: 'add_contact.html',   controller: AddContactCtrl}).

      otherwise({redirectTo: '/contacts'});
}]);


function ContactListCtrl($scope, $http) {
  $http.get('/contacts/api?format=json').success(function(data) {
    $scope.contacts = data;
  });
}

function AddContactCtrl($scope, $http) {
   $scope.add = function() {
    //TODO save
  }
}


