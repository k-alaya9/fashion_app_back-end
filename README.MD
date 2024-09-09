# Fashion Experiment Project
=====================================

This is a Django project that allows users to experiment with different clothes and provide feedback on the results.

## Models
--------

The project consists of the following models:

### Category
* `name`: The name of the category (e.g. "T-Shirts", "Dresses", etc.)
* `image_url`: The URL of the category image

### Clothes
* `name`: The name of the clothes item (e.g. "Summer Tee", "Little Black Dress", etc.)
* `description`: A brief description of the clothes item
* `image_url`: The URL of the clothes item image
* `category`: The category that the clothes item belongs to

### Saved
* `user`: The user who saved the clothes item
* `clothes`: The clothes item that was saved
* `Created_at`: The date and time when the clothes item was saved

### Experiment
* `user_photo_path`: The URL of the user photo
* `clothes_photo_path`: The URL of the clothes photo
* `models_photo_path`: The URL of the model photo

### History
* `user`: The user who performed the experiment
* `experiment`: The experiment that was performed
* `Created_at`: The date and time when the experiment was performed

### Feedback
* `experiment`: The experiment that was performed
* `rate`: The rating given by the user (1-5)
* `description`: A brief description of the feedback

## Installation
--------------

To install the project, follow these steps:

1. Clone the repository: `git clone https://github.com/k-alaya9/fashion_app_back-end`
2. Install the required packages: `pip install -r requirements.txt`
3. Run the migrations: `python manage.py migrate`
4. Start the development server: `python manage.py runserver`

## Usage
-----

To use the project, follow these steps:

1. Create a new user account
2. Browse the categories and clothes items
3. Save clothes items to your favorites
4. Perform an experiment by uploading a user photo and clothes photo
5. Provide feedback on the experiment results

## Contributing
------------

Contributions are welcome! If you'd like to contribute to the project, please fork the repository and submit a pull request.

## License
-------

This project is licensed under the MIT License. See the LICENSE file for details.

## Authors
-------

* khaled alaya: [khaledalaya549@gmail.com]