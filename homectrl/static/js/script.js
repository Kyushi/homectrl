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

