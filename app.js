// Definirea modulului Angular 'VoiceApp'
var app = angular.module('VoiceApp', []);

// Configurarea pentru a schimba delimitatorii de interpolare (de afișare a datelor) din '{{' și '}}' în '[[' și ']]'
app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

// Definirea controlerului 'MainCtrl' în cadrul modulului 'VoiceApp'
app.controller('MainCtrl', ['$scope', '$http', function($scope, $http) {
    // Inițializarea variabilelor în cadrul scopului (scope) controlerului
    $scope.showChat = false;  // Variabilă pentru a controla afișarea chat-ului
    $scope.messages = [];      // Array pentru a stoca mesajele

    // Funcția pentru a începe programarea unei întâlniri
    $scope.bookAppointment = function() {
        $scope.showChat = true;  // Setarea pentru a afișa chat-ul
        $scope.messages.push({   // Adăugarea unui mesaj inițial la array-ul de mesaje
            text: 'Welcome to the appointment system. How can I help you?'
        });
    };

    $scope.playAudio = function(text) {
        var speechMessage = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(speechMessage);
    };

    // Funcția pentru a pune o întrebare
    $scope.askQuestion = function() {
        // Apelarea unui endpoint Flask folosind serviciul $http
        $http.get('/answer').then(function(response) {
            if (response.data.status === "success") {
                // Adăugarea răspunsului primit la array-ul de mesaje în cazul în care cererea a fost cu succes
                $scope.messages.push({
                    text: 'Question: ' + response.data.question
                });
                $scope.messages.push({
                    text: 'Answer: ' + response.data.answer
                });
                $scope.playAudio(response.data.answer);
            } else {
                // Adăugarea unui mesaj de eroare în cazul în care cererea nu a fost cu succes
                $scope.messages.push({
                    text: 'Error: ' + response.data.message
                });
            }
        }).catch(function(error) {
            // Tratarea erorilor în cazul în care apelul către endpoint nu a putut fi realizat
            $scope.messages.push({
                text: 'There was an error processing your question. Please try again.'
            });
        });
    };
}]);
