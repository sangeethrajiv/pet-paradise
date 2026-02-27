import os
import django
import random
import shutil
from pathlib import Path

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'petparadise.settings')
django.setup()

from django.conf import settings
from Paradiseapp.models import (
    MainCategory, Category, SubCategory, Product, 
    Addtional_information, Additional_image,
    Species, Breed, Pet, Petadopt, pets_additional_image, petsadopt_additional_image
)

def clear_data():
    print("Clearing all existing data...")
    pets_additional_image.objects.all().delete()
    petsadopt_additional_image.objects.all().delete()
    Addtional_information.objects.all().delete()
    Additional_image.objects.all().delete()
    Product.objects.all().delete()
    Pet.objects.all().delete()
    Petadopt.objects.all().delete()
    SubCategory.objects.all().delete()
    Category.objects.all().delete()
    MainCategory.objects.all().delete()
    Breed.objects.all().delete()
    Species.objects.all().delete()
    print("Database cleared.")

def get_unique_images():
    # Product images from static/assets/img/products/
    prod_images = [f"assets/img/products/products_img{i:02d}.jpg" for i in range(1, 16)]
    prod_images += [f"assets/img/products/latest_products_img{i:02d}.jpg" for i in range(1, 7)]
    prod_images += [f"assets/img/products/h_products_img{i:02d}.jpg" for i in range(1, 3)]
    
    # Pet images from static/assets/img/shop/
    pet_images = [f"assets/img/shop/shop_img{i:02d}.jpg" for i in range(1, 10)]
    pet_images += [f"assets/img/shop/pet_details{i:02d}.jpg" for i in range(1, 5)]
    
    random.shuffle(prod_images)
    random.shuffle(pet_images)
    
    return prod_images, pet_images

def copy_to_media(src_rel_path, subfolder):
    """Copies a static asset to the media folder for ImageField compatibility."""
    src_path = Path(settings.BASE_DIR) / "static" / src_rel_path
    if not src_path.exists():
        print(f"Warning: Source image {src_path} not found.")
        return None
    
    media_root = Path(settings.MEDIA_ROOT) / subfolder
    media_root.mkdir(parents=True, exist_ok=True)
    
    dest_filename = src_path.name
    dest_path = media_root / dest_filename
    
    shutil.copy(src_path, dest_path)
    return f"{subfolder}/{dest_filename}"

def seed_data():
    print("Starting unique seed process...")
    clear_data()
    prod_image_pool, pet_image_pool = get_unique_images()

    # 1. Create Main Categories
    print("Seeding Categories...")
    mc_supply = MainCategory.objects.create(title="Pet Supplies")
    mc_accessories = MainCategory.objects.create(title="Accessories")
    mc_food = MainCategory.objects.create(title="Pet Food")

    # 2. Create Categories
    cat_dog = Category.objects.create(title="Dog Essentials", maincategory=mc_supply)
    cat_cat = Category.objects.create(title="Cat Essentials", maincategory=mc_supply)
    cat_toys = Category.objects.create(title="Interactive Toys", maincategory=mc_accessories)
    cat_kibble = Category.objects.create(title="Premium Kibble", maincategory=mc_food)

    # 3. Create Sub-Categories
    sub_leash = SubCategory.objects.create(title="Leashes & Collars", category=cat_dog)
    sub_beds = SubCategory.objects.create(title="Beds & Comfort", category=cat_dog)
    sub_litter = SubCategory.objects.create(title="Litter Boxes", category=cat_cat)
    sub_chew = SubCategory.objects.create(title="Chew Toys", category=cat_toys)

    # 4. Create Products (at most 20 to ensure unique images from pool of 23)
    print("Seeding Products with unique images...")
    product_titles = [
        "Orthopedic Memory Bed", "Interactive Laser Pro", "Natural Grain-Free Beef",
        "Reflective Night Harness", "Silent Water Fountain", "Sisal Scratching Post",
        "Rubber Chew Bone", "Silicon Grooming Brush", "High-Protein Puppy Mix",
        "Retractable Long Leash", "Ceramic Feeding Bowl", "Plush Squirrel Squeak",
        "Odor-Control Cat Litter", "Travel Carrier - Medium", "Winter Fleece Jacket",
        "Dental Care Treat sticks", "Catnip Infused Mouse", "Training Clicker Kit",
        "Gentle Shampoo - Aloe", "Bird Seed Bell"
    ]

    for i, title in enumerate(product_titles[:len(prod_image_pool)]):
        img_path = prod_image_pool[i]
        product = Product.objects.create(
            title=title,
            category=random.choice([cat_dog, cat_cat, cat_toys, cat_kibble]),
            price=random.randint(500, 5000),
            discount=random.choice([0, 5, 10, 15, 20]),
            total=random.randint(20, 100),
            available=random.randint(10, 20),
            description=f"Premium quality {title} designed for your pet's happiness and health.",
            tags=f"pet, premium, {title.lower().replace(' ', ', ')}",
            featured_image=img_path, # CharField in this project
            quantity=1
        )
        Addtional_information.objects.create(product=product, title="Package Type", spec="Secure Box")

    # 5. Create Species and Breeds
    print("Seeding Species and Breeds...")
    sp_dog = Species.objects.create(name="Dog")
    sp_cat = Species.objects.create(name="Cat")
    
    breeds_dog = ["Golden Retriever", "German Shepherd", "Beagle", "Poodle", "Bulldog"]
    breeds_cat = ["Persian", "Maine Coon", "Siamese", "British Shorthair", "Sphynx"]

    for b_name in breeds_dog:
        Breed.objects.create(name=b_name, species=sp_dog)
    for b_name in breeds_cat:
        Breed.objects.create(name=b_name, species=sp_cat)

    # 6. Create Pets for Sale (Unique images from pool of 13)
    print("Seeding Pets for Sale with unique images...")
    sale_pet_names = ["Buddy", "Max", "Luna", "Charlie", "Bella", "Rocky"]
    dog_breeds = Breed.objects.filter(species=sp_dog)
    
    for i, name in enumerate(sale_pet_names):
        img_src = pet_image_pool.pop(0)
        media_path = copy_to_media(img_src, "pets")
        
        Pet.objects.create(
            name=name,
            species="DOG",
            breed=random.choice(dog_breeds),
            price=random.randint(8000, 30000),
            location="Kochi, Kerala",
            age=random.randint(1, 4),
            gender=random.choice(["MALE", "FEMALE"]),
            description=f"Meet {name}, a playful and friendly pup ready to join your family.",
            dob="2023-06-12",
            image=media_path,
            available_from="2024-01-01"
        )

    # 7. Create Pets for Adoption (Unique images remaining in pool)
    print("Seeding Pets for Adoption with unique images...")
    adopt_pet_names = ["Daisy", "Milo", "Oliver", "Coco", "Simba"]
    cat_breeds = Breed.objects.filter(species=sp_cat)

    for i, name in enumerate(adopt_pet_names):
        if not pet_image_pool: break
        img_src = pet_image_pool.pop(0)
        media_path = copy_to_media(img_src, "pets") # Both use pets folder if fine
        
        Petadopt.objects.create(
            name=name,
            species="CAT",
            breed=random.choice(cat_breeds),
            location="Kollam, Kerala",
            age=random.randint(1, 3),
            gender=random.choice(["MALE", "FEMALE"]),
            description=f"{name} is a sweet soul looking for a warm home and lots of cuddles.",
            dob="2022-11-20",
            image=media_path,
            available_from="2024-02-15"
        )

    print("\n" + "="*40)
    print("Seed data process completed successfully!")
    print(f"Products created: {Product.objects.count()}")
    print(f"Pets (Sale) created: {Pet.objects.count()}")
    print(f"Pets (Adopt) created: {Petadopt.objects.count()}")
    print("="*40)

if __name__ == "__main__":
    seed_data()
