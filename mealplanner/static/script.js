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

    // Start Drag & Drop
    // TODO: Need to just switch this to a add to/ remove from function
    // Due to incompatibility with mobile uses
    var draggableElement = document.getElementsByClassName('recipePicture');
    if (draggableElement) {
        for (let boxes of draggableElement) {
            boxes.addEventListener('dragstart', startDrag);
        }
    }

    var dropZones = document.getElementsByClassName('dropBoxes');
    if (dropZones) {
        for (let zone of dropZones) {
            zone.addEventListener('drop', endDrag);

            // Prevents default behavior of a dragover() event
            zone.addEventListener('dragover', (event) => {
                event.preventDefault();
            })
        }
    }
    // End Drag & Drop

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

// Functions for Drag & Drop
function startDrag(event) {
    // Set data to be transferred
    var id = event.target;
    var dataId = id.getAttribute('data-id');

    // Attach data-id to the element being transferred
    event.datatransfer.setData("text/plain", dataId);
}

function endDrag(event) {
    event.preventDefault();

    // Obtain the data being transferred from the startDrag event
    let dataId = event.datatransfer.getData('text/plain');
    let droppedBox = event.target;

    // Set the recieved data to the dropbox
    droppedBox.setAttribute('data-id', dataId);

    // Check using console.log to see if the attribute was correctly moved
    console.log(droppedBox.getAttribute('data-id'));
}


// WIP addToPlanner function
// function addToPlanner(id) {
//     let csrf = document.querySelector("#csrf").dataset.csrf;

//     fetch(`recipes/add_to_planner/${id}`, {
//         method: "POST",
//         body: JSON.stringify()
//     })
// }

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

}