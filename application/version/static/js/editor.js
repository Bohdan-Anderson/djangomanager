var EDITOR = {
	init: function() {
		// EDITOR.elements = $(".rw_editor");
		// console.log(EDITOR.elements);
		EDITOR.cookies();
		$(".rw_editor").each(EDITOR.bindCount);
		$(".rw_editor").click(EDITOR.click);
		// EDITOR.elements.mouseOver
		$(document.body).append('<link rel="stylesheet" type="text/css" href=' + "/static/css/editorstyle.css" + '>');
	},
	bindCount: function(count, element) {
		$(element).data({
			"count": count
		})
	},
	click: function(event) {
		EDITOR.modal.count = $(this).data().count
		EDITOR.modal.create(this);

	},
	modal: {
		target: null,
		count: null,
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
			textArea.select();

		},
		exit: function(event) {
			if (event.target.nodeName != "FORM") {
				event.preventDefault();
				return false;
			}
			EDITOR.modal.target.innerHTML = $("#cover textarea").val();

			$.ajax({
				type: "POST",
				data: {
					"count": EDITOR.modal.count,
					"content": EDITOR.modal.target.innerHTML
				},
				success: function(data) {
					alert("worked")
				},
				dataType: "json"
			});

			$("#cover").remove();
		},
		cancle: function() {
			$("#cover").remove();
		}
	},
	cookies: function() {
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

		function csrfSafeMethod(method) {
			// these HTTP methods do not require CSRF protection
			return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
		}
		$.ajaxSetup({
			beforeSend: function(xhr, settings) {
				if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}
			}
		});
	}
}


EDITOR.init();