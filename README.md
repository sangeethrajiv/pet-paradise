<div align="center">

# 🐾 Pet Paradise

**Your One-Stop Platform for Pet Shopping, Adoption & Care Services**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0.7-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![MySQL](https://img.shields.io/badge/Database-MySQL%20%7C%20TiDB-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://tidbcloud.com)
[![Cloudinary](https://img.shields.io/badge/Media-Cloudinary-3448C5?style=for-the-badge&logo=cloudinary&logoColor=white)](https://cloudinary.com)
[![Razorpay](https://img.shields.io/badge/Payments-Razorpay-02042B?style=for-the-badge&logo=razorpay&logoColor=white)](https://razorpay.com)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![Render](https://img.shields.io/badge/Hosted%20on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

</div>

---

**Pet Paradise** is a full-featured, production-grade e-commerce and services web platform built with **Django 5**. It offers a seamlessly integrated experience for discovering and purchasing pet products, adopting pets, and booking professional care services — all in one place.

<div align="center">

### 📸 App Preview

| Home Page | Product Shop | Pet Adoption |
| :---: | :---: | :---: |
| ![Home](screenshots/home.png) | ![Shop](screenshots/shop.png) | ![Adoption](screenshots/adoption.png) |

</div>

---

## ✨ Features

### 🛒 E-Commerce & Product Shop
- **Product Catalog** — Browse products across multiple categories (Main Category → Sub Category → Product)
- **Discount System** — Real-time percentage-based discount calculation with automatic `discount_price` saved on every product
- **Product Detail Pages** — Rich descriptions via CKEditor, additional info specs table, and product images
- **Search** — Full-text search by product title and tags using Django `Q` objects
- **Stock Management** — `available` and `total` stock fields auto-updated on every successful order

### 🛍️ Cart & Checkout
- **Session-based Cart** — Add to cart, update quantity, and remove items via AJAX
- **Cart Count Badge** — Live cart item count displayed in navigation
- **Checkout Flow** — Saved shipping addresses auto-populate the checkout form for faster ordering
- **Shipping Address Book** — Users can save multiple delivery addresses and reuse them at checkout
- **Buy Now** — Skip the cart with a single-product instant checkout flow

### 💳 Payments
- **Razorpay Integration** — Secure online card/UPI payments via Razorpay JavaScript SDK
- **Cash on Delivery (COD)** — Orders placed as COD are marked "Ready for Shipment" immediately
- **Payment Verification** — Razorpay signature verification via `client.utility.verify_payment_signature` before any order is confirmed
- **Order Tracking** — Each order gets a unique `petparadise{7-digit}` tracking number

### 🐶 Pet Shop
- **Pet Listings** — Browse available pets with breed, species, gender, age, weight, color, and location details
- **Pet Detail View** — Dedicated pet page with additional image gallery and Google Maps embed
- **Buy a Pet** — Full checkout flow with Razorpay payment for purchasing pets

### 🐾 Pet Adoption
- **Adoption Listings** — Browse pets specifically listed for adoption with full profiles
- **Adoption Request Form** — Submit name, email, phone, preferred appointment date, species, and breed
- **Adoption Status** — `is_adopted` flag tracks whether a pet has been adopted
- **Slug-based URLs** — SEO-friendly URLs for each adoptable pet (e.g. `/adoptionview/golden-retriever/`)

### 📅 Appointment & Services Booking
Users can book appointments for:
- 🦮 Pet Training
- ✂️ Pet Grooming
- 🏥 Care Services
- 🏨 Pet Boarding
- 🛁 Pet Bath
- 🐾 Pet Adoption Consultation

- **Appointment Confirmation** — Admin confirms appointments with a specific date/time
- **In-App Messaging** — Confirmed appointments trigger user-readable messages visible in the Messages dashboard
- **Unread Count Badge** — Real-time unread message count polled via `/api/unread_count/`

### 👤 User Accounts
- **Registration & Login** — Email + password sign-up with duplicate email/phone validation
- **Real-time Validation** — AJAX checks for duplicate username or email before form submission
- **Password Change** — Authenticated users can change password with session preservation
- **User Profile** — Phone, address, city, state, country, pincode
- **Order History** — View all past orders with their current status and tracking number

### 📄 Other Pages
- `/about/` — About the platform
- `/contact/` — Contact form with email notification
- `/ourteam/` — Team members showcase
- `/gallery/` — Photo gallery
- `/faq/` — Frequently asked questions
- `/blog/` & `/ourblog/` — Blog listing and details
- `/petbreed/` — Breed reference guide

### 🔌 REST API
Basic REST API powered by Django REST Framework (DRF):

| Endpoint | Description |
|---|---|
| `GET /api/products/` | List all products |
| `GET /api/pets/` | List all pets |
| `GET /api/categories/` | List all categories |
| `GET /api/unread_count/` | Get user's unread message count |
| `GET /api/cart_data/` | Get current user's cart data (JSON) |

---

## 🏗️ Architecture & Data Models

```
MainCategory
    └── Category
            └── SubCategory
            └── Product
                    ├── Addtional_information
                    └── Additional_image

Species
    └── Breed
            ├── Pet                    (Pet Shop)
            │       └── pets_additional_image
            └── Petadopt               (Adoption)
                    └── petsadopt_additional_image
                    └── AdoptionRequest

User
    ├── Profile
    ├── userAddress
    ├── ShippingAddress
    ├── CartItem (Product | Pet)
    ├── Order
    │       └── OrderItem
    ├── Appointment
    │       └── ConfirmAppointment
    │               └── Message
    └── Emails
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Language** | Python 3.12 |
| **Framework** | Django 5.0.7 |
| **ORM / DB (Dev)** | SQLite |
| **ORM / DB (Prod)** | MySQL via TiDB Cloud (SSL) |
| **REST API** | Django REST Framework 3.14 |
| **Rich Text Editor** | Django CKEditor 6.7 |
| **Media Storage** | Cloudinary + django-cloudinary-storage |
| **Static Files** | WhiteNoise (compressed + cached) |
| **Payment Gateway** | Razorpay SDK |
| **Email** | Gmail SMTP via Django email backend |
| **Authentication** | Django built-in auth + session |
| **Containerization** | Docker (Python 3.12-slim) |
| **Process Manager** | Gunicorn |
| **Deployment** | Render (via `render.yaml` Blueprint) |
| **Image Processing** | Pillow |
| **Env Management** | python-dotenv |

---

## ⚙️ Local Setup

### Prerequisites
- Python 3.10+
- pip
- Git

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/pet-paradise.git
cd pet-paradise

# 2. Create and activate a virtual environment
python3 -m venv venv_linux
source venv_linux/bin/activate       # Windows: venv_linux\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env and fill in your keys (see below)

# 5. Run migrations
python manage.py migrate

# 6. Create a superuser (admin dashboard access)
python manage.py createsuperuser

# 7. Start the development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** — the app will be running.
Visit **http://127.0.0.1:8000/admin** — Django admin panel.

---

## 🔑 Environment Variables

Create a `.env` file from the example:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost

# Database — leave blank to use local SQLite
DATABASE_URL=mysql://user:password@host:port/dbname?ssl-mode=REQUIRED
MYSQL_ATTR_SSL_CA=/etc/ssl/certs/ca-certificates.crt

# Cloudinary (for production media)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Razorpay (payments)
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_SECRET_KEY=your-razorpay-secret-key

# Email (Gmail SMTP)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

> If `DATABASE_URL` is not set, the app defaults to SQLite — perfect for local development.
> If Cloudinary credentials are not set, the app falls back to local `media/` file storage.

---

## 🐳 Docker

```bash
# Build the image
docker build -t petparadise .

# Run with your .env file
docker run -p 8000:8000 --env-file .env petparadise
```

The `Dockerfile` uses a multi-step approach:
1. Installs system dependencies (`gcc`, `libpq-dev`, `default-libmysqlclient-dev`)
2. Installs Python packages
3. Collects static files via `collectstatic`
4. Starts the app via `entrypoint.sh` (runs Gunicorn)

---

## 🚀 Deployment on Render

This project ships with a `render.yaml` Blueprint. To deploy:

1. Push your code to GitHub.
2. Go to [render.com](https://render.com) → **New** → **Blueprint**.
3. Connect your GitHub repository.
4. Render auto-detects `render.yaml` and provisions the service.
5. Add your environment variables in the Render Dashboard.

> **Tip:** To avoid Render's free-tier cold starts, set up a free monitor at [uptimerobot.com](https://uptimerobot.com) to ping your app every 5 minutes.

---

## 🗂️ Project Structure

```
pet-paradise/
├── Paradiseapp/            # Main Django application
│   ├── models.py           # All data models
│   ├── views.py            # All view logic (~1500 lines)
│   ├── forms.py            # Django form classes
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin panel configuration
│   ├── api_views.py        # DRF ViewSets
│   ├── serializers.py      # DRF Serializers
│   └── migrations/         # Database migrations
├── petparadise/            # Django project config
│   ├── settings.py         # App settings
│   ├── urls.py             # Root URL conf
│   └── wsgi.py             # WSGI entry point
├── templates/              # HTML templates
│   ├── home/               # Home, about, contact, etc.
│   ├── shop/               # Product, pet, order pages
│   ├── cart/               # Cart, checkout pages
│   └── user/               # Login, signup pages
├── static/                 # CSS, JS, images
├── Dockerfile
├── render.yaml
├── entrypoint.sh
├── build.sh
└── requirements.txt
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## 📝 License

Distributed under the **MIT License**.

---

<div align="center">
Built with ❤️ for pet lovers everywhere 🐾
</div>
