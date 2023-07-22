![Images](/images/overview.png)

# Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Resources](#Resources)
- [Development](#Development)
- [Built with](#Built-With)
- [Frontend development](#Frontend-Development)
- [Backend development](#Backend-Development)
- [Continued development](#Continued-Development)
- [Author](#Author) 

# Overview

EzyThrift is an eCommerce platform where users can purchase products at affordble prices 


## Features


## Features Overview

1. **User Authentication and Registration:** Secure user authentication and registration system with encrypted password storage. Users can also log in using their social media accounts like Google and Facebook.

2. **Product Catalog:** A diverse range of products organized into categories and subcategories, with a search functionality to quickly find items. Detailed product pages with images, descriptions, and specifications.

3. **Shopping Cart and Checkout:** Users can add multiple products to their cart, manage quantities, and proceed to checkout. The system calculates order totals, including fees and shipping. Support and integration with popular payment gateways (Paystack).

4. **Order Management:** User-friendly dashboard for customers to track order history and status. Email notifications for order confirmation, shipment, and delivery updates.

5. **User Reviews and Ratings:** Customers can leave reviews and ratings for products, helping other users make informed purchase decisions. Average ratings and reviews displayed on product pages.

6. **Admin Dashboard:** Powerful admin dashboard to manage products, categories, and orders. Product details, availability, and images can be edited from a central interface. Order processing and fulfillment made easy.

7. **Responsive Design:** Mobile-friendly and responsive layout for a seamless experience on all devices, including support for high-resolution screens.


8. **Security Measures:** Protection against common web vulnerabilities like CSRF and XSS. SSL certificate implementation for secure data transmission.

9. **Internationalization and Localization:** Support for multiple languages , allowing a broader reach and better localization options.


These features collectively create a robust and user-friendly eCommerce platform, enabling customers to enjoy a seamless shopping experience while providing site administrators with efficient tools to manage products and orders.


# Resources
- [Live Link](#Live-Link)(https://ezythrift.pythonanywhere.com)
- [Database Schema](#Database-Schema)
- [Presentation](#Presentation)


# Development

# Built With

 Our site was built using the following tools:

        * HTML
        * CSS
        * JAVASCRIPT
        * PYTHON(Django) ​ ​
        * SQLITE3

- How to Use


# To run locally

## Clone the project
``` git clone https://github.com/sidney2022/ezythrift.git ```

## Go to the project directory
``` cd ezythrift ```

## Create a Virtual Environment
``` python -m venv venv ```

## Activate Virtual Environment
``` venv\scripts\activate ```

## Install Dependencies
``` pip install -r requirements.txt ```

## Make migrations
``` python manage.py makemigrations ```

## Migrate the database
``` python manage.py migrate ```

## Create superuser ```
``` python manage.py createsuperuser ```
NB: uses email for authentication

## Finally, Start The Server.
``` python manage.py runserver ``` 


# Author
Sidney Uwaya [{@sidney2022}](https://github.com/sidney2022)


