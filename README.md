# Fake E-commerce

This project is a simple e-commerce website built with Django, designed to showcase products (specifically watches). It features a payment gateway integration and a Machine Learning-based chatbot for user interaction.

## Features

### 1. **Product Showcase**
   - Displays a list of products (watches in this case), including images and descriptions.
   - Products are shown with a sliding effect, one by one, on the homepage.

### 2. **Payment Gateway Integration**
   - **Stripe Payment Gateway**: The website integrates Stripe for handling secure online payments. Users can make payments via credit or debit cards.
   - To make the payment process more seamless, the following fields are captured:
     - Full name
     - Email
     - Address
     - Credit card information (name, number, expiration, CVV)
   
   **How to set up Stripe**:
   - Sign up for a Stripe account at [Stripe](https://stripe.com).
   - Obtain your **Publishable Key** and **Secret Key** from the Stripe Dashboard.
   - Replace the `STRIPE_PUBLISHABLE_KEY` and `STRIPE_SECRET_KEY` in your Django `settings.py` file with your keys.

### 3. **Machine Learning Chatbot**
   - The chatbot interacts with users, helping them with common queries and product recommendations.
   - Built using a custom ML model or API integration to provide automated responses.
   - The chatbot can handle basic requests such as:
     - Product inquiries
     - Order status
     - General queries
   - The backend uses the `/chatbot-response/` endpoint to send messages to the chatbot and retrieve responses.

   **How to implement the chatbot**:
   - This functionality relies on an AI/ML API, or a custom model can be trained for interaction.
   - A CSRF token is sent with each request to protect against cross-site request forgery.

### 4. **User Authentication**
   - Users can log in and register to manage their cart and make purchases.
   - Passwords are securely hashed using Django's built-in authentication system.
   - The login URL is `/login/`, and the default redirect URL is set to `store:product_list` after a successful login.

### 5. **Cart and Checkout**
   - Users can add products to their cart and proceed to checkout where they input their shipping and payment details.
   - Upon checkout, the user is able to confirm their order and make payments using the integrated Stripe gateway.

### 6. **Responsive Design**
   - The website is built to be fully responsive, using Bootstrap 4 for styling and layout.
   - All pages adapt to different screen sizes, ensuring a seamless experience across devices.

Technologies Used
Backend: Django (Python)
Frontend: HTML, CSS (Bootstrap 4), JavaScript
Payment Gateway: Stripe API
Machine Learning API: Custom integration for chatbot responses
Database: SQLite (default for development)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/fake-ecommerce.git
   cd fake-ecommerce
