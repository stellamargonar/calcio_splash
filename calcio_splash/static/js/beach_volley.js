(function ($) {
    var timerId = '#beach_match_timer';
    var setButtonsIdTemplate = '#beach_button_set';
    var resetButtonId = '#beach_button_reset';
    var teamButtonSelector = '.team-player.btn';
    var currentSet = $(timerId).data('current-set');
    $(function () {

        for (var i=1; i<4; i++) {
            $(setButtonsIdTemplate + i).bind('click', function (event) {
                setCurrentSet(event.target.id.charAt(setButtonsIdTemplate.length - 1));
            });
        }
        $(resetButtonId).bind('click', function (event) {
            resetMatch($(timerId).data('match-id'));
        });

        $(teamButtonSelector).click(function () {
            score($(this).data('team'), $(this).data('match'));
        });
        $(teamButtonSelector).on('taphold', function (event) {
            event.stopPropagation();
            if (confirm('Eliminare ultimo punto?'))
                deleteScore($(this).data('team'), $(this).data('match'));
        });

        var csrftoken = getCookie('csrftoken');
        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });


        initUI();
    });

    function initUI() {
        for (var i=1; i<4; i++) {
            $('#team-score-set' + i).hide();
        }
        setCurrentSet(currentSet);
    }

    function setCurrentSet(set) {
        console.log('Click', set);
        currentSet = set;
        $(setButtonsIdTemplate + set).addClass('btn-success');
        $('#team-score-set' + set).show('');
        startSet($(timerId).data('match-id'), set);

        for (var j = 1; j < 4; j++) {
            if (j != parseInt(set)) {
                $(setButtonsIdTemplate + j).removeClass('btn-success');
            }
            if (j > parseInt(set)) {
                $('#team-score-set' + j).hide();
            } else {
                $('#team-score-set' + j).show();
            }
        }

    }

    function startSet(matchId, set) {
        $.ajax({
            type: "POST",
            url: 'match_beach/' + matchId + '/startset/' + set,
            success: function (data) {
                // SUCCESS
                updateContext(data)
            },
            error: function (data, error) {
                alert(error);
            }
        });
    }

    function score(teamId, matchId) {
        $.ajax({
            type: "POST",
            url: 'match_beach/' + matchId + '/score_beach',
            data: {
                team: teamId,
                set: currentSet,
            },
            success: function (data) {
                // SUCCESS
                updateContext(data)
            },
            error: function (data, error) {
                alert(error);
            }
        });
    }

    function deleteScore(teamId, matchId) {
        $.ajax({
            type: "POST",
            url: 'match_beach/' + matchId + '/undo',
            data: {
                team: teamId,
                set: currentSet,
            },
            success: function (data) {
                // SUCCESS
                updateContext(data)
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
                url: 'match_beach/' + matchId + '/reset',
                success: function (data) {
                    location.reload();
                },
                error: function (obj, error) {
                    alert(error);
                }
            })
    }


    function updateContext(data) {
        $('#team-score-set1').text(data.match.team_a_set_1 + ' - ' + data.match.team_b_set_1)
        $('#team-score-set2').text(data.match.team_a_set_2 + ' - ' + data.match.team_b_set_2)
        $('#team-score-set3').text(data.match.team_a_set_3 + ' - ' + data.match.team_b_set_3)
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
