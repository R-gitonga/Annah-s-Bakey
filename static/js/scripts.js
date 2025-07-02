document.addEventListener('DOMContentLoaded', function() {
    //Generic function to set up a read more/less toggle
    //this fun takes a button and its associated content div

    function setupReadMoreToggle(button, contentDiv) {
        if (button && contentDiv) {
            button.addEventListener('click', function() {
                contentDiv.classList.toggle('expanded');
                if (contentDiv.classList.contains('expanded')) {
                    button.textContent = 'Read Less';
                } else {
                    button.textContent = 'Read More';
                }
            });
        }
    }
    //setup for About section
    const aboutToggleButton = document.querySelector('.read-more-toggle');
    const aboutContentDiv = document.querySelector('.profile-text-content');
    setupReadMoreToggle(aboutToggleButton, aboutContentDiv)

    //setup for all buttons with .card-read-more-toggle class
    const cardToggleButtons = document.querySelectorAll('.card-read-more-toggle');

    //loop through each card's toggle button
    cardToggleButtons.forEach(button => {
        //find content div associated with THIS specific button
        //The Content Div is the previous sibling of the button's parent(which is the .card-body)
        // or more robustly: ind the closest parent  .card-bofy, then query for its child .card-description-content
        const cardBody = button.closest('.card-body');
        if (cardBody) {
            const cardContentDiv = cardBody.querySelector('.card-description-content') //find the content div inside the card body
            setupReadMoreToggle(button, cardContentDiv); //apply the generic setup function to this pair
        }
    });

});