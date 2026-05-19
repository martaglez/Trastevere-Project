# Trastevere Web App
![](frontend/trastevere-logo.jpeg)

A digital platform centered around the creation, sharing, and discovery of culinary recipes. The application connects users who wish to upload their own creations with a community eager to explore new culinary ideas.

## Tech Stack
| **Frontend** | **Backend** | **Database** | **Integrations/Tools** |
|--------------|-------------|--------------|------------------------|
| Flet | Python/Flet | PostgreSQL (SQLAlchemy & JSONB) | Redsys Virtual POS & Resend API |

## Features

- **Authentication System & Profiles**: Secure login functionality paired with a secure password recovery system utilizing tokens sent via the Resend email client
- **Public Access**: "About" section that allows public visitors to view software information without needing an active account or logging in.
- **Home Feed & Drafts System**: Centralized home feed to explore recipes , supported by a temporal drafts system that allows users to save intermediate recipe statuses in a dedicated "Table" to prevent data loss
- **Advanced Search**: Multi-faceted search capabilities backed by a user search history tracking mechanism persisted via JSONB fields.
- **Subscription Tiers**: A dual-tier monetization model distinguishing between Basic and Premium access levels.
  - **Basic Plan**: Users are limited to viewing 4 recipes per day and a single daily use of the "I'm feeling lucky" feature.
  - **Premium Plan**: Offers limitless daily recipe views, infinite usage of the "I'm feeling lucky" button, access to the "Recipe of the Week" logic, exclusive weekly coupons, and customizable visual application themes.
- **Secure Payment Gateway**: Secure financial transactions handled externally via a Redsys Virtual POS tunnel utilizing SHA-256 and 3DES encryption to process payments without storing raw credit card data.
- **Social & Interaction Tools**: A creator follow/unfollow interface , a 1-to-5 star recipe rating system , and an asynchronously loaded comments section.
- **Internationalization**: Multi-language interface translations allowing seamless toggling between English and Spanish.

## Getting Started
### Prerrequisites
- Python
- PostgreSQL

### Installation
```bash
git clone https://github.com/martaglez/Trastevere-Project.git
cd trastevere-Project
pip install -r requirements.txt
```

### Environment setup
Create a `.env` file in the root directory to manage your local PostgreSQL database configurations and third-party integration credentials:
```bash
DATABASE_URL=postgresql://user:password@localhost:5432/trastevere
REDSYS_SECRET_KEY=your_redsys_key_here
RESEND_API_KEY=your_resend_key_here
```

## Running the application
Before running the interface, ensure the connection between your Python models and the PostgreSQL tables is established and that the v3 schema migrations are properly executed.
```bash
python manage.py migrate
python main.py
```

## License
This project is licensed under Apache2.0 license. For more information, read `LICENSE.md`.

## Trastevere Team
* **Hugo Díaz** - [GitHub Profile](https://github.com/HugoDzP)
* **Javier Fernández** - [GitHub Profile](https://github.com/javixfdez)
* **María Ángeles Muñoz** - [GitHub Profile](https://github.com/chelesmjd)
* **Marta González** - [GitHub Profile](https://github.com/martaglez)
* **Marta Santomé** - [GitHub Profile](https://github.com/MartaSantome)
* **Marcos E. Fernández** - [GitHub Profile](https://github.com/MarcoseFdz)
