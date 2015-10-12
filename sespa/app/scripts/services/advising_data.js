'use strict';

/**
 * @ngdoc service
 * @name sespaApp.advisingService
 * @description
 * # advisingService
 * Factory in the sespaApp.
 */
angular.module('sespaApp')
  .factory('advisingData', function($http) {
    var config = function() {
      return $http.get('api/', {'cache': true})
        .then(function(response) {
          // console.log(response.data);
          return response.data;
        });
    };

    var pushPaginatedData = function(obj, url) {
      $http.get(url).then(function(response) {
        response.data.results.forEach(function(entry) {
          obj.push(entry);
        });

        if (response.data.next !== null) {
          pushPaginatedData(obj, response.data.next);
        }
      });
    };

    // Public API here
    return {
      allAdvisors: function() {
        return config().then(function(config) {
          return $http.get(config.advisors, {'cache': true})
            .then(function(response) {
              return response.data
            });
        });
      },

      advisorDetails: function(advisorName) {
        return config().then(function(config) {
          return $http.get(config.advisors+advisorName+'/', {'cache': true})
            .then(function(response) {
              return response.data;
            });
        });
      },
      
      advisorsStudents: function(advisorName) {
        return config().then(function(config) {
          return $http.get(config.advisors+advisorName+'/students/', {'cache': true})
            .then(function(response) {
              return response.data;
            });
        });
      },

      allStudents: function() {
        return config().then(function(config) {
          return $http.get(config.students, {'cache': true})
            .then(function(response) {
              return response.data
            });
        });
      }

    };
  });