angular

.module('tm', ['ngResource'], function($routeProvider) {
  $routeProvider
    .when('/messages', {
      templateUrl: 'messages.html',
      controller: 'MessagesCtrl'
    })
    .when('/contacts', {
      templateUrl: 'contacts.html',
      controller: 'ContactsCtrl'
    })
    .when('/contacts/add', {
      templateUrl: 'add_contact.html',
      controller: 'AddContactCtrl'
    })
    .when('/contacts/:contactId/messages', {
      templateUrl: 'contact_messages.html',
      controller: 'ContactMessagesCtrl'
    })
    .when('/stats', {
      templateUrl: 'stats.html',
      controller: 'StatsCtrl'
    })
    .otherwise({
      redirectTo: '/messages'
    });
})

.config([
  '$httpProvider', function($httpProvider) {
    var interceptor = function($q) {
      var success = function(response) {
        return response;
      };

      var error = function(response) {
        if (response.status === 403) {
          document.location = '/accounts/login';
        }

        return $q.reject(response);
      };

      return function(promise) {
        return promise.then(success, error);
      };
    };

    $httpProvider.responseInterceptors.push(interceptor);

    var csrfToken = window.document.cookie.match(/csrftoken=([^;]+)/)[1];

    $httpProvider.defaults.headers.post['X-CSRFToken'] = csrfToken;
  }
])

.value('user', {
  username: USER
})

.factory('Contact', function($resource) {
  return $resource('/api/contacts/:contactId', {
    contactId: '@id'
  });
})

.factory('Message', function($resource) {
  return $resource('/api/messages/:messageId', {
    messageId: '@id'
  });
})

.factory('Stats', function($resource) {
  return $resource('/api/stats');
})

.controller('MessagesCtrl', function($scope, Message) {
  $scope.loaded = false;

  Message.query(function(messages) {
    $scope.loaded = true;

    messages = _.groupBy(messages, function(msg) {
      return msg.contact;
    })

    messages = _.map(messages, function(msgs) {
      msgs = _.sortBy(msgs, function(msg) {
        return msg.date_sent;
      });

      msgs.reverse();

      return msgs[0];
    });

    messages = _.sortBy(messages, function(msg) {
      return msg.date_sent;
    });

    messages.reverse();

    $scope.messages = messages;
  });
})

.controller('ContactsCtrl', function($scope, Contact) {
  $scope.loaded = false;

  $scope.contacts = Contact.query(function() {
    $scope.loaded = true;
  });
})

.controller('AddContactCtrl', function($scope, Contact) {
  $scope.contact = {
    firstName: '',
    lastName: '',
    phoneNumber: ''
  };

  $scope.add = function() {
    var contact;
    contact = new Contact({
      first_name: $scope.contact.firstName,
      last_name: $scope.contact.lastName,
      phone_number: $scope.contact.phoneNumber
    });

    contact.$save(function(res) {
      window.location = "#/contacts/" + res.id + "/messages";
    });
  };
})

.controller('ContactMessagesCtrl', function($scope, $resource, $routeParams, Contact, Message, user, $timeout) {
  $scope.me = user.username;
  $scope.contact = null;
  $scope.loaded = false;

  if ($routeParams.back == 'messages') {
    $scope.back = {
      text: 'Mesages',
      href: '#/messages'
    }
  } else {
    $scope.back = {
      text: 'Contacts',
      href: '#/contacts'
    }
  }

  $scope.contact = Contact.get({
    contactId: $routeParams.contactId
  }, function(contact) {
    $scope.load();
    $scope.poll();
  });

  $scope.stopPolling = false;

  $scope.$on('$destroy', function() {
    $scope.stopPolling = true;
  });

  $scope.poll = function() {
    $timeout(function() {
      if (!$scope.stopPolling) {
        $scope.load();
        $scope.poll();
      }
    }, 3000);
  };

  $scope.load = function() {
    var msgs = Message.query({
      'contact': $scope.contact.id
    }, function() {
      $scope.loaded = true;

      $scope.messages = _.map(msgs, function(el) {
        var person = el.recepient ? 'me' : 'you';

        return {
          person: person,
          message: el.message
        };
      });

      $scope.scrollToBottom();
    });
  };

  $scope.scrollToBottom = function() {
    if ($scope.contentScroller != null) {
      $scope.contentScroller.scrollToBottom();
    }
  };

  $scope.sendMessage = function() {
    var msg = $scope.newMessage;

    if (msg) {
      var message = new Message({
        recepient: $scope.contact.id,
        message: msg
      });

      message.$save(function(res) {
        $scope.load();
        $scope.newMessage = '';
      });

      $scope.newMessage = 'Sending...';
    }
  };
})

.controller('StatsCtrl', function($scope, Stats) {
  Stats.get(function(stats) {
    $scope.stats = stats;
  });
})

.directive('focus', function() {
  return function(scope, element, attrs) {
    element.focus();
  };
})

.directive('scroller', function() {
  return function(scope, element, attrs) {
    scope[attrs.scroller] = {
      scrollToBottom: function() {
        element.animate({
          scrollTop: element[0].scrollHeight
        }, 300);
      }
    };
  };
})

.directive('plot', function() {
  return function(scope, element, attrs) {
    scope.$watch(attrs.plot, function(data) {
      if (data) {
        $.jqplot(element[0].id, [data], {
          animate: true,
          seriesDefaults: {
              renderer: $.jqplot.BarRenderer,
              pointLabels: { show: true }
          },
          axes: {
              xaxis: {
                  renderer: $.jqplot.DateAxisRenderer,
                  tickInterval: '1 day',
                  tickOptions: { formatString:'%#d' }
              }
          },
          highlighter: { show: false }
      });
      }
    });
  }
});

$.jqplot.config.enablePlugins = true;
