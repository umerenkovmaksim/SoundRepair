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
});

function ApplyFilters() {
    const selectedFilters = [];
    const checkboxes = document.querySelectorAll('input[name="manufacturer"]:checked');
    checkboxes.forEach(checkbox => {
        selectedFilters.push(checkbox.value);
    });
    const currentUrl = new URL(window.location.href);
    if (selectedFilters.length > 0) {
      currentUrl.searchParams.set('manufacturer', selectedFilters.join(','));
    } else {
        currentUrl.searchParams.delete('manufacturer');
    }
    let minPrice = document.getElementById('minPriceInput').value;
    let maxPrice = document.getElementById('maxPriceInput').value;
  
    // Если значения не были введены, то удаляем параметр
    if (!minPrice && !maxPrice) {
      currentUrl.searchParams.delete('price');
      window.location.href = currentUrl;
      return;
    }
  
    // Если отсутствует minPrice, то устанавливаем его в 0
    if (!minPrice) {
      minPrice = 0;
    }
  
    // Если отсутствует maxPrice, то устанавливаем его в inf
    if (!maxPrice) {
      maxPrice = 'inf';
    }
  
    // Объединяем значения в одну строку и устанавливаем параметр в url
    const priceRange = `${minPrice}-${maxPrice}`;
    currentUrl.searchParams.set('price', priceRange);
    window.location.href = currentUrl;
}
  