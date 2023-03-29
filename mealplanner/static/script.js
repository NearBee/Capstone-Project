document.addEventListener('DOMContentLoaded', function () {

    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]')
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl))
    var grid = document.querySelector('.grid');
    var iso = new Isotope(grid, {
        itemSelector: '.grid-item',
        masonry: {
            columnWidth: 25,
            fitWidth: true
        }
    });

    var editProfileButton = document.querySelector('.editWrapper');
    if (editProfileButton) {
        editProfileButton.addEventListener('click', function () {
            let id = editProfileButton.getAttribute('data-id');

            editProfile(id);
        })
    }

    var submitEditForm = document.getElementById('edit-form');
    if (submitEditForm) {
        submitEditForm.addEventListener('submit', function (e) {
            e.preventDefault();
            let id = submitEditForm.getAttribute('data-id');

            submitEdit(id);
        })
    }

    // Finding favorite buttons on a recipe and attaching the favoriteRecipe function to them
    var favoriteButton = document.getElementsByClassName('favStar');
    for (let button of favoriteButton) {
        button.addEventListener('click', function () {
            let id = button.getAttribute('data-id');

            favoriteRecipe(id);
        });
    }

    // Finding like buttons on a planner and attaching the "likePlanner" function to them
    var likeButtons = document.getElementsByClassName("likeRow")
    for (let button of likeButtons) {
        button.addEventListener('click', function () {
            let id = button.getAttribute('data-id');

            likePlanner(id);
        });
    }

    // Finding add to cart buttons on a planner and attaching the "addToCart" function to them
    var addToCartButtons = document.getElementsByClassName('listRow')
    for (let button of addToCartButtons) {
        button.addEventListener('click', function () {
            let id = button.getAttribute('data-id');

            addToCart(id);
        })
    }

    // nifty little animation for button click
    var clickableButtons = document.getElementsByClassName('plannerButton');
    for (var button of clickableButtons) {
        console.log("setting button");
        button.addEventListener('click', function () {
            this.classList.add("pulse");
            var target = this;
            setTimeout(function () {
                target.classList.remove("pulse");
            }, 800);
        });
    }

    // filter items on button click
    let filterButtonGroup = document.querySelector('.filter-button-group');
    if (filterButtonGroup) {
        filterButtonGroup.addEventListener('click', function (event) {
            // only work with buttons
            if (!matchesSelector(event.target, 'button')) {
                return;
            }
            let filterValue = event.target.getAttribute('data-filter');
            iso.arrange({ filter: filterValue });
        });
    }

    // Add an event listener to "add" a recipe to the planner
    var addButton = document.getElementsByClassName('addButton');
    if (addButton) {
        for (let button of addButton) {
            button.addEventListener('click', addToPlanner);
        }
    }

    // Add an event listener to "remove" a recipe from the planner
    var removeButton = document.getElementsByClassName('removeButton');
    if (removeButton) {
        for (let button of removeButton) {
            button.addEventListener('click', removeFromPlanner);
        }
    }

    // Find the button with the class "#finalizePlannerButton", then attach a click event to it
    var finalizePlannerButton = document.querySelector('.finalizePlannerButton')
    if (finalizePlannerButton) {
        finalizePlannerButton.addEventListener('click', finalizePlanner);
    }



    // Form Errors

    var form = document.getElementById('register-form');

    if (form) {
        if (Object.keys(errors).length > 0) {
            form.classList.add('has-error');
        }
        console.log(form);
    }

});
// Isotope JS+

function editProfile(id) {
    // Get all components that need to be switched out
    let profileHeader = document.querySelector('.profileHeader');
    let activeCol = document.querySelector(".activeView");
    let editCol = document.querySelector('.editCol');
    let logoutButtons = document.querySelector('.logoutCol');
    let confirmButtons = document.querySelector('.confirmationCol');

    if (!profileHeader.classList.contains("inProgress")) {

        // Change profile header to reflect that the user is currently editing
        profileHeader.innerHTML = "Profile Editing";
        profileHeader.classList.add("inProgress");

        // Remove "hidden" from editCol form
        activeCol.classList.add("hidden");
        editCol.classList.remove("hidden");


        // Hide logout button / Show confirmation buttons
        logoutButtons.style.display = 'none';
        confirmButtons.style.display = 'flex';
    } else {

        // Change profile header to reflect being back to normal profile view
        profileHeader.innerHTML = "Profile information";
        profileHeader.classList.remove("inProgress");

        // Add "hidden" from editCol form
        activeCol.classList.remove("hidden");
        editCol.classList.add("hidden");


        // Show logout button / Hide confirmation buttons
        logoutButtons.style.display = 'flex';
        confirmButtons.style.display = 'none';
    }

}

function submitEdit(id) {

    let csrf = document.querySelector("#csrf").dataset.csrf;

    let form = document.getElementById('edit-form');
    let formData = new FormData(form);

    fetch(`/edit_profile/${id}`, {
        method: "POST", // use POST method
        body: formData,
        headers: { "X-CSRFTOKEN": csrf },
        credentials: 'same-origin',
    })
        .then((response) => response.json())
        .then((result) => {

            editProfile(id);

            // Get the elements that need to be updated
            let profilePicture = document.getElementsByClassName('profilePicture');
            let profileUsername = document.getElementsByClassName('profileUsername');
            let profileEmail = document.getElementsByClassName('profileEmail');

            // Due to getElementsByClassName returning an HTMLcollection
            // A for loop is required to assign the updates where they are needed
            for (let profilePictures of profilePicture) {
                profilePictures.src = result.profile_picture;
            }
            for (let usernames of profileUsername) {
                usernames.innerHTML = result.username;
            }
            for (let emails of profileEmail) {
                emails.innerHTML = result.email;
            }



        })

        .catch(error => {
            console.log(`${error}`);
        })
}


function favoriteRecipe(id) {
    let csrf = document.querySelector("#csrf").dataset.csrf;

    fetch(`/favorite/${id}`, {
        method: 'POST',
        body: JSON.stringify({
            id: id
        }),
        headers: { "X-CSRFToken": csrf },
        credentials: 'same-origin',
    })

        .then((response => {
            let selectedBox = document.querySelector(`#gridItemModal${id} > div > div > div.modal-header > div.col-auto.me-2.mb-1.favStarBox > i`)

            if (selectedBox.classList.contains('bi-star-fill')) {
                selectedBox.classList.replace('bi-star-fill', 'bi-star');
            } else {
                selectedBox.classList.replace('bi-star', 'bi-star-fill');
            }

            // Target the star in the recipe grid and toggle hidden class
            var favoritedRecipeStar = document.getElementById(`favoritedRecipeStar${id}`);
            if (favoritedRecipeStar) {
                if (favoritedRecipeStar.classList.contains('hidden')) {
                    favoritedRecipeStar.classList.remove('hidden');
                } else {
                    favoritedRecipeStar.classList.add('hidden');
                }

            }
        }))

        .catch(error => {
            console.log(`${error}`);
        })
}

// Functions for Drag & Drop
function addToPlanner(event) {
    // Prevents default form submission event
    event.preventDefault()

    // Set data to be transferred
    var id = event.target;
    var dataId = id.getAttribute('data-id');

    let csrf = document.querySelector("#csrf").dataset.csrf;

    fetch(`recipes/add_to_planner/${dataId}`, {
        method: "POST",
        body: JSON.stringify({ id: dataId }),
        headers: { "X-CSRFTOKEN": csrf },
        credentials: 'same-origin',
    })
        .then(response => response.json())
        .then(data => {
            // Construct HTML for recipe box
            plannerBoxRecipe = `
                    <img class="object-fit-cover plannerRecipePhoto" src="${data.photo}" alt="${data.name}"
                    data-id="${data.id}">
                    <span class="position-absolute top-0 start-100 translate-middle badge border border-light rounded-circle bg-danger removeButton"
                    data-id="${data.id}"><i class="fa-solid fa-xmark" data-id="${data.id}"></i></span>
                    <div class="row justify-content-center">
                    <div class="col-auto gridItemText">
                        <span class="plannerRecipeText px-1">${data.name}</span>
                    </div>
                    </div>
                    `;

            // Attach data-id to the element being transferred
            let boxes = document.querySelectorAll('.plannerBoxes');
            var removeButton = document.getElementsByClassName('removeButton');
            for (let i = 0; i < boxes.length; i++) {
                if (boxes[i].innerHTML.trim() === "") {
                    console.log(i);
                    // Attach html of a recipe to innerhtml
                    boxes[i].innerHTML += plannerBoxRecipe;
                    if (removeButton) {
                        for (let button of removeButton) {
                            button.addEventListener('click', removeFromPlanner);
                        }
                    }
                    break;
                }

                //Check to see if the boxes are full
                if (i === boxes.length - 2) {
                    console.log("Boxes full!");

                    // Code to be executed if the condition is met
                    let finalizeButton = document.querySelector('.finalizePlannerButton');
                    finalizeButton.classList.remove('disabled');
                }
            }
        })
        .then(error => console.error(error));
}


function removeFromPlanner(event) {
    // Functionality to remove from planner will be added here
    // Prevents default form submission event
    event.preventDefault()

    // Set data to be transferred
    var id = event.target;
    var dataId = id.getAttribute('data-id');

    let csrf = document.querySelector("#csrf").dataset.csrf;

    fetch(`recipes/remove_from_planner/${dataId}`, {
        method: "POST",
        body: JSON.stringify({ id: dataId }),
        headers: { "X-CSRFTOKEN": csrf },
        credentials: 'same-origin',
    })
        .then(response => response.json())
        .then(data => {
            // Construct HTML for recipe box
            let box = document.querySelector(`[data-id="${data.id}"]`).closest(`.plannerBoxes`);
            box.innerHTML = '';

            // Disable the finalize planner button if not already disabled
            let finalizeButton = document.querySelector('.finalizePlannerButton');
            if (!finalizeButton.classList.contains('disabled')) {
                finalizeButton.classList.add('disabled');
            }
        })
        .catch(error => {
            console.log(`${error}`);
        });
}



function finalizePlanner(event) {
    let csrf = document.querySelector("#csrf").dataset.csrf;


    // Set data to be transferred
    var id = event.target;
    var dataId = id.getAttribute('data-id');

    // Add recipe to planner
    fetch(`/finalize_planner/${dataId}`, {
        method: "POST",
        body: JSON.stringify({ id: dataId }),
        headers: { "X-CSRFTOKEN": csrf },
        credentials: 'same-origin',
    })
        .then(response => response.json())
        .then(data => {
            console.log(data);
        })
        .catch(error => {
            console.log(`${error}`);
        });
}

function likePlanner(id) {
    let csrf = document.querySelector("#csrf").dataset.csrf;

    fetch(`/like_planner/${id}`, {
        method: "POST",
        body: JSON.stringify({
            id: id,
        }),
        headers: { "X-CSRFTOKEN": csrf },
        credentials: 'same-origin',
    })

        .catch(error => {
            console.log(`${error}`);
        })

        .then(() => {
            fetch(`/get_likes/${id}`)
                .then(response => response.json())
                .then(data => {
                    const likes = data.likes;
                    document.querySelector(`.likeButton${id}`).innerHTML = `${likes}`;
                })
                .catch(error => {
                    console.log(`${error}`);
                })
        })

        .catch(error => {
            console.log(`${error}`);
        });
}

function addToCart(id) {
    let csrf = document.querySelector("#csrf").dataset.csrf;

    fetch(`/add_to_cart/${id}`, {
        method: "POST",
        body: JSON.stringify({
            id: id,
        }),
        headers: { "X-CSRFTOKEN": csrf },
        credentials: 'same-origin',
    })
        .then((response) => response.json())
        .then((result) => {
            let newFormat = "";


            // Get shopping modal
            var modal = document.getElementById("shoppingModal")

            // Set the modal content to the JSON result
            var modalBody = modal.querySelector('.modal-body');

            for (let [name, [quantity, unit]] of Object.entries(result.shopping_list)) {
                newFormat += `
                <div class="row justify-content-between lh-1">
                    <div class="col-8">
                        <div>${name} : </div>
                    </div>
                    <div class="col-4">
                        <div>${quantity} ${unit}</div>
                    </div>
                </div>
                <hr>`
            }

            modalBody.innerHTML = newFormat;

        })
        .catch(error => {
            console.log(`${error}`);
        });

}