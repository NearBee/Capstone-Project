// TODO: Create an animation AFTER validation for Username/Password
// I am thinking currently after focus changes
// "tab" slides to the right, bg -> success.subtle bg.gradient

document.addEventListener('DOMContentLoaded', function () {

    var grid = document.querySelector('.grid');
    var iso = new Isotope(grid, {
        itemSelector: '.grid-item',
        masonry: {
            columnWidth: 25,
            fitWidth: true
        }
    });

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

    var favoriteButton = document.getElementsByClassName('favStar');
    for (let button of favoriteButton) {
        button.addEventListener('click', function () {
            let id = button.getAttribute('data-id');

            favoriteRecipe(id);
        })
    }
    // filter items on button click
    let filterButtonGroup = document.querySelector('.filter-button-group');
    filterButtonGroup.addEventListener('click', function (event) {
        // only work with buttons
        if (!matchesSelector(event.target, 'button')) {
            return;
        }
        let filterValue = event.target.getAttribute('data-filter');
        iso.arrange({ filter: filterValue });
        console.log(filterValue);
    });

    // Find the button with the class "#finalizePlannerButton", then attach a click event to it
    var finalizePlannerButton = document.querySelector('.finalizePlannerButton')
    finalizePlannerButton.addEventListener('click', function () {
        let id = finalizePlannerButton.getAttribute('data-id');

        finalizePlanner(id);
    });



    // Form Errors

    var form = document.getElementById('register-form');

    if (Object.keys(errors).length > 0) {
        form.classList.add('has-error');
    }
    console.log(form);
})
// Isotope JS+


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
            console.log(id)
            // TODO: Make changes to the html for the planner making it uneditable potentially
        }))
}