var EDITOR = {
	init: function() {
		// EDITOR.elements = $(".rw_editor");
		// console.log(EDITOR.elements);
		$(".rw_editor").click(EDITOR.click);
		// EDITOR.elements.mouseOver
		$(document.body).append('<link rel="stylesheet" type="text/css" href=' + "/static/css/editorstyle.css" + '>');
	},
	click: function(event) {
		EDITOR.modal.create(this);

	},
	modal: {
		target: null,
		create: function(element) {
			EDITOR.modal.target = element;

			var cover = document.createElement("div"),
				form = document.createElement("form"),
				textArea = document.createElement("textarea"),
				cancle = document.createElement("button");

			cover.id = "cover";
			$(cover).click(EDITOR.modal.exit);

			textArea.value = element.innerHTML;

			cancle.innerHTML = "cancle";
			$(cancle).click(EDITOR.modal.cancle);



			form.appendChild(textArea);
			form.appendChild(cancle);
			cover.appendChild(form);
			document.body.appendChild(cover);

		},
		exit: function(event) {
			if (event.target.nodeName != "FORM") {
				event.preventDefault();
				return false;
			}
			$.ajax({
				type: "POST",
				data: "data",
				success: function(data) {
					alert("worked")
				},
				dataType: "json"
			});
			console.log(EDITOR.modal.target)
			EDITOR.modal.target.innerHTML = $("#cover textarea").val();
			$("#cover").remove();
		},
		cancle: function() {
			$("#cover").remove();
		}
	}
}

function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
		var cookies = document.cookie.split(';');
		for (var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);
			// Does this cookie string begin with the name we want?
			if (cookie.substring(0, name.length + 1) == (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}
	return cookieValue;
}
var csrftoken = getCookie('csrftoken');

EDITOR.init();