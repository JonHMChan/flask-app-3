// Your code starts here
$(document).ready(function() {
    $.ajax({
        method: "GET",
        url: "/api" + window.location.pathname,
        success: function(data) {

            // Update edit link so it goes to the correct page
            $(".edit").attr("href", `/teams/${data.id}/edit`);

            // Bind an API call to delete the team
            $(".delete").click(function() {
                $.ajax({
                    url: `/api/teams/${data.id}`,
                    method: "DELETE",
                    success: function() {
                        // Once deleted, redirect the user to the home page
                        window.location.href = "/";
                    }
                })
            })
            
            // Add team name
            $(".team-name").html(data.name);
            
            // Add description
            $(".team-description").text(data.description);

            // Add team members
            for (var j = 0; j < data.members.length; j++) {
                var member = data.members[j];

                // Insert markup to the container BEFORE the API call with the right member ID
                // This part is tricky because of the team member's level - you can't get it from /api/pokemon/:id
                $(".team-pokemon").append(`
                    <tr class="team-member-${member.pokemon_id}">
                        <td><img class="pokemon-image" /></td>
                        <td><a class="pokemon" href="/pokemon/${member.pokemon_id}"></a></td>
                        <td class="level">${member.level}</td>
                        <td class="types"></td>
                    </tr>
                `)
                $.ajax({
                    method: "GET",
                    url: "/api/pokemon/" + member.pokemon_id,
                    success: function(pokemon) {
                        // Add pokemon information based on ID
                        // Note: the pokemon's level is not set here! It's done before the API call
                        $member = $(".team-member-" + pokemon.id);
                        $member.find("img").attr("src", pokemon.image_url);
                        $member.find("a").text(pokemon.name);
                        $member.find(".types").text(pokemon.types);
                    }
                });
                
            }
        }
    })
})