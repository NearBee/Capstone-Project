// TODO: Create an animation AFTER validation for Username/Password
// I am thinking currently after focus changes
// "tab" slides to the right, bg -> success.subtle bg.gradient

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
            let username = editProfileButton.getAttribute('data-user');

            editProfile(username);
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

    // Allows for use of the recipes in the grid using isotope, also re-sorts them after each content load
    if (grid) {
        grid.addEventListener('click', function (event) {
            var target = event.target;

            iso.layout();
            let content = target.querySelector('.content-row');
            if (!content.style.display.includes('none')) {
                content.style.display = 'none';
            } else {
                content.style.display = 'block';
            }

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

    // Find the button with the class "#finalizePlannerButton", then attach a click event to it
    var finalizePlannerButton = document.querySelector('.finalizePlannerButton')
    if (finalizePlannerButton) {
        finalizePlannerButton.addEventListener('click', function () {
            let id = finalizePlannerButton.getAttribute('data-id');

            finalizePlanner(id);
        });
    }



    // Form Errors

    var form = document.getElementById('register-form');

    if (form) {
        if (Object.keys(errors).length > 0) {
            form.classList.add('has-error');
        }
        console.log(form);
    }

})
// Isotope JS+

function editProfile(username) {
    // Get all components that need to be switched out
    let profileHeader = document.querySelector('.profileHeader');
    let profilePicture = document.querySelector('.profilePictureCol');
    let profileUsername = document.querySelector('.usernameCol');
    let profileEmail = document.querySelector('.emailCol');
    let logoutButtons = document.querySelector('.logoutCol');
    let confirmButtons = document.querySelector('.confirmationCol');

    // Make new changes to HTML
    profileHeader.innerHTML = "Profile Edit";
    profilePicture.innerHTML = "<input type='file' class='form-control'>";
    profileUsername.innerHTML = "<input type='text' class='form-control' placeholder='New Username'>"
    profileEmail.innerHTML = "<input type='text' class='form-control' placeholder='New Email'>"

    // Hide logout button / Show confirmation buttons
    logoutButtons.style.display = 'none';
    confirmButtons.style.display = 'flex';

}

function submitEdit(username) {
    let csrf = document.querySelector("#csrf").dataset.csrf;

    fetch(`/edit_profile/${username}`, {
        method: "POST",
        body: JSON.stringify({
            username: username,
        }),
        headers: { "X-CSRFTOKEN": csrf },
        credentials: 'same-origin',
    })
        .then((response) => response.json())
        .then((result) => {
            console.log(result);
            // TODO: Access elements of profile modal for editing
            // Elements to touch: "Profile Information">"Profile Pic">"Username">"Email"

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
        .catch(error => {
            console.log(`${error}`);
        })

        .then((response => {
            let selectedBox = document.querySelector(`#gridItemModal${id} > div > div > div.modal-header > div.col-auto.me-2.mb-1.favStarBox > i`)
            console.log(selectedBox);

            if (selectedBox.classList.contains('bi-star-fill')) {
                selectedBox.classList.replace('bi-star-fill', 'bi-star');
            } else {
                selectedBox.classList.replace('bi-star', 'bi-star-fill');
            }
        }))

        .catch(error => {
            console.log(`${error}`);
        })
}

function finalizePlanner(id) {
    let csrf = document.querySelector("#csrf").dataset.csrf;

    fetch(`/finalize_planner/${id}`, {
        method: "POST",
        body: JSON.stringify({
            id: id
        }),
        headers: { "X-CSRFToken": csrf },
        credentials: 'same-origin',
    })

        .catch(error => {
            console.log(`${error}`);
        })

        .then((response => {
            // TODO: Might do something more here but for the time being it works
        }))
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
            console.log(result.shopping_list)
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

    // TODO: Do something with the result
}