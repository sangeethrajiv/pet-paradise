from django.contrib import admin
from .models import *
from django.utils.html import mark_safe


class PetsImageAdminTabular(admin.TabularInline):
    model = pets_additional_image  # Make sure the model name is correct
    extra = 4  # Optional: number of extra forms to display


class PetsadoptImageAdminTabular(admin.TabularInline):
    model = petsadopt_additional_image  # Make sure the model name is correct
    extra = 4  # Optional: number of extra forms to display


class SpeciesAdmin(admin.ModelAdmin):
    list_display = ("name",)


class BreedAdmin(admin.ModelAdmin):
    list_display = ("name", "species")
    list_filter = ("species",)


class PetAdmin(admin.ModelAdmin):
    inlines = [PetsImageAdminTabular]
    list_display = (
        "display_image",
        "name",
        "species",
        "breed",
        "age",
        "weight",
        "location",
    )
    list_filter = ("species", "breed")
    search_fields = (("name", "breed__name"),)

    def display_image(self, obj):
        if obj.image:  # Assuming 'image' is the field storing the image
            return mark_safe(
                f'<img src="{obj.image.url}" style="width: 50px; height: auto;" />'
            )
        return "No Image"

    display_image.short_description = "Image"


class PetAdoptAdmin(admin.ModelAdmin):
    inlines = [PetsadoptImageAdminTabular]
    list_display = (
        "display_image",
        "name",
        "species",
        "breed",
        "age",
        "weight",
        "is_adopted",
        "location",
        "id",
    )
    list_filter = ("species", "breed", "is_adopted","id")
    search_fields = ("name", "breed__name","id",)

    def display_image(self, obj):
        if obj.image:  # Assuming 'image' is the field storing the image
            return mark_safe(
                f'<img src="{obj.image.url}" style="width: 50px; height: auto;" />'
            )
        return "No Image"

    display_image.short_description = "Image"

    def display_image(self, obj):
        if obj.image:  # Assuming 'image' is the field storing the image
            return mark_safe(
                f'<img src="{obj.image.url}" style="width: 50px; height: auto;" />'
            )
        return "No Image"

    display_image.short_description = "Image"


class ConfirmAppointmentTabular(admin.TabularInline):
    model = ConfirmAppointment
    extra = 1


class MessageTabular(admin.TabularInline):
    model = Message
    extra = 1


class AppointmentAdmin(admin.ModelAdmin):
    inlines = [ConfirmAppointmentTabular, MessageTabular]


class SubCategoryTabular(admin.TabularInline):
    model = SubCategory


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryTabular]


class AdditionalInfoTabular(admin.TabularInline):
    model = Addtional_information


class AdditionalImageTabular(admin.TabularInline):
    model = Additional_image


class ProductAdmin(admin.ModelAdmin):
    inlines = [AdditionalInfoTabular, AdditionalImageTabular]
    list_display = ("title", "price", "featured_image", "category")
    list_filter = ("price", "category", "discount", "title")


@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = (
        "fullname",
        "email",
        "phone",
        "appointment_date",
        "species",
        "breed",
        "pet_id",  # Corrected field name
    )
    search_fields = (
        "fullname",
        "email",
        "phone",
        "species",
        "breed",
        "comment",
    )  # Corrected field name
    list_filter = ("species", "breed", "appointment_date")


# Register your models here
admin.site.register(MainCategory)
admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory)
admin.site.register(Product, ProductAdmin)
admin.site.register(userAddress)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Emails)
admin.site.register(Profile)
admin.site.register(Message)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(ConfirmAppointment)
admin.site.register(Species, SpeciesAdmin)
admin.site.register(Breed, BreedAdmin)
admin.site.register(Pet, PetAdmin)
admin.site.register(Petadopt,PetAdoptAdmin)
