document.addEventListener('DOMContentLoaded', (event) => {
    document.querySelector('.category-add').addEventListener('click', function() {
        const categoryName = document.querySelector('.form-name_category').value.trim();
        if (categoryName) {
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'category';
            categoryDiv.innerHTML = `${categoryName} <span class="remove-category">X</span>`;
            document.querySelector('#categories').appendChild(categoryDiv);
            document.querySelector('.form-name_category').value = ''; // Clear input field after adding
            addRemoveListener(categoryDiv.querySelector('.remove-category'));
        }
    });

    const addRemoveListener = (element) => {
        element.addEventListener('click', function() {
            this.parentNode.remove();
        });
    };

    // Add remove listeners to existing categories
    document.querySelectorAll('.remove-category').forEach(addRemoveListener);
});
