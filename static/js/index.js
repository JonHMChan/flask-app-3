// Your code starts here
$(document).ready(function() {
    $.ajax({
        method: "GET",
        url: "/api/pokemon",
        success: function(data) {
            for (var i = 0; i < data.length; i++) {
                var pokemon = data[i];
                var $pokemon = $(`<a href="/pokemon/${pokemon.id}"></a>`).addClass("pokemon");
                var html = `
                    <h3>${pokemon.name}</h3>
                    <img class="pokemon-image" src=${pokemon.image_url} />
                `;
                $pokemon.append(html);
                $(".pokemon-container").append($pokemon);
            }
        }
    });

    $.ajax({
        method: "GET",
        url: "/api/teams",
        success: function(data) {
            for (var i = 0; i < data.length; i++) {
                var team = data[i];
                var $team = $(`<a href="/teams/${team.id}"></a>`).addClass("team");
                var html = `
                    <h3>${team.name}</h3>
                `;
                $team.append(html);
                $(".teams-container").append($team);
            }
        }
    });
})