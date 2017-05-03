(function ($) {
  var timerId = '#match_timer';
  var startButtonId = '#button_start';
  var endButtonId = '#button_end';
  var playerButtonSelector = '.team-player';
  var timer;

  $(function() {
    $(startButtonId).bind('click', function(event) {
      startMatch();
    });

    $(endButtonId).hide();
    $(endButtonId).bind('click', function(event) {
      endMatch();
    });

    $(timerId).hide();

    $(playerButtonSelector).click(function(){
        var playerId = $(this).data('player');
        goal($(this).data('player'), $(this).data('team'), $(this).data('match'));
    }).attr('disabled', 'disabled');

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
  });


  function startMatch() {
    $(startButtonId).hide();
    $(endButtonId).show();

    $(timerId).show();
    $(playerButtonSelector).attr('disabled', 'enabled');
    setTimerText(0,0);
    startTimer();
  }

  function endMatch() {
    stopTimer();
    $(timerId).hide();
    $(endButtonId).attr("disabled","disabled");
  }

	function startTimer() {
		var startTime = new Date().getTime();

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
    $(timerId).html(minutes + ":" + seconds);
  }

  function stopTimer() {
    clearInterval(timer);
  }

  function goal(playerId, teamId, matchId) {
    var minute = $(timerId).text().split(':')[0];
    console.log('request', 'match_goals/' + matchId + '/score_goal/')
    $.ajax({
      type: "POST",
      url: 'match_goals/' + matchId + '/score_goal',
      data: {
        player: playerId,
        team: teamId,
        minute: minute
      },
      success: function() {
        // SUCCESS
        // TODO reload match and goals
      }
    });
  }
  // using jQuery
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
