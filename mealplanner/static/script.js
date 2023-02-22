// TODO: Create an animation AFTER validation for Username/Password
// I am thinking currently after focus changes
// "tab" slides to the right, bg -> success.subtle bg.gradient

document.addEventListener('DOMContentLoaded', function () {

    var grid = document.querySelector('.grid');
    var iso = new Isotope(grid, {
        itemSelector: '.grid-item',
        masonry: {
            columnWidth: 42
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

    //TODO: Fix filter button with Javascript

    // filter items on button click
    let filterButtonGroup = document.querySelector('.filter-button-group');
    filterButtonGroup.addEventListener('click', 'button', function () {
        var filterValue = filterButtonGroup.getAttribute('data-filter');
        grid.isotope({ filter: filterValue });
    });
});
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
            document.querySelector('.favStarBox').innerHTML = `<i class="bi-star-fill favStar" data-id="{{ recipe.id }}"></i>`
        }))

        .catch(error => {
            console.log(`${error}`);
        })
}