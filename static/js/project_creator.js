$(document).ready(function() {
    // Function to update the hidden input with categories
    const updateCategoryList = () => {
        // Select the category name and remove the 'X'
        const categories = $('.categoryCreate').map(function() {
            return $(this).text().replace(' X', '').trim();
        }).get();
        // Join the categories with '|' and update the hidden input
        $('#category_list').val(categories.join('|'));
    };

    // Add a listener for the add category button
    $('.category-add').click(function() {
        // Get the name of the category to add
        const categoryName = $('.form-name_category').val().trim();
        if (categoryName) {
            // Create new div for the category
            const categoryDiv = $('<div></div>', {
                class: 'categoryCreate badge rounded-pill text-bg-primary',
                html: `${categoryName} <span class="remove-category">X</span>`
            });
            // Add this new div to the categories
            $('#categories').append(categoryDiv);
            // Clear the category name input
            $('.form-name_category').val('');
            // Add a removal listener
            addRemoveListener(categoryDiv.find('.remove-category'));
            // Update the hidden input
            updateCategoryList();
        }
    });

    // Add listener on the remove button
    const addRemoveListener = (element) => {
        element.click(function() {
            // Delete the category div
            $(this).parent().remove();
            // Update the hidden input
            updateCategoryList();
        });
    };

    $('.remove-category').each(function() {
        addRemoveListener($(this));
    });

    // Update the categories at launch
    updateCategoryList();
});

