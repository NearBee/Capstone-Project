# CS50w Capstone - Meal Mapper

## Description
---
[Video Demo](https://youtu.be/tIVYQL7bJLo) 

This my final project for CS50w. Using 
[Python](https://en.wikipedia.org/wiki/Python_(programming_language)) ([Django](https://en.wikipedia.org/wiki/Django_(web_framework)) web framework), [Javascript](https://en.wikipedia.org/wiki/JavaScript), [HTML](https://en.wikipedia.org/wiki/HTML) and [CSS](https://en.wikipedia.org/wiki/CSS). Meal Mapper is a web application that allows users to create and share planners using recipes provided on the recipes page (all recipes are provided by [All Recipes](https://www.allrecipes.com/)). Users can also search for recipes by meal preference and favorite them for an easier distinction for further recipes. Users can also create a shopping list of ingredients they need to buy for the recipes they have saved.

## Distinctiveness and Complexity
---
### Distinctiveness:
 This project is distinct from the previous projects in the course due to the use of Javascript to make requests to the API in conjunction with Django to create a seamless experience for the user to create and use a planner for the daily/weekly food needs. Also the use of a third party API to optimize the size of the images uploaded to the database to reduce the amount of time it take for a specific page to load (API in question is provided by [TinyPNG](https://tinypng.com/)).

### Complexity:
The projects complexity comes from the use of Javascript to make requests to the API to do a number of functions without having to reload the entirity of the page, some of the functions are:
- Search for recipes by meal preference
- Add recipes to the planner
- Remove recipes from the planner
- Add recipes to the favorites
- etc.

While also being able to update the profile for the user with an optimized image and new username/email, also being able to copy another user's planner without making changes to the original user's planner or being able to make changes to your own personal planners and not being forced to create new planners for them.


## Files
---

### `index.html`
This page was created in the idea that the user could be met with the page and be able to have a brief description for each of the recipes that would be provided on the recipe page. This would be the hook of the application to get the user's attention.
![Index.html](/mealplanner/imgs_for_readme/Welcome_Page.png)

### `recipes.html`
This page was created to provide the user with a list of recipes that they can choose from to add to their planner. The recipes are provided by [All Recipes](https://www.allrecipes.com/). The recipes are displayed in a grid format with the image of the recipe, the name of the recipe, the ingredients required to make the meal, and finally the nutritional facts about the recipe. The user can also search for recipes by meal preference and add them to their planner or even their favorites.
![Recipes.html](/mealplanner/imgs_for_readme/Recipes_Page.jpg)

### `planner_page.html`
This page was created to provide the user with a list of recipes that they have added to their planner. The planners are on a grid showing the user's active planner as well as all other planners created in order of the most recently created to the oldest planner. The user can also choose to edit their planners from this page as well as copy other user's planners to customize and make one of their own.
![planner_page.html](/mealplanner/imgs_for_readme/Planners_Page.png)

### `login.html/register.html`
These html files were created for use with Django's built in authentication system. They are also used in the modal's that are provided in the `layout.html` so they can be accessed from any part of the website.

![login.html](/mealplanner/imgs_for_readme/Login.png)
![register.html](/mealplanner/imgs_for_readme/Registration.png)

### `layout.html`
This file was created to provide the user with a consistent layout throughout the website. This file is used as a base template for all other html files. This file also contains the modal's for the login and register pages as well as housing links for other parts of the website.

### `Profile Information`
The profile information for each user is easily accessible by clicking on the user's name in the navbar. This will show the user the profile modal with information regarding their username, email as well as information regarding how many favorited recipes they have and how many planners they've created. Users can also update their profile information as well by simply clicking the update icon at the top of the profile modal.
![Profile Information](/mealplanner/imgs_for_readme/User_Profile_Information.png)

### `Shopping List`
The shopping list is a feature that allows the user to create a list of ingredients that they need to buy for the recipes they have saved. This list is created by clicking on the shopping list icon on the selected planner on the planners page. This will show the user the shopping list modal with a list of ingredients that they need to buy.
![Shopping List](/mealplanner/imgs_for_readme/Shopping_List.png)


## How to run the application
---

1. Clone the repository

```bash
git clone https://github.com/NearBee/Capstone-Project.git
```

2. Create a virtual environment and activate it

```bash
python3 -m venv venv && source venv/bin/activate
```

3. Install the requirements

```bash
pip install -r requirements.txt
```

4. Make migrations

```bash
python manage.py makemigrations mealplanner && python manage.py migrate
```

5. Run the application

```bash
python manage.py runserver
```

6. Open the application in your browser


## Additional Information
---
I created this application to help me with my meal planning. I've always had an issue of figuring out what to eat especially when it came to scheduling food to it and that would result in having a very unhealthy lifestyle. With this application I am able to get the information I need with ease and it helps with having a much more stable/healthy lifestyle.
Thank you for taking the time to read this README and I hope you enjoy the application as much as I did creating it. :wave: