import os
import django
import random

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petparadise.settings')
django.setup()

from django.contrib.auth.models import User
from Paradiseapp.models import (
    MainCategory, Category, SubCategory, Product, 
    Addtional_information, Additional_image,
    Species, Breed, Pet, Petadopt, pets_additional_image, petsadopt_additional_image
)

def seed_data():
    print("Starting seed process...")

    # 1. Create Main Categories
    print("Seeding Categories...")
    mc_supply = MainCategory.objects.get_or_create(title="Pet Supplies")[0]
    mc_accessories = MainCategory.objects.get_or_create(title="Accessories")[0]
    mc_food = MainCategory.objects.get_or_create(title="Pet Food")[0]

    # 2. Create Categories
    cat_dog = Category.objects.get_or_create(title="Dog Essentials", maincategory=mc_supply)[0]
    cat_cat = Category.objects.get_or_create(title="Cat Essentials", maincategory=mc_supply)[0]
    cat_toys = Category.objects.get_or_create(title="Interactive Toys", maincategory=mc_accessories)[0]
    cat_kibble = Category.objects.get_or_create(title="Premium Kibble", maincategory=mc_food)[0]

    # 3. Create Sub-Categories
    sub_leash = SubCategory.objects.get_or_create(title="Leashes & Collars", category=cat_dog)[0]
    sub_beds = SubCategory.objects.get_or_create(title="Beds & Comfort", category=cat_dog)[0]
    sub_litter = SubCategory.objects.get_or_create(title="Litter Boxes", category=cat_cat)[0]
    sub_chew = SubCategory.objects.get_or_create(title="Chew Toys", category=cat_toys)[0]

    # 4. Create Products
    print("Seeding Products...")
    products_data = [
        {
            "title": "Orthopedic Dog Bed",
            "category": cat_dog,
            "price": 4500,
            "discount": 10,
            "total": 50,
            "available": 45,
            "description": "Premium memory foam bed providing ultimate comfort for your canine companion.",
            "tags": "dog, bed, comfort, orthopedic",
        },
        {
            "title": "Interactive Cat Laser Toy",
            "category": cat_cat,
            "price": 1200,
            "discount": 15,
            "total": 100,
            "available": 88,
            "description": "Keep your cat entertained for hours with this automatic rotating laser pointer.",
            "tags": "cat, toy, laser, interactive",
        },
        {
            "title": "Natural Grain-Free Dog Food (12kg)",
            "category": cat_kibble,
            "price": 3200,
            "discount": 5,
            "total": 30,
            "available": 25,
            "description": "High-protein, grain-free formula suitable for all adult dog breeds.",
            "tags": "dog, food, kibble, natural",
        },
        {
            "title": "Reflective Harness - Small",
            "category": cat_dog,
            "price": 850,
            "discount": 0,
            "total": 60,
            "available": 60,
            "description": "Durable and reflective harness for safe night walks.",
            "tags": "dog, harness, safety, Small",
        },
    ]

    for p_data in products_data:
        product, created = Product.objects.get_or_create(
            title=p_data["title"],
            defaults={
                "category": p_data["category"],
                "price": p_data["price"],
                "discount": p_data["discount"],
                "total": p_data["total"],
                "available": p_data["available"],
                "description": p_data["description"],
                "tags": p_data["tags"],
                "quantity": 1
            }
        )
        if created:
            # Add some additional info
            Addtional_information.objects.create(
                product=product,
                title="Material",
                spec="Breathable Mesh" if "Harness" in product.title else "Memory Foam" if "Bed" in product.title else "Recycled Plastic"
            )

    # 5. Create Species and Breeds
    print("Seeding Species and Breeds...")
    sp_dog = Species.objects.get_or_create(name="Dog")[0]
    sp_cat = Species.objects.get_or_create(name="Cat")[0]
    sp_bird = Species.objects.get_or_create(name="Bird")[0]

    breeds_dog = ["Golden Retriever", "German Shepherd", "Beagle", "Poodle", "Labrador"]
    breeds_cat = ["Persian", "Maine Coon", "Siamese", "British Shorthair"]

    for b_name in breeds_dog:
        Breed.objects.get_or_create(name=b_name, species=sp_dog)
    
    for b_name in breeds_cat:
        Breed.objects.get_or_create(name=b_name, species=sp_cat)

    # 6. Create Pets (for sale)
    print("Seeding Pets for Sale...")
    pet_breeds = Breed.objects.filter(species=sp_dog)
    pet_names = ["Buddy", "Max", "Luna", "Charlie", "Bella"]
    
    for i in range(3):
        breed = random.choice(pet_breeds)
        name = pet_names[i]
        Pet.objects.get_or_create(
            name=name,
            species="DOG",
            breed=breed,
            price=random.randint(5000, 25000),
            location="Kollam, Kerala",
            age=random.randint(1, 5),
            gender=random.choice(["MALE", "FEMALE"]),
            description=f"A friendly and healthy {breed.name} looking for a loving home.",
            dob="2023-01-01",
            available_from="2024-01-01"
        )

    # 7. Create Pets for Adoption
    print("Seeding Pets for Adoption...")
    adoption_names = ["Daisy", "Milo", "Oliver"]
    cat_breeds = Breed.objects.filter(species=sp_cat)

    for i in range(2):
        breed = random.choice(cat_breeds)
        name = adoption_names[i]
        Petadopt.objects.get_or_create(
            name=name,
            species="CAT",
            breed=breed,
            location="Kollam City",
            age=random.randint(1, 3),
            gender=random.choice(["MALE", "FEMALE"]),
            description=f"Sweet {name} is looking for a forever home. Extremely gentle.",
            dob="2022-05-10",
            available_from="2024-02-15"
        )

    print("Seed data process completed successfully!")

if __name__ == "__main__":
    seed_data()
