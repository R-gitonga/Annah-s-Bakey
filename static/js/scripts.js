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


    const categoryDropdownButton = document.getElementById('categoryDropdown');
    const categoryFilterItems = document.querySelectorAll('.category-filter-item');
    const productCardsContainer = document.getElementById('product-cards-container');

    if (categoryFilterItems.length > 0 && productCardsContainer) {
        categoryFilterItems.forEach(item => {
            item.addEventListener('click', function(event) {
                event.preventDefault(); //prevent the default link behavior(page refresh)

                const selectedCategory = this.dataset.category; //get category from data-category attribute


                //update the dropdown button text
                categoryDropdownButton.textContent = selectedCategory;

                //remove 'active' class from all items and add to the clicked one

                categoryFilterItems.forEach(i => i.classList.remove('active'));
                this.classList.add('active');

                //make an AJAX request to new endpoint
                fetch(`/filter_products?category=${encodeURIComponent(selectedCategory)}`)
                .then(Response => {
                    if (!Response.ok) {
                        throw new Error(`HTTP error! status: ${Response.status}`);
                    }
                    return Response.text(); //get the HTML response
                })
                .then(html => {
                    //replace content of the product cards container
                    productCardsContainer.innerHTML = html;
                })
                .catch(error => {
                    console.error('Error fetching products:', error);
                });
            });
        });
    }
});