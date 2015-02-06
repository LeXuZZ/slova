/**
 * Created by lxz on 2/1/15.
 */
$(function () {
    var host = window.location.host;
    var ws = new WebSocket("ws://" + host + "/ws");


    var initArea = function () {
        console.log("ready!");
        var $playarea = $('#playarea');
        var cellSize = 60;
        var gameDimensions = 8;
        var $rowCache = [];

        $playarea.css('width', gameDimensions * cellSize);
        $playarea.css('height', gameDimensions * cellSize);

        for (var i = 0; i < gameDimensions; i++) {
            $playarea.append('<span id="row' + i + '">');
        }

        for (i = 0; i < gameDimensions; i++) {
            $rowCache[i] = $('#row' + i);

            for (var j = 0; j < gameDimensions; j++) {
                $rowCache[i].append('<div id="' + j + '-' + i + '" class="cell" style="top:' + i * cellSize + 'px; left:' + j * cellSize + 'px;" ></div>');
            }
        }

        $('.cell').css('width', cellSize).css('height', cellSize);
    };

    initArea();

    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    var fillGrid = function (grid) {
        var gd = 8;
        var wc = 10;
        var colorList = [];
        for (var c = 0; c < wc; c ++) {
            colorList.push(getRandomColor());
        }
        for (var i = 0; i < gd; i ++) {
            var color = getRandomColor();
            var row = grid[i];
            for (var j = 0; j < gd; j ++) {
                $('div#' + i + '-' + j + '.cell').append('<span>' + row[j].letter.value + '</span>').css('background-color', colorList[row[j].letter.value]);
                //$('div#' + i + '-' + j + '.cell span').css('color', colorList[row[j].letter.value]);
            }
        }

    };

    var addLetterToCell = function (msg) {
        $('div#0-0.cell').append('<span>' + msg["0"]["0"].letter.value + '</span>')
    };

    ws.onmessage = function (msg) {
        //console.log('message is: ' + msg.data);
        var message = $.parseJSON(msg.data);
        //addLetterToCell(message);
        fillGrid(message)
    };

});