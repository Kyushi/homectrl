console.log($SCRIPT_ROOT)
// Close button
$(".close").on("click", function() {
  $(this).parent().remove();
});

// Funciton to scan for new buetooth thermostats
function scanForDevices() {
    $.ajax({
        type: 'GET',
        url: $SCRIPT_ROOT + ''

    })
}

// Function to check if public category exists already
function catNameCheck() {
  // If "make public" is checked, check for duplicate name
  if ($("#new-public").prop("checked")) {
    $catName = $("#newcategory").val();
    // If we're on the edit category name page, pass category id to backend
    if ($("#cat-id").length) {
      $catId = $("#cat-id").val()
      $data = {catname: $catName, catid: $catId}
    }
    // If not editing category name, there is no ID to pass
    else {
      $data = {catname: $catName}
    }
    // Use Ajax to check category name in the background.
    $.ajax({
      type: 'POST',
      url: $base_url + '/checkcatname/',
      data: JSON.stringify($data),
      contentType: 'application/json; charset=utf-8',
      success: function(result) {
        if(result != "OK"){
          // If the public category already exists, disable submit and display
          // error.
          $("#catname-warning").html("A public category with this name already \
                                      exists. Please choose a different name.");
          $("#submit").prop("disabled", true);
          $("#submit").css("background-color", "#aaa")
        }
        else {
          // If all is good, make sure submit is enabled and everything looks
          // normal
          $("#catname-warning").html("");
          $("#submit").prop("disabled", false);
          $("#submit").css("background-color", "");
        }
      }
    });
  }
  else {
    // If "make public" is not checked, make sure that form looks normal and
    // submit is enabled.
    $("#catname-warning").html("");
    $("#submit").prop("disabled", false);
    $("#submit").css("background-color", "");
  }
}

// Trigger above function on either clicking the checkbox or leaving the text
// input field.
$("#new-public").on("change", catNameCheck);
$("#newcategory").on("blur", catNameCheck);
