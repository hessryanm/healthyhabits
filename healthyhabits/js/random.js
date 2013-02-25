
function getRandomPerson() {
	
	var people = [];
	$(".person_info").each(function(){
		var name = $(this).find(".name").text();
		var weight = parseInt($(this).find(".total").text());
		people.push([name, weight]);
	});
	console.log(people);
	
    var totalWeight = 0, cumWeight = 0, i;
    // sum up the weights
    for (i = 0; i < people.length; i++) {
        totalWeight += (people[i][1] * people[i][1]);
    }
    var random = Math.floor(Math.random() * totalWeight);
    // now find which bucket out random value is in

    for (i = 0; i < people.length; i++) {
        cumWeight += (people[i][1] * people[i][1]);
        if (random < cumWeight) {
            $(".winner_box").html(people[i][0]);
            return;
        }
    }
}