$(function () {
    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    var initArea = function () {
        console.log("ready!");
        var $playarea = $('#playarea');
        var cellSize = 60;
        var gameDimensions = 3;
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

        $('.cell').css('width', cellSize).css('height', cellSize).append('<span>O</span>');
    };

    initArea();
    $('.cell span').each(function () { $(this).css('color', getRandomColor())});

});