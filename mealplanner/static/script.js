// TODO: Create an animation AFTER validation for Username/Password
// I am thinking currently after focus changes
// "tab" slides to the right, bg -> success.subtle bg.gradient

document.addEventListener('DOMContentLoaded', function () {

    var grid = document.querySelector('.grid');
    var iso = new Isotope(grid, {
        itemSelector: '.grid-item',
        masonry: {
            columnWidth: 80
        }
    });

    grid.addEventListener('click', function (event) {
        var target = event.target;
        // only click on itemContent
        if (!target.classList.contains('grid-item-content')) {
            return;
        }
        var itemElem = target.parentNode;
        itemElem.classList.toggle('is-expanded');
        iso.layout();
        target.childNodes[3].classList


    });


    // JS for reactive content

    // var elem = document.querySelector('.grid');
    // var iso = new Isotope(elem, {
    //     // options
    //     itemSelector: '.grid-item',
    //     percentPosition: true,
    //     // layoutMode: 'fitRows',
    //     masonry: {
    //         columnWidth: '.grid-sizer'
    //     },
    //     stagger: 30,
    //     // Staggers transitions by 30 milliseconds
    //     transitionDuration: 400,
    //     // Transition lasts .4s in milliseconds
    // });

    // elem.addEventListener('click', function (event) {
    //     var itemContent = event.target;
    //     if (!itemContent.classList.contains('grid-item-content')) {
    //         return;
    //     }

    //     setItemContentPixelSize(itemContent);

    //     var itemElem = itemContent.parentNode;
    //     itemElem.classList.toggle('is-expanded');

    //     // Force redraw
    //     var redraw = itemContent.offsetWidth;
    //     // Renable default transition
    //     itemContent.style[transitionProp] = '';

    //     addTransitionListener(itemContent);
    //     setItemContentTransitionSize(itemContent, itemElem);

    //     iso.layout();
    // });

    // var docElemStyle = document.documentElement.style;
    // var transitionProp = typeof docElemStyle.transition == 'string' ?
    //     'transition' : 'WebkitTransition';
    // var transitionEndEvent = {
    //     WebkitTransition: 'webkitTransitionEnd',
    //     transition: 'transitionend'
    // }[transitionProp];

    // function setItemContentPixelSize(itemContent) {
    //     // Disable transition
    //     itemContent.style[transitionProp] = 'none';
    //     // Set current size in pixels
    //     setItemContentPixelSize(itemContent, itemContent);
    // }

    // function addTransitionListener(itemContent) {
    //     itemContent.style.width = '';
    //     itemContent.style.height = '';
    //     itemContent.removeEventListener(
    //         transitionEndEvent, onTransitionEnd);
    // };
    // itemContent.addEventListener(transitionEndEvent, onTransitionEnd);

    // function setItemContentTransitionSize(itemContent, itemElem) {
    //     // Set new size
    //     setItemContentSize(itemContent, itemElem);
    // }

    // function setItemContentSize(itemContent, elem) {
    //     var size = getSize(elem);
    //     itemContent.style.width = size.width + 'px';
    //     itemContent.style.height = size.height + 'px';
    // }

    // filter items on button click
    let filterButtonGroup = document.querySelector('.filter-button-group');
    filterButtonGroup.addEventListener('click', 'button', function () {
        var filterValue = filterButtonGroup.getAttribute('data-filter');
        grid.isotope({ filter: filterValue });
    });
})
// Isotope JS+
