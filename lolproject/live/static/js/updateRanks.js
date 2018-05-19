//Updates all ranks on the page!
//only works for live (or any other page with the same structure)

//prepare the tooltip hover stuff
$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
});




var ranks = document.getElementsByClassName("rank");

queue = []

function createCallback(item) {
    return function(data) {
        update(data, item);
    };
}

icons = {
    UNRANKED: 0,
    BRONZE: 1,
    SILVER: 2,
    GOLD: 3,
    PLATINUM: 4,
    DIAMOND: 5,
    MASTER: 6,
    CHALLENGER: 7
};

function update(data, a) {
    nodes = a.nodes;
    nodes[1].innerHTML = "Level " + data.level;
    nodes[3].innerHTML = data.tier + " " + data.rank;
    nodes[3].setAttribute("title", data.leagueName);

    bg = a.background;
    bg.setAttribute("title", data.leagueName);
    bg.style.backgroundImage = "url('/static/tier-icons.png')";
    bg.style.backgroundPositionX = (icons[data.tier] * -42) + "px";
}

for (i = 0; i < ranks.length; i++) {
    var id = ranks[i].getAttribute('id');
    var nodes = ranks[i].childNodes;
    data = {
        'id': id,
        'nodes': nodes,
        'background': ranks[i]
    };
    queue.push(data);
}

for (i = 0; i < queue.length; i++)
    $.getJSON("getLeague?summoner=" + queue[i]['id'], createCallback(queue[i]));