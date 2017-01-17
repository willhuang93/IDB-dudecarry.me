// lol.js

// Flips between ascending and descending sort
function sortOrder(oldSortType, newSortType, reverse) {
  if (oldSortType == newSortType) {
    return !reverse;
  }
  else {
    return false;
  }
}

function getNumber(num) {
  var arr = new Array(num);
  for (i = 0; i < num; i++)
  {
    arr[i] = i;
  }
  return arr;
}

var lol_app = angular.module('lol_app', []);

lol_app.controller('lol_controller', function($scope, $http) {

  $scope.rut = "Unit test complete.";
  $scope.fillrut = "";

  // SUMMONERS
  //
  //

  $scope.summs_sortType     = 'name'; // set the default sort type
  $scope.summs_sortReverse  = false;  // set the default sort order
  $scope.summs_search   = '';     // set the default search/filter term

  $scope.sortOrder = sortOrder;
  $scope.getNumber = getNumber;

  // Summoners Data

  $scope.request_summoners = function() {
    $http.get("/api/summoners")
    .then(function(response) {
      $scope.summoners = response.data.summoners;
    });
  }

  $scope.request_summoner = function (id) {
    $http.get("/api/summoner/" + id)
    .then(function(response) {
      var summoner = response.data;
      summoner.icon_url = $scope.champion_icon_url(summoner.top_3_champs[0].name);
      $scope.summoner = summoner;
    });
  }

  /*$scope.summoners = [{
    "name": "XRedxDragonX",
    "id": 23509228,
    "icon_url": "http://sk2.op.gg/images/profile_icons/profileIcon592.jpg",
    "rank": {
        "tier": "DIAMOND",
        "division": 4,
        "league_points": 69
    },
    "teams": [
        "OPot"
    ],
    "top_3_champions": [
        412,
        45,
        55
    ],
    "win_percentage": 0.539603960396,
    "total_games": 202,
    "link" : "/summoner/0",
  },
  {
    "name": "Eveloken",
    "id": 72680640,
    "icon_url": "http://sk2.op.gg/images/profile_icons/profileIcon1105.jpg",
    "rank": {
        "tier": "CHALLENGER",
        "division": 1,
        "league_points": 1360
    },
    "teams": [
        "OPot"
    ],
    "top_3_champions": [
        55,
        45,
        412
    ],
    "win_percentage": 0.691842900302,
    "total_games": 331,
    "link" : "/summoner/1",
  },
  {
    "name": "Ah Wunder",
    "id": 36109721,
    "icon_url": "http://sk2.op.gg/images/profile_icons/profileIcon588.jpg",
    "rank": {
        "tier": "GOLD",
        "division": 2,
        "league_points": 54
    },
    "teams": [
        "zonpls",
        "ILILI"
    ],
    "top_3_champions": [
        55,
        45,
        412
    ],
    "win_percentage": 0.530120481928,
    "total_games": 83,
    "link" : "/summoner/2",
  }];*/

  function get_summoner_link(index) {
    if (index < 0 || index >= $scope.summoners.length) {
      return '#';
    }
    else {
      return '/summoner/' + index;
    }
  }

    function get_summoner_name(index) {
    if (index < 0 || index >= $scope.summoners.length) {
      return 'Not listed';
    }
    else {
      return $scope.summoners[index].name;
    }
  }

  function get_summoner_index(id) {
    for (i = 0; i < $scope.summoners.length; i++) {
      if (id == $scope.summoners[i].id) {
        return i;
      }
    }
    return -1;
  }

  $scope.get_summoner_link = get_summoner_link;
  $scope.get_summoner_name = get_summoner_name;
  $scope.get_summoner_index = get_summoner_index;

  // CHAMPIONS
  //
  //

  $scope.champs_sortType     = 'name'; // set the default sort type
  $scope.champs_sortReverse  = false;  // set the default sort order
  $scope.champs_search   = '';     // set the default search/filter term

  // Champions Data

  $scope.champion_icon_url = function(name) {
  return "http://ddragon.leagueoflegends.com/cdn/6.7.1/img/champion/" + 
    name.replace(/'(.)/, function(v) { return v.toLowerCase(); })
    .replace(/[^a-zA-Z0-9]/g,'') + ".png";
  }

  $scope.request_champs = function() {
    $http.get("/api/champions")
    .then(function(response) {
      $scope.champs = response.data.champions;
    });
  }

  $scope.request_champ = function (id) {
    $http.get("/api/champion/" + id)
    .then(function(response) {
      var champ = response.data;
      champ.icon_url = $scope.champion_icon_url(champ.name);      
      $scope.champ = champ;
    });
  }

  function get_champion_link(index) {
    if (index < 0 || index >= $scope.champs.length) {
      return '#';
    }
    else {
      return '/champion/' + index;
    }
  }

    function get_champion_name(index) {
    if (index < 0 || index >= $scope.champs.length) {
      return 'Not listed';
    }
    else {
      return $scope.champs[index].name;
    }
  }

  function get_champion_index(id) {
    for (i = 0; i < $scope.champs.length; i++) {
      if (id == $scope.champs[i].id) {
        return i;
      }
    }
    return -1;
  }

  $scope.get_champion_link = get_champion_link;
  $scope.get_champion_name = get_champion_name;
  $scope.get_champion_index = get_champion_index;

  // TEAMS
  //
  //

  $scope.teams_sortType     = 'name'; // set the default sort type
  $scope.teams_sortReverse  = false;  // set the default sort order
  $scope.teams_search   = '';     // set the default search/filter term

  // Teams Data

  $scope.request_teams = function() {
    $http.get("/api/teams")
    .then(function(response) {
      $scope.teams = response.data.teams;
    });
  }

  $scope.request_team = function (id) {
    $http.get("/api/team/" + id)
    .then(function(response) {
      $scope.team = response.data;
    });
  }

  /*$scope.teams = [{
      "name": "Order of the Iron Potato",
      "id": "TEAM-222e7b80-49d9-11e4-806c-782bcb4d0bb2",
      "tag": "OPot",
      "status": "RANKED",
      "win_percentage": 0.5,
      "total_games": 2,
      "most_recent_member_timestamp": 1413137738000,
      "players": [
          23509228,
          72680640
      ],
      "link" : "/team/0",
  },
  {
      "name": "Team Zon and Friends",
      "id": "TEAM-f5b98c70-3bcd-11e4-834d-782bcb4d1861",
      "tag": "zonpls",
      "status": "RANKED",
      "win_percentage": 0.6,
      "total_games": 5,
      "most_recent_member_timestamp": 1432351174000,
      "players": [
          36109721
      ],
      "link" : "/team/1",
  },
  {
      "name": "Tomato Terrors",
      "id": "TEAM-9b111140-5e80-11e5-87b6-c81f66dd45c9",
      "tag": "ILILI",
      "status": "RANKED",
      "win_percentage": 0.6,
      "total_games": 8,
      "most_recent_member_timestamp": 1445915715000,
      "players": [
          36109721
      ],
      "link" : "/team/2",
  }];*/

});
