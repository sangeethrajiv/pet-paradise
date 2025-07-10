from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import*
import datetime
from django.contrib.auth.forms import PasswordChangeForm

# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(
#         max_length=254, help_text="Required. Enter a valid email address."
#     )
#     address = forms.CharField(max_length=255, help_text="Required. Enter your address.")
#     phone = forms.CharField(
#         max_length=20, help_text="Required. Enter your phone number."
#     )

#     class Meta:
#         model = User
#         fields = ("username", "email", "password1", "password2", "address", "phone")

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Enter your username"}
#         )
#         self.fields["email"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Enter your email"}
#         )
#         self.fields["password1"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Enter your password"}
#         )
#         self.fields["password2"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Confirm your password"}
#         )
#         self.fields["address"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Enter your address"}
#         )
#         self.fields["phone"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Enter your phone number"}
#         )

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.email = self.cleaned_data["email"]
#         if commit:
#             user.save()
#         return user


# class LoginForm(forms.Form):
#     username = forms.CharField(max_length=100)
#     password = forms.CharField(widget=forms.PasswordInput())


#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Enter your username"}
#         )
#         self.fields["password"].widget.attrs.update(
#             {"class": "form-control", "placeholder": "Enter your password"}
#         )

# In forms.py


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    country = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=10)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    ship_to_different_address = forms.BooleanField(required=False)
    order_notes = forms.CharField(widget=forms.Textarea, required=False)
    agree_terms = forms.BooleanField()
    payment_method = forms.ChoiceField(
        choices=(
            ("direct_bank_transfer", "Direct Bank Transfer"),
            ("check_payments", "Check Payments"),
            ("cash_on_delivery", "Cash on Delivery"),
        )
    )
    shipping_method = forms.ChoiceField(
        choices=(
            ("flat_rate", "Flat Rate: $5.00"),
            ("free_shipping", "Free Shipping"),
            ("local_pickup", "Local Pickup"),
        )
    )


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['name', 'pet_type', 'interest', 'date', 'time', 'phone']


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "species" in self.data:
            try:
                species_id = int(self.data.get("species"))
                self.fields["breed"].queryset = Breed.objects.filter(
                    species_id=species_id
                ).order_by("name")
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields["breed"].queryset = self.instance.species.breeds.order_by(
                "name"
            )

# shop/pets/forms.py


# class AdoptionRequestForm(forms.Form):
#     full_name = forms.CharField(label="Full Name")
#     email = forms.EmailField(label="Email",)
#     phone = forms.CharField(label="Phone",)
#     appointment_date = forms.DateField(
#         label="Appointment Date",
#         widget=forms.DateInput(attrs={"type": "date"}),
#     )
#     species = forms.ChoiceField(
#         label="Species", choices=[("Cat", "Cat"), ("Dog", "Dog")],
#     )
#     breed = forms.ChoiceField(
#         label="Breed", choices=[],
#     )  # Populate choices dynamically
#     pet_id = forms.ChoiceField(
#         label="Pet ID", choices=[],
#     )  # Populate choices dynamically
#     comment = forms.CharField(
#         label="Special Note", widget=forms.Textarea, required=False
#     )

#     # Custom validation can be added here if necessary
#     def clean_phone(self):
#         phone = self.cleaned_data.get("phone")
#         # Example validation: Check phone number length
#         if len(phone) < 10:
#             raise forms.ValidationError("Phone number must be at least 10 digits long.")
#         return phone

#     def clean_email(self):
#         email = self.cleaned_data.get("email")
#         # Example validation: Check email uniqueness or format
#         # Assuming you have a user model, adjust accordingly
#         if not "@" in email:
#             raise forms.ValidationError("Enter a valid email address.")
#         return email

#     def clean_appointment_date(self):
#         appointment_date = self.cleaned_data.get("appointment_date")
#         # Example validation: Ensure the date is not in the past
#         if appointment_date and appointment_date < datetime.date.today():
#             raise forms.ValidationError("Appointment date cannot be in the past.")
#         return appointment_date


class AdoptionRequestForm(forms.Form):
    fullname = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    appointment_date = forms.DateField()
    species = forms.ChoiceField(choices=[("Cat", "Cat"), ("Dog", "Dog")])
    breed = forms.CharField(max_length=100)
    comment = forms.CharField(widget=forms.Textarea, required=False)
    petadopt_id = forms.IntegerField(widget=forms.HiddenInput())


class CustomPasswordChangeForm(PasswordChangeForm):
    # Customize the form if needed
    old_password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Current Password"})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm New Password"})
    )

    class Meta:
        model = User
        fields = ["old_password", "new_password1", "new_password2"]
