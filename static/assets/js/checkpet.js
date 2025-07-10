$(document).ready(function () {
  // Function to handle Cash on Delivery (COD) payment
  $(".payWithCash").click(function (e) {
    e.preventDefault();

    // Collect form data
    var fname = $("[name='fname']").val();
    var lname = $("[name='lname']").val();
    var address = $("[name='address']").val();
    var state = $("[name='state']").val();
    var city = $("[name='city']").val();
    var pincode = $("[name='pincode']").val();
    var phone = $("[name='phone']").val();
    var email = $("[name='email']").val();
    var pet_id = $("[name='pet_id']").val();
    var quantity = $("[name='quantity']").val();

    // Validate required fields
    if (
      !fname ||
      !lname ||
      !address ||
      !state ||
      !city ||
      !pincode ||
      !phone ||
      !email
    ) {
      Swal.fire({
        icon: "error",
        title: "Alert",
        text: "All fields are required!",
        footer: '<a href="#">Why do I have this issue?</a>',
      });
      return false;
    }

    // AJAX call to place the order for COD
    $.ajax({
      method: "POST",
      url: "/place_order_petbuy/" + pet_id + "/",
      data: {
        fname: fname,
        lname: lname,
        address: address,
        state: state,
        city: city,
        pincode: pincode,
        phone: phone,
        email: email,
        quantity: quantity,
        payment_mode: "Cash on Delivery",
        status: "Ready for Shipment",
        payment_status: "Pending",
        csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val(),
      },
      success: function () {
        window.location.href = "/order-success/";
      },
      error: function (xhr, status, error) {
        console.error("AJAX Error: ", error);
        Swal.fire({
          icon: "error",
          title: "Error",
          text: "There was an error processing your order. Please try again.",
        });
      },
    });
  });
});
