from django.db import models,transaction
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.conf import settings
import uuid,random
from django.utils import timezone


class MainCategory(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title[:40]


class Category(models.Model):
    title = models.CharField(max_length=255)
    maincategory = models.ForeignKey(
        MainCategory, related_name="categories", null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class SubCategory(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        Category, related_name="subcategories", null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title[:40]


class Product(models.Model):
    title = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, null=True, on_delete=models.DO_NOTHING)
    price = models.PositiveBigIntegerField(default=0, null=True)
    discount = models.PositiveIntegerField(default=0, null=True)
    discount_price = models.PositiveBigIntegerField(default=0, null=True)
    featured_image = models.CharField(max_length=255, null=True)
    total = models.PositiveIntegerField(default=0, null=True)
    available = models.PositiveIntegerField(default=0, null=True)
    description = RichTextField(null=True, blank=True)
    product_information = RichTextField(null=True, blank=True)
    tags = models.CharField(max_length=555, null=True, blank=True)
    slug = models.CharField(max_length=555, null=True, blank=True)
    quantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.title

    @property
    def discounted_price(self):
        if self.discount > 0:
            discount_amount = (self.discount / 100) * self.price
            return self.price - discount_amount
        return self.price

    def save(self, *args, **kwargs):
        self.discount_price = self.discounted_price
        super().save(*args, **kwargs)


@receiver(pre_save, sender=Product)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title)
        unique_slug = base_slug
        num = 1
        while Product.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        instance.slug = unique_slug


class Addtional_information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=True, blank=True)
    spec = models.CharField(max_length=255, null=True, blank=True)


class Additional_image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.CharField(max_length=555, null=True, blank=True)


class userAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user} "


class Species(models.Model):
    name = models.CharField(
        max_length=50, unique=True, help_text="Enter the species name (e.g., Dog, Cat)"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Species"
        verbose_name_plural = "Species"
        ordering = ["name"]


class Breed(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the breed name")
    species = models.ForeignKey(
        Species,
        on_delete=models.CASCADE,
        related_name="breeds",
        help_text="Select the species this breed belongs to",
    )

    def __str__(self):
        return f"{self.name} ({self.species.name})"

    class Meta:
        verbose_name = "Breed"
        verbose_name_plural = "Breeds"
        ordering = ["name"]


class Pet(models.Model):
    SPECIES_CHOICES = [
        ("DOG", "Dog"),
        ("CAT", "Cat"),
        ("BIRD", "Bird"),
        ("FISH", "Fish"),
        ("REPTILES", "Reptiles"),
        ("SMALL MAMMAL", "Small Mammal"),
        ("OTHER", "Other"),
    ]
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    name = models.CharField(max_length=250, help_text="Enter the pet's name")
    species = models.CharField(
        max_length=250,
        choices=SPECIES_CHOICES,
        help_text="Select the species of the pet",
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="pets",
        help_text="Select the breed of the pet",
    )
    breed2 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Enter the second breed of the pet",
    )
    price = models.IntegerField(default=0, help_text="Enter the price of the pet")
    location = models.CharField(
        max_length=100, null=True, blank=True, help_text="Enter the location of the pet"
    )
    quantity = models.IntegerField(default=1, help_text="Enter the quantity of the pet")
    color = models.CharField(
        max_length=50, null=True, blank=True, help_text="Enter the color of the pet"
    )
    dob = models.CharField(
        max_length=100, help_text="Enter the date of birth of the pet"
    )
    age = models.PositiveIntegerField(
        null=True, blank=True, help_text="Enter the age of the pet in years"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Enter the weight of the pet",
    )
    gender = models.CharField(
        max_length=50, choices=GENDER_CHOICES, help_text="Enter the gender of the pet"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Enter a brief description of the pet"
    )
    slug = models.SlugField(max_length=250, null=True, blank=True)
    image = models.ImageField(
        upload_to="pets/", blank=True, null=True, help_text="Upload an image of the pet"
    )
    available_from = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the pet became available for adoption",
    )
    pets_no = models.CharField(
        max_length=4, unique=True, help_text="Enter the 4-digit pet number",default=""
    )
    map = models.TextField(null=True, blank=True, default="")

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when the pet record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the pet record was last updated",
    )

    def generate_unique_pets_no(self):
        while True:
            pets_no = f"{random.randint(1000, 9999):04d}"
            if not Pet.objects.filter(pets_no=pets_no).exists():
                return pets_no

    def save(self, *args, **kwargs):
        if not self.pets_no:
            self.pets_no = self.generate_unique_pets_no()
        super(Pet, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Pet"
        verbose_name_plural = "Pets"
        ordering = ["-created_at"]


@receiver(pre_save, sender=Pet)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        unique_slug = base_slug
        num = 1
        while Pet.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        instance.slug = unique_slug


class pets_additional_image(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="pets/", blank=True, null=True)


class CartItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_product(self):
        return self.product is not None

    def is_pet(self):
        return self.pet is not None

    def __str__(self):
        return f"{self.product}--------> {self.user}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart({self.user.username})"


class Order(models.Model):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    PAYMENT_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (SUCCESS, "Success"),
        (FAILURE, "Failure"),
    ]

    NOT_PACKED = "Not Packed"
    READY_FOR_SHIPMENT = "Ready For Shipment"
    SHIPPED = "Shipped"
    DELIVERED = "Delivered"

    ORDER_STATUS_CHOICES = [
        (NOT_PACKED, "Not Packed"),
        (READY_FOR_SHIPMENT, "Ready For Shipment"),
        (SHIPPED, "Shipped"),
        (DELIVERED, "Delivered"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=150, null=False, default="")
    lname = models.CharField(max_length=150, null=False, default="")
    email = models.CharField(max_length=150, null=False, default="")
    phone = models.CharField(max_length=150, null=False, default="")
    address = models.TextField(default="", null=False)
    city = models.CharField(max_length=150, null=False, default="")
    state = models.CharField(max_length=150, null=False, default="")
    pincode = models.CharField(max_length=150, null=False, default="")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=False, default=0
    )
    payment_mode = models.CharField(max_length=150, null=False, default="")
    order_id = models.CharField(max_length=255, unique=True, default="")
    payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    status = models.CharField(
        max_length=255, choices=ORDER_STATUS_CHOICES, default=NOT_PACKED
    )
    payment_status = models.CharField(
        max_length=255, choices=PAYMENT_STATUS_CHOICES, default=PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    datetime_of_payment = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    message = models.TextField(null=True)
    tracking_no = models.CharField(max_length=255, null=True)
    products = models.ManyToManyField("Product", through="OrderItem")

    def save(self, *args, **kwargs):
        # Generate a unique order_id if it is not already set
        if not self.order_id:
            self.order_id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    @transaction.atomic
    def update_product_availability(self):
        """Update product availability based on the order items."""
        for item in self.orderitem_set.all():
            product = item.product
            if product:
                product.available -= item.quantity
                product.save()

    def __str__(self):
        return "{}-{}-{}-------{}".format(
            self.id, self.tracking_no, self.user, self.datetime_of_payment
        )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)

    def __str__(self):
        return f"OrderItem - {self.product.title} x Quantity : {self.quantity} / Order --{self.id}//USER --{self.order.user}"


class Emails(models.Model):
    subject = models.CharField(max_length=255)
    message = models.TextField()
    email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False, default="")
    address = models.TextField(null=False)
    city = models.CharField(max_length=150, null=False)
    state = models.CharField(max_length=150, null=False)
    country = models.CharField(max_length=150, null=False)
    pincode = models.CharField(max_length=150, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    pet_type = models.CharField(
        max_length=100,
        choices=[
            ("Cat", "Cat"),
            ("Dog", "Dog"),
            ("Other", "Other"),
        ],
    )
    interest = models.CharField(
        max_length=100,
        choices=[
            ("Pet Training", "Pet Training"),
            ("Pet Grooming", "Pet Grooming"),
            ("Care Services", "Care Services"),
            ("Pet Boarding", "Pet Boarding"),
            ("Pet Bath", "Pet Bath"),
            ("Pet Adoption", "Pet Adoption"),
        ],
    )
    date = models.DateField()
    time = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class ConfirmAppointment(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    confirmed = models.BooleanField(default=False)  # Add a confirmed field

    def __str__(self):
        return f"Appointment on {self.date} at {self.time} for {self.appointment.user.username}"


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    confirmed_appointment = models.ForeignKey(
        ConfirmAppointment, on_delete=models.CASCADE
    )
    Appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        default=None,
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return self.title


def generate_unique_pets_no():
    """Generate a unique 4-digit pet number."""
    while True:
        unique_id = str(random.randint(1000, 9999))  # Generate a 4-digit number
        if not Petadopt.objects.filter(pets_no=unique_id).exists():  # Ensure uniqueness
            return unique_id

class Petadopt(models.Model):
    SPECIES_CHOICES = [
        ("DOG", "Dog"),
        ("CAT", "Cat"),
        ("BIRD", "Bird"),
        ("FISH", "Fish"),
        ("REPTILES", "Reptiles"),
        ("SMALL MAMMAL", "Small Mammal"),
        ("OTHER", "Other"),
    ]
    GENDER_CHOICES = [
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    ]

    name = models.CharField(max_length=250, help_text="Enter the pet's name")
    species = models.CharField(
        max_length=250,
        choices=SPECIES_CHOICES,
        help_text="Select the species of the pet",
    )
    breed = models.ForeignKey(
        Breed,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="petsadoption",
        help_text="Select the breed of the pet",
    )
    breed2 = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        help_text="Enter the second breed of the pet",
    )
    location = models.CharField(
        max_length=100, null=True, blank=True, help_text="Enter the location of the pet"
    )
    quantity = models.IntegerField(default=1, help_text="Enter the quantity of the pet")
    color = models.CharField(
        max_length=50, null=True, blank=True, help_text="Enter the color of the pet"
    )
    dob = models.CharField(
        max_length=100, help_text="Enter the date of birth of the pet"
    )
    age = models.PositiveIntegerField(
        null=True, blank=True, help_text="Enter the age of the pet in years"
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Enter the weight of the pet",
    )
    gender = models.CharField(
        max_length=50, choices=GENDER_CHOICES, help_text="Enter the gender of the pet"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Enter a brief description of the pet"
    )
    slug = models.SlugField(max_length=250, null=True, blank=True)
    image = models.ImageField(
        upload_to="pets/", blank=True, null=True, help_text="Upload an image of the pet"
    )
    is_adopted = models.BooleanField(
        default=False, help_text="Mark if the pet has been adopted"
    )
    available_from = models.DateField(
        blank=True,
        null=True,
        help_text="Date when the pet became available for adoption",
    )
    map = models.TextField(null=True, blank=True, default="")

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="The date and time when the pet record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the pet record was last updated",
    )

    def save(self, *args, **kwargs):
        if not self.pets_no:
            self.pets_no = generate_unique_pets_no()  # Generate unique 4-digit pets_no
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(pre_save, sender=Petadopt)
def generate_petadopt_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.name)
        unique_slug = base_slug
        num = 1
        while Petadopt.objects.filter(slug=unique_slug).exists():
            unique_slug = f"{base_slug}-{num}"
            num += 1
        instance.slug = unique_slug


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Petadopt"
        verbose_name_plural = "Petsadoption"
        ordering = ["-created_at"]


class petsadopt_additional_image(models.Model):
    pet = models.ForeignKey(Petadopt, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="petsadopt/", blank=True, null=True)

    def __str__(self):
        return f"Additional Image for {self.pet.name}"


class AdoptionRequest(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    appointment_date = models.DateField()
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    pet_id = models.CharField(max_length=50,default="")
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fullname} - {self.pet_id}"
