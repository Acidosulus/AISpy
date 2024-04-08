try {
	document.querySelector(`#designer_ul_run_button`)
	.addEventListener('click', function() {
		// RunInScreenForm(`ul_designer_form`, `GetSourceFromServer();GetSourceFromServerParameters();`,`/reports_builder_ul`);
		RunInScreenForm(
		{
			form_name : "report_designer_ul",
			execute_after_load : "GetSourceFromServer();GetSourceFromServerParameters();",
			request_link : "/reports_builder_ul"
		}
		);
	});
  } catch (error) {	console.error("Event bind error:", error); }