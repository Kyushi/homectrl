// Close button
$(".close").on("click", function() {
  $(this).parent().remove();
});

// Function to scan for new buetooth thermostats
function scanForDevices() {
    $.get($base_url + 'heater/register/scan', function(data) {
		console.log(data);
	}
    )
}

function startAiring() {
    $.post($base_url + 'air/start', function(data) {
	    console.log("Airing apartment");
            $("#response").text(data);
	    console.log(data);
    });
}

function stopAiring() {
    $.post($base_url + 'air/end', function(data) {
	    console.log("Setting back to auto");
            $("#response").text(data);
	    console.log(data);
    });
}

