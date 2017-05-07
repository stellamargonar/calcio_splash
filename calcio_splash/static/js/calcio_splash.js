(function ($) {
  var timerId = '#match_timer';
  var startButtonId = '#button_start';
  var endButtonId = '#button_end';
  var playerButtonSelector = '.team-player>.btn';
  var timer;

  $(function() {
    $(startButtonId).bind('click', function(event) {
      startMatch();
    });

    $(endButtonId).bind('click', function(event) {
      endMatch();
    });

    $(playerButtonSelector).click(function(){
        goal($(this).data('player'), $(this).data('team'), $(this).data('match'));
    });
    $(playerButtonSelector).on('taphold', function(event) {
      event.stopPropagation();
      if (confirm('Eliminare ultimo goal?'))
        deleteGoal($(this).data('player'), $(this).data('team'), $(this).data('match'));
    });

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var startTime = $(timerId).data('match-start');
    var endTime = $(timerId).data('match-end');

    if (startTime == null && endTime == null) {
      initUIUnstarted();
    } else if (endTime == null) {
      initUIStarted(startTime);
    } else {
      initUIEnded();
    }
  });

  function initUIUnstarted() {
    $(endButtonId).hide();
    $(timerId).hide();
    $(playerButtonSelector).attr('disabled', true);
  }

  function initUIStarted(startTime) {
    $(startButtonId).hide();
    $(endButtonId).show();
    $(timerId).show();
    $(playerButtonSelector).attr('disabled', false);

    // init timer with
    startTimer(startTime);
  }


  function initUIEnded() {
    $(startButtonId).hide();
    $(endButtonId).attr('disabled', true);
    $(timerId).hide();
  }


  function startMatch() {
    $(startButtonId).hide();
    $(endButtonId).show();

    $(timerId).show();
    $(playerButtonSelector).attr('disabled', false);
    startMatchTime($(timerId).data('match-id'));
  }

  function startMatchTime(matchId) {
    $.ajax({
      type: "POST",
      url: 'match_goals/' + matchId + '/start',
      data: {
        time: new Date().getTime()
      },
      success: function(data) {
        setTimerText(0,0);
        startTimer(data.time);
      },
      error: function(data, error) {
        alert(error);
      }
    });
  }

  function endMatch() {
    endMatchTime($(timerId).data('match-id'));
    stopTimer();
    $(timerId).hide();
    $(endButtonId).attr("disabled", true);
    $(playerButtonSelector).attr('disabled', true);
  }

  function endMatchTime(matchId) {
    $.ajax({
      type: "POST",
      url: 'match_goals/' + matchId + '/end',
      data: {
        time: new Date().getTime()
      },
      success: function(data) {
      },
      error: function(data, error) {
        alert(error);
      }
    });
  }

	function startTimer(startTime) {
    startTime = startTime || new Date().getTime();

		// Update the count down every 1 second
		timer = setInterval(function() {
		  var now = new Date().getTime();
		  var distance = now - startTime;

      var minutes = Math.floor(distance / (1000 * 60));
		  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

		  setTimerText(minutes, seconds);
		}, 1000);
	}

  function setTimerText(minutes, seconds) {
    if (minutes < 10) {
      minutes = '0' + minutes;
    }
    if (seconds  < 10) {
      seconds = '0' + seconds;
    }
    $(timerId).html('<h2>' + minutes + ":" + seconds + '</h2>');
  }

  function stopTimer() {
    clearInterval(timer);
  }

  function goal(playerId, teamId, matchId) {
    var minute = $(timerId).text().split(':')[0];
    $.ajax({
      type: "POST",
      url: 'match_goals/' + matchId + '/score_goal',
      data: {
        player: playerId,
        team: teamId,
        minute: minute
      },
      success: function(data) {
        // SUCCESS
        updateScores(data)
      },
      error: function(data, error) {
        alert(error);
      }
    });
  }

  function deleteGoal(playerId, teamId, matchId) {
    $.ajax({
      type: "POST",
      url: 'match_goals/' + matchId + '/undo',
      data: {
        player: playerId,
        team: teamId
      },
      success: function(data) {
        // SUCCESS
        updateScores(data)
      },
      error: function(obj, error) {
        alert(error);
      }
    });
  }

  function updateScores(data) {
    $('.team-score').text(data.team_a_score + ' - ' + data.team_b_score);
    for (var playerId in data.playerMap) {
      $('#player_' + playerId).text('(' + data.playerMap[playerId] + ')')
    }
  }

  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }



})(jQuery);
