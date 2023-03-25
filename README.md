# Project 02: Commerce
Commerce is an eBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a "watchlist."

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites
You need to have the following software installed in your system:

* Python 3.6 or above
* Django 3.1 or above
* Markdown2

## Installing
Follow the below steps to get a development environment running.

1. Clone the repository

`https://github.com/me50/alexaung/tree/web50/projects/2020/x/commerce`

2. Install the dependencies

`pip install -r requirements.txt`

3. Apply the migrations

`python manage.py migrate`

4. Run the server

`python manage.py runserver`

## Running the tests
To run the tests, execute the following command:

`python manage.py test encyclopedia`

## Functionality
The website has the following functionalities:

* **Create Listing**: Users should be able to visit a page to create a new listing. They should be able to specify a title for the listing, a text-based description, and what the starting bid should be. Users should also optionally be able to provide a URL for an image for the listing and/or a category (e.g. Fashion, Toys, Electronics, Home, etc.).

* **Active Listings Page**: The default route of your web application should let users view all of the currently active auction listings. For each active listing, this page should display (at minimum) the title, description, current price, and photo (if one exists for the listing).

* **Listing Page**: Clicking on a listing should take users to a page specific to that listing. On that page, users should be able to view all details about the listing, including the current price for the listing.

  * If the user is signed in, the user should be able to add the item to their “Watchlist.” If the item is already on the watchlist, the user should be able to remove it.
  * If the user is signed in, the user should be able to bid on the item. The bid must be at least as large as the starting bid, and must be greater than any other bids that have been placed (if any). If the bid doesn’t meet those criteria, the user should be presented with an error.
  * If the user is signed in and is the one who created the listing, the user should have the ability to “close” the auction from this page, which makes the highest bidder the winner of the auction and makes the listing no longer active.
  * If a user is signed in on a closed listing page, and the user has won that auction, the page should say so.
  * Users who are signed in should be able to add comments to the listing page. The listing page should display all comments that have been made on the listing.


* **Watchlist**: Users who are signed in should be able to visit a Watchlist page, which should display all of the listings that a user has added to their watchlist. Clicking on any of those listings should take the user to that listing’s page.

* **Categories**: Users should be able to visit a page that displays a list of all listing categories. Clicking on the name of any category should take the user to a page that displays all of the active listings in that category.

* **Django Admin Interface**: Via the Django admin interface, a site administrator should be able to view, add, edit, and delete any listings, comments, and bids made on the site.

## Built With
* Django - The web framework used

## Authors
Aung Myo Oo - Initial work

## Acknowledgments
This project is a part of CS50’s Web Programming with Python and JavaScript course on edX. I would like to thank the CS50 team for providing such an amazing course and opportunity to learn and build real-world web applications using Python and Django. Special thanks to my instructor and peers for their guidance and support throughout this project.
