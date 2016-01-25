'use strict';

/**
 * @ngdoc directive
 * @name sespaApp.directive:digDataFetchProgress
 * @description
 * # digDataFetchProgress
 */
angular.module('sespaApp')
  .directive('digDataFetchProgress', function() {
    return {
      templateUrl: 'views/dig_data_fetch_progress.html',
      restrict: 'E',
      scope: {
        progress: '@',
      },
      controller: function ($scope) {
        $scope.showProgress = true;
      }
    };
  });
