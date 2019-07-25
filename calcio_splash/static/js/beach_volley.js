(function ($) {
    var timerId = '#beach_match_timer';
    var startButtonId = '#beach_button_start1';
    var endPrimoTempoButtonId = '#beach_button_end1';
    var startSecondoTempoButtonId = '#beach_button_start2';
    var endButtonId = '#beach_button_end2';
    var resetButtonId = '#beach_button_reset';
    var playerButtonSelector = '.team-player.btn';
    var timer;

    $(function () {
        $(startButtonId).bind('click', function (event) {
            startMatch();
        });

        $(endPrimoTempoButtonId).bind('click', function (event) {
            pauseMatch();
        });

        $(startSecondoTempoButtonId).bind('click', function (event) {
            restartMatch();
        });

        $(endButtonId).bind('click', function (event) {
            endMatch();
        });

        $(resetButtonId).bind('click', function (event) {
            resetMatch($(timerId).data('match-id'));
        });

        $(playerButtonSelector).click(function () {
            goal($(this).data('player'), $(this).data('team'), $(this).data('match'));
        });
        $(playerButtonSelector).on('taphold', function (event) {
            event.stopPropagation();
            if (confirm('Eliminare ultimo goal?'))
                deleteGoal($(this).data('player'), $(this).data('team'), $(this).data('match'));
        });

        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });

        var startTime = $(timerId).data('match-start');
        var endTime = $(timerId).data('match-end');

        var startSecondoTempo = $(timerId).data('match-start-secondo');
        var endPrimoTempo = $(timerId).data('match-end-primo');

        var tempo = null;
        if (endPrimoTempo == null) {
            tempo = 1;
        } else if (startSecondoTempo != null) {
            tempo = 2;
        }
        initUI(
            startTime != null,
            endTime != null,
            tempo,
            startSecondoTempo || startTime);
    });

    function initUI(started, ended, tempo, startTime) {
        if (started && ended) {
            $(startButtonId).hide();
            $(endButtonId).attr('disabled', true);
            $(timerId).hide();
        } else if (!started) {
            $(endPrimoTempoButtonId).hide();
            $(startSecondoTempoButtonId).hide();
            $(endButtonId).hide();

            $(timerId).hide();
            $(playerButtonSelector).attr('disabled', true);
        } else {
            $(startButtonId).hide();
            $(playerButtonSelector).attr('disabled', false);

            if (tempo == 1) {
                $(timerId).show();
                $(endPrimoTempoButtonId).show();
                $(startSecondoTempoButtonId).hide();
                $(endButtonId).hide();

                // init timer with
                startTimer(startTime);
            } else if (tempo == 2) {
                $(timerId).show();
                $(endPrimoTempoButtonId).hide();
                $(startSecondoTempoButtonId).hide();
                $(endButtonId).show();

                // init timer with
                startTimer(startTime);
            } else {
                $(endPrimoTempoButtonId).hide();
                $(startSecondoTempoButtonId).show();
                $(endButtonId).hide();
            }

        }

    }

    function initUIUnstarted() {
        $(endPrimoTempoButtonId).hide();
        $(startSecondoTempoButtonId).hide();
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


    function startMatch() {
        $(startButtonId).hide();
        $(endPrimoTempoButtonId).show();
        $(playerButtonSelector).attr('disabled', false);
    }


    function endMatch() {
        $(endButtonId).attr("disabled", true);
        $(playerButtonSelector).attr('disabled', true);
    }

    function pauseMatch() {
        endPrimoTempo($(timerId).data('match-id'));
        $(endPrimoTempoButtonId).hide();
        $(startSecondoTempoButtonId).show();
    }

    function restartMatch() {
        startSecondoTempo($(timerId).data('match-id'));
        startTimer();
        $(timerId).show();
        $(startSecondoTempoButtonId).hide();
        $(endButtonId).show();
    }

    function endMatchTime(matchId) {
        $.ajax({
            type: "POST",
            url: 'match_goals/' + matchId + '/end',
            data: {
                time: new Date().getTime()
            },
            success: function (data) {
            },
            error: function (data, error) {
                alert(error);
            }
        });
    }

    function endPrimoTempo(matchId) {
        $.ajax({
            type: "POST",
            url: 'match_goals/' + matchId + '/endprimotempo',
            data: {
                time: new Date().getTime()
            },
            success: function (data) {
            },
            error: function (data, error) {
                alert(error);
            }
        });
    }

    function startSecondoTempo(matchId) {
        $.ajax({
            type: "POST",
            url: 'match_goals/' + matchId + '/startsecondotempo',
            data: {
                time: new Date().getTime()
            },
            success: function (data) {
            },
            error: function (data, error) {
                alert(error);
            }
        });
    }

    function startTimer(startTime) {
        startTime = startTime || new Date().getTime();

        // Update the count down every 1 second
        timer = setInterval(function () {
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
        if (seconds < 10) {
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
            success: function (data) {
                // SUCCESS
                updateScores(data)
            },
            error: function (data, error) {
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
            success: function (data) {
                // SUCCESS
                updateScores(data)
            },
            error: function (obj, error) {
                alert(error);
            }
        });
    }

    function resetMatch(matchId) {
        if (confirm('Resettare partita?'))
            $.ajax({
                type: 'POST',
                url: 'match_goals/' + matchId + '/reset',
                success: function (data) {
                    location.reload();
                },
                error: function (obj, error) {
                    alert(error);
                }
            })
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
