updateWishlistHeart();
function getWishlist() {
    // Получаем текущий список понравившихся товаров из localStorage
    var wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];
    
    // Возвращаем список товаров в формате JSON
    return wishlist;
  }
  
function AddToWishlist(event) {
    // Получаем информацию о товаре из кнопки или других элементов на странице
    var button = event.target.classList.contains('add-wishlist-btn') ? event.target : event.target.parentNode;
    var productId = button.getAttribute('data-id');
    var productName = button.getAttribute('data-name');
    var productPrice = button.getAttribute('data-price');
    var productPriceWithSale = button.getAttribute('data-price_with_sale');
    var productSale = button.getAttribute('data-sale');
    var productImage = button.getAttribute('data-image_href');
    
    // Получаем текущий список понравившихся товаров из localStorage
    var wishlist = getWishlist();
    
    // Проверяем, есть ли товар уже в списке понравившихся
    var existingProduct = wishlist.find(function(item) {
      return item.productId === productId;
    });
    
    // Если товар уже существует, не добавляем его повторно
    if (existingProduct) {
      removeItemFromWishlist(productId, false);
      updateWishlistHeart();
      return;
    }
    
    // Добавляем новый товар в список понравившихся
    wishlist.push({
      productId: productId,
      productName: productName,
      productPrice: productPrice,
      productPriceWithSale: productPriceWithSale,
      productSale: productSale,
      productImage: productImage
    });
    // Сохраняем обновленный список понравившихся товаров в localStorage
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    updateWishlistHeart();
  }
  
  // Находим все кнопки с классом "add-wishlist-btn" и назначаем обработчик события клика на каждую из них
  var addToWishlistButtons = document.querySelectorAll('.add-wishlist-btn');
  addToWishlistButtons.forEach(function(button) {
    button.addEventListener('click', AddToWishlist);
  });
  
function clearWishlist() {
    localStorage.removeItem('wishlist');
    updateWishlist();
}
  
function updateWishlist() {
    var wishlistData = getWishlist();
    var wishlistTable = document.getElementById('wishlist-table');
    wishlistTable.innerHTML = '';
    const myElement = document.getElementById('page-url');
    const url = myElement.dataset.url;

  // Перебираем каждый товар в списке понравившихся
  wishlistData.forEach(function(item) {
    
    var row = document.createElement('tr'); // Создаем новую строку для товара

    // Создаем ячейки для каждого столбца
    var removeCell = document.createElement('td');
    removeCell.className = 'product-remove';
    removeCell.innerHTML = '<button class="product-remove-btn" onclick="removeItemFromWishlist(' + item.productId + ')"><i class="fa fa-times" aria-hidden="true"></i></button>';

    var thumbnailCell = document.createElement('td');
    thumbnailCell.className = 'product-thumbnail';
    thumbnailCell.innerHTML = '<a href="' + url + '/product/' + item.productId + '"><img src="' + item.productImage + '" alt="cart-image" /></a>';

    var nameCell = document.createElement('td');
    nameCell.className = 'product-name';
    nameCell.innerHTML = '<a href="' + url + '/product/' + item.productId + '">' + item.productName + '</a>';

    var priceCell = document.createElement('td');
    priceCell.className = 'product-price';
    priceCell.innerHTML = '<span class="amount">' + item.productPriceWithSale + '₽</span>';

    var addToCartCell = document.createElement('td');
    addToCartCell.className = 'product-add-to-cart';
    
    var addButton = document.createElement('button');
    addButton.className = 'add-cart-btn';
    addButton.setAttribute('data-id', item.productId);
    addButton.setAttribute('data-name', item.productName);
    addButton.setAttribute('data-price', item.productPrice);
    addButton.setAttribute('data-price_with_sale', item.productPriceWithSale);
    addButton.setAttribute('data-sale', item.productSale);
    addButton.setAttribute('data-image_href', item.productImage);
    addButton.setAttribute('data-toggle', 'tooltip');
    addButton.setAttribute('title', 'Добавить в корзину');
    addButton.textContent = 'В корзину';
    
    addToCartCell.appendChild(addButton);
    

    // Добавляем ячейки в строку
    row.appendChild(removeCell);
    row.appendChild(thumbnailCell);
    row.appendChild(nameCell);
    row.appendChild(priceCell);
    row.appendChild(addToCartCell);

    // Добавляем строку в таблицу
    wishlistTable.appendChild(row);
  });
}

function removeItemFromWishlist(itemId, update=true) {
    var wishlistData = getWishlist(); // Получаем список товаров из localStorage
  
    var updatedWishlist = wishlistData.filter(function(item) {
        return item.productId !== itemId.toString();
      });
    
    localStorage.setItem('wishlist', JSON.stringify(updatedWishlist));
    if (update) {updateWishlist()};
  }
function isInWishlist(productId) {
    // Получаем список товаров из localStorage
    var wishlistItems = getWishlist();
  
    // Проверяем наличие товара в списке по его ID
    return wishlistItems.some(function(item) {
      return item.productId === productId;
    });
  }
  
function updateWishlistHeart() {
    var cartButtons = document.querySelectorAll('.add-wishlist-btn');

    cartButtons.forEach(function(button) {
      var productId = button.dataset.id;
      var icon = button.querySelector('i.fa');
      if (isInWishlist(productId)) {
        icon.classList.remove('fa-heart');
        icon.classList.add('fa-check');
      } else {
        icon.classList.remove('fa-check');
        icon.classList.add('fa-heart');
      }
  });
}
updateWishlist();
updateCart();
