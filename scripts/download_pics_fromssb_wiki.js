function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

var images = document.getElementsByTagName('img');


var lastChar = "";
var costidx = 0;
for (var i = 0; i < images.length; ++i) {
    if (!images[i].src.includes("Head")) continue;


    //****NOTE THIS MAKES PACMAN DOWNLOAD AS "MAN"******
    var curChar = images[i].src.substring(images[i].src.lastIndexOf("-") + 1, images[i].src.lastIndexOf("Head"))

    if (curChar != lastChar) {
        costidx = 0;
        lastChar = curChar;
    }
    else {
        costidx++;
    }

    var link = document.createElement("a");
    link.id = i;
    link.download = curChar + "" + costidx;
    link.href = images[i].src;
    link.click();
    await sleep(1500);
}