from django.urls import path

from . import views  # Import your views

urlpatterns = [
    # Main pages
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("shop/", views.shop, name="shop"),
    path("contact/", views.contact, name="contact"),
    path("messages/", views.messages_page, name="messages_page"),
    path("api/unread_count/", views.fetch_unread_count, name="fetch_unread_count"),
    path("book-appointment/", views.book_appointment, name="book_appointment"),
    path("login-required/", views.login_required_view, name="login_required"),
    # Product related
    path("product/<slug:slug>/", views.pro_details, name="product_details"),
    # path("filter_category/", views.category_products, name="category_products"),
    # Authentication
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),
    path("user-validate/<username>/<field>", views.user_validate, name="user_validate"),
    # Cart related
    path("cart/", views.carty, name="cart"),
    path("cart_count/", views.cart_count, name="cart_count"),
    path("addtocart/", views.add_to_cart, name="add_to_cart"),
    path("shopaddtocart/", views.shop_add_to_cart, name="shop_add_to_cart"),
    path("cart_data/", views.cart_data, name="cart_data"),
    # Payment
    path("proceed-to-pay/", views.razorpaycheck, name="proceed-to-pay"),
    path("proceed-to-paybuy/", views.proceed_to_pay_view, name="proceed_to_paybuy"),
    path(
        "place_order_petbuy/<int:pet_id>/",
        views.place_order_petbuy,
        name="place_order_petbuy",
    ),
    path("payment/callback/", views.payment_callback, name="payment_callback"),
    path("order-success/", views.order_success, name="order-success"),
    # Order related
    path("search-view/", views.search_view, name="search_view"),
    path(
        "update-cart-item/<int:item_id>/",
        views.update_cart_item,
        name="update_cart_item",
    ),
    path(
        "remove-from-cart/<int:item_id>/",
        views.remove_from_cart,
        name="remove_from_cart",
    ),
    path("checkout/", views.checkout, name="checkout"),
    path("checkoutpet/", views.checkoutpet, name="checkoutpet"),
    path("checkpet/", views.checkpet, name="checkpet"),
    path("check/", views.check, name="check"),
    path("checkbuy/", views.checkbuy, name="checkbuy"),
    path("checkpet/", views.checkpet, name="checkpet"),
    path("buy-now/", views.buy_now, name="buy_now"),
    path(
        "place_order_checkout/", views.place_order_checkout, name="place_order_checkout"
    ),
    path(
        "placeorder_buynow/<int:product_id>/",
        views.place_order_buynow,
        name="placeorder_buynow",
    ),
    # path("/proceed-to-pay/", views.razorpaycheck),
    path("view-orders/<str:t_no>", views.myorders, name="order_view"),
    path("orderslist/", views.order_list, name="orderslist"),
    # Pet related
    path("petbreed/", views.petbreed, name="petbreed"),
    path("petadopt/", views.petadopt, name="petadopt"),
    path("shophome/", views.shophome, name="shophome"),
    path("petshop/", views.petshop, name="petshop"),
    path("petsdetails/<int:pet_id>/", views.petsdetails, name="petsdetails"),
    # Adoption related
    path("petadoption/", views.petadoption, name="petadoption"),
    path("adoptionview/<slug:slug>/", views.adoption_view, name="adoptionview"),
    path("adoptionrequest/<slug:slug>/", views.adoptionrequest, name="adoptionrequest"),
    path(
        "adoptionrequestsend/<int:pet_id>/",
        views.adoption_request_send,
        name="adoptionrequestsend",
    ),
    #Pages
    path("ourteam/", views.ourteam, name="ourteam"),
    path("gallery/", views.gallery, name="gallery"),
    path("faq/", views.faq, name="faq"),
    path("teamdetails/", views.teamdetails, name="teamdetails"),
    path("blog/", views.blog, name="blog"),
    path("ourblog/",views.ourblog,name="ourblog"),
    path("change_password/", views.change_password, name="change_password"),
]
