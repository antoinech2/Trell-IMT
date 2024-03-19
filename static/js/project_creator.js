document.addEventListener('DOMContentLoaded', (event) => {
    // Function to update the hided input with categories
    const updateCategoryList = () => {
        //select the category name and remove the 'X'
        const categories = Array.from(document.querySelectorAll('.categoryCreate'))
            .map(elem => elem.textContent.replace(' X', '').trim());
        //link the catégories with ',' and update the hided input
        document.getElementById('category_list').value = categories.join('|');
    };

    //add a listener for the add category button
    document.querySelector('.category-add').addEventListener('click', function() {
        //get the name of the category to add
        const categoryName = document.querySelector('.form-name_category').value.trim();
        if (categoryName) {
            //create nex div for category
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'categoryCreate badge rounded-pill text-bg-primary';
            categoryDiv.innerHTML = `${categoryName} <span class="remove-category">X</span>`;
            //add this new div to the categories
            document.querySelector('#categories').appendChild(categoryDiv);
            // remove what's in category name input
            document.querySelector('.form-name_category').value = '';
            //add a suppression listener
            addRemoveListener(categoryDiv.querySelector('.remove-category'));
            //update the hided input
            updateCategoryList();
        }
    });

    // add listener on the remove button
    const addRemoveListener = (element) => {
        element.addEventListener('click', function() {
            // delete the category div
            this.parentNode.remove();
            //update the hided input
            updateCategoryList();
        });
    };

    document.querySelectorAll('.remove-category').forEach(addRemoveListener);

    //update the categories at launch
    updateCategoryList();
});

