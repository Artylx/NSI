var btn_left = document.querySelector('.left-button');
var btn_right = document.querySelector('.right-button');
var veiwer = document.querySelector('.veiwer');

var list_img = veiwer.querySelectorAll('img');
var img_width = list_img[0].style.display = 'block';

function scrool(direction) {
    for (var i = 0; i < list_img.length; i++) {
        if (list_img[i].style.display === 'block') {
            list_img[i].style.display = 'none';
            if (direction === 'left') {
                if (i === 0) {
                    list_img[list_img.length - 1].style.display = 'block';
                }
                else {
                    list_img[i - 1].style.display = 'block';
                }
            }
            else if (direction === 'right') {
                if (i === list_img.length - 1) {
                    list_img[0].style.display = 'block';
                }
                else {
                    list_img[i + 1].style.display = 'block';
                }
            }
            break;
        }
    }
};

btn_left.addEventListener('click', function() {
    scrool('left');
});

btn_right.addEventListener('click', function() {
    scrool('right');
});

