// Your code starts here
$(document).ready(function() {
    var team = {
        name: "",
        description: "",
        members: []
    }

    var searchResults = [];

    $(".js-search").keyup(function() {
        var _value = $(this).val();
        if (_value.length > 0) {
            $.ajax({
                method: "GET",
                url: `/api/pokemon?search=${_value}`,
                success: function(data) {
                    searchResults = data.map(function(pokemon) {
                        pokemon.member = {
                            pokemon_id: pokemon.id,
                            level: 1
                        };
                        pokemon.html = `
                            <tr>
                                <td><img class="pokemon-image" src="${pokemon.image_url}" /></td>
                                <td><a href="/pokemon/${pokemon.id}">${pokemon.name}</a></td>
                                <td><input type="text name="level" class="js-level" value="1" /></td>
                                <td>${pokemon.types.join(", ")}</td>
                            </tr>
                        `;
                        return pokemon;
                    });
                    renderSearchResults();
                }
            })
        }
    }).keypress(function(event) {
        if (event.which === 13 && searchResults.length > 0) {
            event.preventDefault();
            var pokemon = searchResults[0];
            $(".team-pokemon").append(pokemon.html);
            team.members.push(pokemon.member)
            return;
        }
    });

    function renderSearchResults() {
        var html = "";
        for (var i = 0; i < searchResults.length; i++) {
            var result = searchResults[i];
            html += `
                <div class="search-result${i===0 ? " search-result--active" : ""}">
                    <p>${result.name}</p>
                </div>
            `;
        }
        $(".js-search-results").html(html);
    }

    $(".js-form").submit(function(event) {
        event.preventDefault();
        $(".js-level").each(function(index) {
            team.members[index].level = parseInt($(this).val());
        })
        team.name = $(".js-name").val();
        team.description = $(".js-description").val();
        $.ajax({
            method: "POST",
            url: "/api/teams",
            data: JSON.stringify(team),
            contentType: "application/json",
            success: function() {
                window.location.href="/";
            }
        })
        return false;
    })
})