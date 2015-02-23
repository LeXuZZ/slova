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
                $rowCache[i].append('<div id="' + i + '-' + j + '" class="cell noselect" style="top:' + i * cellSize + 'px; left:' + j * cellSize + 'px;" ></div>');
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
        for (var c = 0; c < wc; c++) {
            colorList.push(getRandomColor());
        }
        for (var i = 0; i < gd; i++) {
            var color = getRandomColor();
            var row = grid[i];
            for (var j = 0; j < gd; j++) {
                $('div#' + i + '-' + j + '.cell').append('<span>' + row[j].letter.value + '</span>').css('background-color', colorList[row[j].letter.value]);
                //$('div#' + i + '-' + j + '.cell span').css('color', colorList[row[j].letter.value]);
            }
        }

    };

    ws.onmessage = function (msg) {
        //console.log('message is: ' + msg.data);
        var message = $.parseJSON(msg.data);
        fillGrid(message)
    };

    //$('div.cell').on("mouseenter mouseleave", function (e) {
    //    $(this).toggleClass('selected', e.type == 'mouseenter');
    //});


    //var elem_list = [];
    //$('div.cell').on('mousedown', function (e) {
    //    $(this).addClass('selected');
    //    $('div.cell').one('mouseenter.c', function (e) {
    //        $(this).toggleClass('selected', e.type == 'mouseenter.c');
    //        elem_list.push(this)
    //    });
    //}).on('mouseup', function (e) {
    //    elem_list.forEach(function (elem) {
    //        $(elem).toggleClass('selected')
    //    });
    //    $('div.cell').on('mouseenter.c');
    //    elem_list = []
    //});
    var if_elem_nearby = function (id1, id2) {
        var id1 = [id1[0], id1[2]];
        var id2 = [id2[0], id2[2]];
    };

    var tmp_elem;
    var elem_list = [];
    var handler = function () {
        if (!tmp_elem.isNaN() && if_elem_nearby(this, tmp_elem)) {
            $(this).addClass('selected');
            elem_list.push(this);
            tmp_elem = this;
            console.log($(tmp_elem).attr('id'))
        }
    };
    $('div.cell').mousedown(function () {
        $(this).addClass('selected');
        elem_list.push(this);
        tmp_elem = this;
        console.log($(tmp_elem).attr('id'));
        $('div.cell').on('mouseenter.с', handler)
    }).mouseup(function () {
        elem_list.forEach(function (elem) {
            //console.log(elem);
            $(elem).removeClass('selected')
        });
        $('div.cell').off('mouseenter.с', handler)
    })
});