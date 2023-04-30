const filterHeaders = document.querySelectorAll('.filter__header');

filterHeaders.forEach(filterHeader => {
  const filterContent = filterHeader.nextElementSibling;
  const collapseBtn = filterHeader.querySelector('.filter__collapse-btn');

  // Add click event to filter header
  filterHeader.addEventListener('click', () => {
    filterContent.classList.toggle('show');
    collapseBtn.classList.toggle('fa-angle-up');
    collapseBtn.classList.toggle('fa-angle-down');

  });

  // Add change event to checkbox
  const checkboxes = filterContent.querySelectorAll('input[type="checkbox"]');
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
      const selectedCategories = getSelectedCategories();
      const url = buildUrl(selectedCategories);
    //   window.location.href = url;
    });
  });
});

// Get selected categories
function getSelectedCategories() {
  const checkboxes = document.querySelectorAll('input[name="manufacturer"]');
  const selectedCategories = [];
  checkboxes.forEach(checkbox => {
    if (checkbox.checked) {
      selectedCategories.push(checkbox.value);
    }
  });
  return selectedCategories;
}

// Build url with selected categories
function buildUrl(selectedCategories) {
    const url = new URL(window.location.href);
    const categories = url.searchParams.getAll('category');
    categories.forEach(category => {
      url.searchParams.delete('category');
    });
    selectedCategories.forEach(category => {
      categories.push(category);
    });
    categories.forEach(category => {
      url.searchParams.append('category', category);
    });
    return url.href;
  }
  
function ApplyFilters() {
    console.log('dsfdsf')
    const selectedFilters = [];
    const checkboxes = document.querySelectorAll('input[name="manufacturer"]:checked');
    checkboxes.forEach(checkbox => {
        selectedFilters.push(checkbox.value);
    });
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('manufacturer', selectedFilters.join(','));
    window.location.href = currentUrl;
}
  