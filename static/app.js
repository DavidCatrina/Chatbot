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
            text: 'Bine ati venit la sistemul de programari. Cum va pot ajuta?'
        });
    };

    $scope.askQuestion = function() {
        // Call the Flask endpoint
        $http.get('/answer').then(function(response) {
            if (response.data.status === "success") {
                $scope.messages.push({
                    text: 'Intrebare: ' + response.data.question
                });
                $scope.messages.push({
                    text: 'Raspuns: ' + response.data.answer
                });
            } else {
                $scope.messages.push({
                    text: 'Eroare: ' + response.data.message
                });
            }
        }).catch(function(error) {
            $scope.messages.push({
                text: 'A aparut o problema cand am procesat intrevarea dumneavoastra. Va rugam incarcati din nou!'
            });
        });
    };
}]);
