// describe('controllers', function() {
//     var columns, episodeData, optionsData, patientData, Schema, schema, Episode, Item;

//     beforeEach(function() {
//         module('opal.controllers');
//         columns = [
//             {
//                 name: 'demographics',
//                 single: true,
//                 fields: [
//                     {name: 'name', type: 'string'},
//                     {name: 'date_of_birth', type: 'date'},
//                 ]},
//             {
//                 name: 'location',
//                 single: true,
//                 fields: [
//                     {name: 'category', type: 'string'},
//                     {name: 'hospital', type: 'string'},
//                     {name: 'ward', type: 'string'},
//                     {name: 'bed', type: 'string'},
//                     {name: 'date_of_admission', type: 'date'},
//                     {name: 'tags', type: 'list'},
//                 ]},
//             {
//                 name: 'diagnosis',
//                 single: false,
//                 fields: [
//                     {name: 'condition', type: 'string'},
//                     {name: 'provisional', type: 'boolean'},
//                 ]},
//         ];

//         episodeData = {
//             id: 123,
//             demographics: [{
//                 id: 101,
//                 name: 'John Smith',
//                 date_of_birth: '1980-07-31'
//             }],
//             location: [{
//                 category: 'Inepisode',
//                 hospital: 'UCH',
//                 ward: 'T10',
//                 bed: '15',
//                 date_of_admission: '2013-08-01',
//                 tags: {'mine': true, 'tropical': true}
//             }],
//             diagnosis: [{
//                 id: 102,
//                 condition: 'Dengue',
//                 provisional: true,
//             }, {
//                 id: 103,
//                 condition: 'Malaria',
//                 provisional: false,
//             }]
//         };

//         patientData = {
//                 "active_episode_id": null,
//                 "demographics": [
//                     {
//                         "consistency_token": "0beb0d46",
//                         "date_of_birth": "1999-12-12",
//                         "hospital_number": "",
//                         "id": 2,
//                         "name": "Mr WAT",
//                         "patient_id": 2
//                     }
//                 ],
//                 "episodes": {
//                     "3": {
//                         "antimicrobial": [],
//                         "demographics": [
//                             {
//                                 "consistency_token": "0beb0d46",
//                                 "date_of_birth": "1999-12-12",
//                                 "hospital_number": "",
//                                 "id": 2,
//                                 "name": "Mr WAT",
//                                 "patient_id": 2
//                             }
//                         ],
//                         "diagnosis": [],
//                         "general_note": [],
//                         "id": 3,
//                         "location": [
//                             {
//                                 "bed": "",
//                                 "category": "Discharged",
//                                 "consistency_token": "bd4f5db6",
//                                 "date_of_admission": "2013-11-14",
//                                 "discharge_date": null,
//                                 "episode_id": 3,
//                                 "hospital": "",
//                                 "id": 3,
//                                 "tags": {},
//                                 "ward": ""
//                             }
//                         ],
//                         "microbiology_input": [],
//                         "microbiology_test": [
//                             {
//                                 "adenovirus": "",
//                                 "anti_hbcore_igg": "",
//                                 "anti_hbcore_igm": "",
//                                 "anti_hbs": "",
//                                 "c_difficile_antigen": "",
//                                 "c_difficile_toxin": "",
//                                 "cmv": "",
//                                 "consistency_token": "29429ebf",
//                                 "cryptosporidium": "",
//                                 "date_ordered": "2013-11-14",
//                                 "details": "",
//                                 "ebna_igg": "",
//                                 "ebv": "",
//                                 "entamoeba_histolytica": "",
//                                 "enterovirus": "",
//                                 "episode_id": 3,
//                                 "giardia": "",
//                                 "hbsag": "",
//                                 "hsv": "",
//                                 "hsv_1": "",
//                                 "hsv_2": "",
//                                 "id": 1,
//                                 "igg": "",
//                                 "igm": "",
//                                 "influenza_a": "",
//                                 "influenza_b": "",
//                                 "metapneumovirus": "",
//                                 "microscopy": "",
//                                 "norovirus": "",
//                                 "organism": "",
//                                 "parainfluenza": "",
//                                 "parasitaemia": "",
//                                 "resistant_antibiotics": "",
//                                 "result": "pending",
//                                 "rotavirus": "",
//                                 "rpr": "",
//                                 "rsv": "",
//                                 "sensitive_antibiotics": "",
//                                 "species": "",
//                                 "syphilis": "",
//                                 "test": "Fasciola Serology",
//                                 "tppa": "",
//                                 "vca_igg": "",
//                                 "vca_igm": "",
//                                 "viral_load": "",
//                                 "vzv": ""
//                             }
//                         ],
//                         "past_medical_history": [],
//                         "todo": [],
//                         "travel": []
//                     }
//                 },
//                 "id": 2
//             }

//         optionsData = {
//             condition: ['Another condition', 'Some condition']
//         }

//         inject(function($injector) {
//             Schema = $injector.get('Schema');
//             Episode = $injector.get('Episode');
//             Item = $injector.get('Item');
//         });

//         schema = new Schema(columns);
//     });


//     describe('DischargeEpisodeCtrl', function (){
//         var $scope, $http, $cookieStore, $timeout, $dialog;
//         var dialog, episode, options, demographics;

//         beforeEach(function(){
//             inject(function($injector){
//                 $rootScope  = $injector.get('$rootScope');
//                 $scope      = $rootScope.$new();
//                 $controller = $injector.get('$controller');
//                 $timeout    = $injector.get('$timeout');
//                 $modal      = $injector.get('$modal');
//             });

//             dialog = $modal.open({template: 'notatemplate'});
//             episode = new Episode(episodeData, schema);

//             controller = $controller('DischargeEpisodeCtrl', {
//                 $scope        : $scope,
//                 $timeout      : $timeout,
//                 $modal        : $modal,
//                 $modalInstance: dialog,
//                 episode       : episode,
//                 currentTag    : 'mine',
//                 currentSubTag : 'all'
//             });
//         });

//         describe('setting up the controller', function (){
//             it('Should set up the current category', function () {
//                 expect($scope.currentCategory).toBe('Inepisode');
//             });

//             it('Should set the discharge date to today', function(){
//                 expect($scope.episode.discharge_date)
//                     .toEqual(moment().format('DD/MM/YYYY'));
//             });
//         });

//         describe('confirming discharges', function(){
//             beforeEach(function(){
//                 episode.location[0].category = 'Discharged';
//                 episode.discharge_date = '2012-04-23';

//                 controller = $controller('DischargeEpisodeCtrl', {
//                     $scope        : $scope,
//                     $timeout      : $timeout,
//                     $modal        : $modal,
//                     $modalInstance: dialog,
//                     episode       : episode,
//                     currentTag    : 'mine',
//                     currentSubTag : 'all'
//                 });
//             });

//             it('Should leave the discharge date if confirming', function(){
//                 expect($scope.currentCategory).toBe('Discharged');
//                 expect($scope.episode.discharge_date).toBe('2012-04-23');
//             });
//         });

//         describe('closing the dialog', function(){
//             it('should close the modal instance', function(){
//                 spyOn(dialog, 'close');
//                 $scope.cancel();
//                 expect(dialog.close).toHaveBeenCalledWith('cancel');
//             });
//         });
//     });


// });
