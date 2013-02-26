var highest = 0;

$(function(){
	$(".total").each(function(){
		var val = $(this).html();
		val = parseInt(val);
		if (val == highest) {
			var user = $(this).closest("tr").children(":first").text();
			if ($(".winning").text() != "") $(".winning").append("<br/>");
			$(".winning").append(user);
		} else if (val > highest){
			highest = val;
			var user = $(this).closest("tr").children(":first").text();
			$(".winning").text(user);
		} 
	});
});