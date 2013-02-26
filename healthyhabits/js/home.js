
$(function(){
	$("#change_name").click(change_name_click);
});

function change_name_click(){
	$(this).before("<input type='text' placeholder='New Name' id='new_name' />");
		$(this).val("Submit");
		$(this).unbind();
		$(this).click(function(){
			var name = $("#new_name").val();
			if (name == "") return;
			var self = this;
			$.ajax({
				url: "/",
				type: "POST",
				data: {name: name},
				dataType: "json",
				success:function(response){
					if (response.result){
						var oldname = $("#uname").html();
						$("#uname").html(name);
						$(".person_info").each(function(){
							if ($(this).find(".name").html().trim() == oldname) $(this).children(":first").html(name)
						});
						$(self).val("Change Name").unbind().click(change_name_click).prev().remove();
					}
				}
			});
		})
}