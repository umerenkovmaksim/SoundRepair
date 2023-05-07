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
    console.log(minPrice)
  
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

function ApplyFilters_2() {
  const selectedFilters = [];
  const checkboxes = document.querySelectorAll('input[name="manufacturer-2"]:checked');
  checkboxes.forEach(checkbox => {
      selectedFilters.push(checkbox.value);
  });
  const currentUrl = new URL(window.location.href);
  if (selectedFilters.length > 0) {
    currentUrl.searchParams.set('manufacturer', selectedFilters.join(','));
  } else {
      currentUrl.searchParams.delete('manufacturer');
  }
  let minPrice = document.getElementById('minPriceInput-2').value;
  let maxPrice = document.getElementById('maxPriceInput-2').value;
  console.log(minPrice)

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

function setPageNumber(pageNumber) {
  var url = new URL(window.location.href);
  url.searchParams.set('page', pageNumber);
  window.location.href = url;
}


const sortNameLink = document.querySelector('.sort-name');
const sortCostLink = document.querySelector('.sort-cost');

sortNameLink.addEventListener('click', (event) => {
  event.preventDefault();
  const currentUrl = new URL(window.location.href);
  currentUrl.searchParams.set('sort_type', 'name');
  window.location.href = currentUrl.toString();
});

sortCostLink.addEventListener('click', (event) => {
  event.preventDefault();
  const currentUrl = new URL(window.location.href);
  currentUrl.searchParams.set('sort_type', 'cost');
  window.location.href = currentUrl.toString();
});
function sortProducts(e) {
  e.preventDefault();
  const sortType = this.getAttribute("data-type");
  const isReverse = this.getAttribute("data-reverse");
  const url = new URL(window.location.href);
  url.searchParams.set("sort_type", sortType);
  url.searchParams.set("is_reverse", isReverse);
  window.location.href = url.toString();
  document.querySelector(".menu-icon").textContent = this.textContent;
}
const menuLinks = document.querySelectorAll(".menu-wrap a");
menuLinks.forEach(link => link.addEventListener("click", sortProducts));
