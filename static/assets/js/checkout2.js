$(document).ready(function () {
  // Function to handle online payment
  $(".payWithOnline").click(function (e) {
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
        title: "Alert..",
        text: "All fields are required!",
        footer: '<a href="#">Why do I have this issue?</a>',
      });
      return false;
    } else {
      // AJAX call to get the order ID
      $.ajax({
        method: "GET",
        url: "/proceed-to-paybuy/",
        success: function (response) {
          if (response.total_prices) {
            var options = {
              key: "rzp_test_MFikh57HLh7CDc", // Replace with your Razorpay Key ID
              amount: response.total_prices * 100, // Amount in paise (e.g., 50000 paise = 500 INR)
              currency: "INR",
              name: "Petparadise",
              description: "Thank you for shopping with us",
              image: "{% static 'assets/img/logo/logos_icon.png' %}", // Replace with your logo URL
              handler: function (payment_response) {
                $.ajax({
                  method: "POST",
                  url: "/placeorder_buynow/",
                  data: {
                    fname: fname,
                    lname: lname,
                    address: address,
                    state: state,
                    city: city,
                    pincode: pincode,
                    phone: phone,
                    email: email,
                    payment_mode: "Paid by Razorpay",
                    status: "Ready to Shipment",
                    payment_status: "Success",
                    razorpay_payment_id: payment_response.razorpay_payment_id,
                    csrfmiddlewaretoken: $(
                      "input[name='csrfmiddlewaretoken']"
                    ).val(),
                  },
                  success: function (response) {
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
              },
              prefill: {
                name: fname,
                email: email,
                contact: phone,
              },
              theme: {
                color: "#3399cc",
              },
            };

            var rzp1 = new Razorpay(options);
            rzp1.open();
          } else {
            console.error(
              "No valid response received from server for total price."
            );
          }
        },
        error: function (xhr, status, error) {
          console.error("AJAX Error: ", error);
        },
      });
    }
  });

  // Function to handle Cash on Delivery (COD) payment
  $(".payWithCod").click(function (e) {
    e.preventDefault();

    var fname = $("[name='fname']").val();
    var lname = $("[name='lname']").val();
    var address = $("[name='address']").val();
    var state = $("[name='state']").val();
    var city = $("[name='city']").val();
    var pincode = $("[name='pincode']").val();
    var phone = $("[name='phone']").val();
    var email = $("[name='email']").val();

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
        title: "Alert..",
        text: "All fields are required!",
        footer: '<a href="#">Why do I have this issue?</a>',
      });
      return false;
    }

    // AJAX call to place the order for COD
    $.ajax({
      method: "POST",
      url: "/placeorder_buynow/",
      data: {
        fname: fname,
        lname: lname,
        address: address,
        state: state,
        city: city,
        pincode: pincode,
        phone: phone,
        email: email,
        payment_mode: "Cash on Delivery",
        status: "Ready to Shipment",
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
