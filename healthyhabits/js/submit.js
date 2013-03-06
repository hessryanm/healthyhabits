
$(function(){
	$("form").submit(function(){
		alert("Your changes have been recorded");
	});
	
	var today = parseInt($("body").data("day"));
	var this_week = $("body").data("week");
	if (this_week == "True") this_week = true;
	else this_week = false;
	console.log(this_week)
	$("form").each(function(){
		var day = parseInt($(this).data("daynum"));
		//{% if 2 < day_num - 1 or day_num < 2 or not this_week %}
		console.log("day: "+day+"; today: "+today)
		if (!this_week || day < today - 1 || today < day){
			$(this).find("input[type='checkbox']").attr("disabled", "disabled");
			$(this).find("input.day_submit").remove();
		}
	});
});