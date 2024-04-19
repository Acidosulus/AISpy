	const EventsBindener = {

		designer_ul_run_button: function(){
			RunInScreenForm(
				{
					form_name : "report_designer_ul",
					execute_after_load : "GetSourceFromServer();GetSourceFromServerParameters();",
					request_link : "/reports_builder_ul"
				}
				);
		},

		services_button: function(){
			RunInScreenForm(
				{
					form_name : "db_services_form",
					execute_after_load : "EventsBindener.assignOnClickToMatchingElement();",
					request_link : "/db_services",
					execute_on_cancel:'CloseToplevelDynamicForm();'
				}
				);
		},
		

	
		ul_db_regain_statistic: function(){
			asyncRequest(`/ul_regain_statistic`,'GET');
			CloseToplevelDynamicForm();
		},

















	    assignOnClickToMatchingElement: function() {
			for (let methodName in this) {
				if (typeof this[methodName] === 'function') {
					const element = document.getElementById(methodName);
					if (element) {
						element.onclick = this[methodName].bind(this);
					}
				}
			}
		}
	};
	
	