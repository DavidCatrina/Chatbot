var app = angular.module('VoiceApp', []);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

app.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {
    $scope.showChat = false;
    $scope.messages = [];

    $scope.bookAppointment = function() {
        $scope.showChat = true;
        $scope.messages.push({
            text: 'Welcome to the appointment system. How can I help you?'
        });
    };

    $scope.askQuestion = function() {
        // Call the Flask endpoint
        $http.get('/answer').then(function(response) {
            if (response.data.status === "success") {
                $scope.messages.push({
                    text: 'Question: ' + response.data.question
                });
                $scope.messages.push({
                    text: 'Answer: ' + response.data.answer
                });
            } else {
                $scope.messages.push({
                    text: 'Error: ' + response.data.message
                });
            }
        }).catch(function(error) {
            $scope.messages.push({
                text: 'There was an error processing your question. Please try again.'
            });
        });
    };
}]);
