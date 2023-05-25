// Получение информации о товарах из LocalStorage
const getCartItems = () => {
    const items = localStorage.getItem('cartItems');
    const cartCounterElement = document.querySelector('.cart-counter');
    const cartSubTotal = document.querySelector('.subtotal-amount');
    const cartTotal = document.querySelector('.total-amount');
    const jsonItems = JSON.parse(items);
    if (!jsonItems) {
        const cartItemCount = 0;
        cartCounterElement.textContent = cartItemCount.toString();
    } else {
        const cartItemCount = jsonItems.length;
        cartCounterElement.textContent = cartItemCount.toString();
    }
    if (cartSubTotal) {
        cartSubTotal.textContent = getCartSubTotal(jsonItems).toString() + '₽';
        cartTotal.textContent = getCartTotal(jsonItems).toString() + '₽';
    }
    if (items) {
      return jsonItems;
    } else {
      return [];
    }
  }
  const updateCart = () => {
    const jsonItems = getCartItems();
    const cartCounterElement = document.querySelector('.cart-counter');
    const cartSubTotal = document.querySelector('.subtotal-amount');
    const cartTotal = document.querySelector('.total-amount');
    if (!jsonItems) {
        const cartItemCount = 0;
        cartCounterElement.textContent = cartItemCount.toString();
    } else {
        const cartItemCount = jsonItems.length;
        cartCounterElement.textContent = cartItemCount.toString();
    }
    if (cartSubTotal) {
        cartSubTotal.textContent = getCartSubTotal().toString() + '₽';
        cartTotal.textContent = getCartTotal().toString() + '₽';
    }
  }
  // Добавление товара в корзину
  const addToCart = (item) => {
    let cartItems = getCartItems();
    const existingItem = cartItems.find((i) => i.id === item.id);
    if (existingItem) {
      existingItem.quantity += item.quantity;
    } else {
      cartItems.push(item);
    }
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    updateCart();
    updateButton(item.id);
  }
  
  // Удаление товара из корзины
  const removeFromCart = (id) => {
    let cartItems = getCartItems();
    console.log(cartItems);
    cartItems = cartItems.filter((i) => i.id !== id);
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
    console.log(getCartItems());
    updateCart();
  }
  
  // Получение общей суммы товаров в корзине
  const getCartSubTotal = (cartItems = getCartItems()) => {
    if (cartItems) {
        return cartItems.reduce((total, item) => total + (item.price * item.quantity), 0);
    } else {
        return 0;
    }
  }
  const getCartTotal = (cartItems = getCartItems()) => {
    if (cartItems) {
        return cartItems.reduce((total, item) => total + (item.price_with_sale * item.quantity), 0);
    } else {
        return 0;
    }
  }
  
  // Получение количества товаров в корзине
  const getCartItemCount = () => {
    let cartItems = getCartItems();
    return cartItems.reduce((total, item) => total + item.quantity, 0);
  }
  
  // Очистка корзины
  const clearCart = () => {
    localStorage.removeItem('cartItems');
    updateCart();
  }
  function updateQuantity(input) {
    var quantity = parseInt(input.value);
    var productId = input.getAttribute("data-id");
    // Обновляем количество товаров в локальном хранилище
    var cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    var updatedCartItems = cartItems.map(function(item) {
      if (item.id === productId) {
        item.quantity = quantity;
      }
      return item;
    });
    
    localStorage.setItem("cartItems", JSON.stringify(updatedCartItems));
    var productPrice = parseInt(input.dataset.price);
    var totalPrice = productPrice * quantity;
    var subtotalElement = document.getElementById(`subtotal-${productId}`);
    subtotalElement.innerHTML = totalPrice + '₽'; // Обновляем сумму
    // Обновляем цену на странице
    updateCart();
  }
  function isInCart(productId) {
    var cartItems = JSON.parse(localStorage.getItem("cartItems")) || [];
    return cartItems.some(function(item) {
      return item.id === productId;
    });
  }
  
  // Изменение кнопки, если товар есть в корзине
  function updateButton(productId) {
    var button = document.querySelector('button[data-id="' + productId + '"]');
    console.log(button);
    if (isInCart(productId)) {
      button.innerHTML = "УЖЕ В КОРЗИНЕ";
      button.onclick = function() {
        var currentUrl = window.location.href;
        var newUrl = currentUrl.split('/')[0] + '/cart';
        window.location.href = newUrl;
      };
    } else {
      button.innerHTML = "В КОРЗИНУ";
      button.onclick = function() {
        addToCart(productId);
      };
    }
  }
const addToCartButtons = document.querySelectorAll('.add-cart-btn');

addToCartButtons.forEach(button => {
    button.addEventListener('click', () => {
      const product = {
        id: button.getAttribute('data-id'),
        name: button.getAttribute('data-name'),
        image_href: button.getAttribute('data-image_href'),
        price: button.getAttribute('data-price'),
        sale: button.getAttribute('data-sale'),
        price_with_sale: button.getAttribute('data-price_with_sale'),
        quantity: 1
      };
      addToCart(product);
    });
  });


const cartItems = getCartItems();
const myElement = document.getElementById('page-url');
const url = myElement.dataset.url;

const cartItemsContainer = document.getElementById('cart-items');
cartItems.forEach(item => {
const row = document.createElement('tr');
row.setAttribute('data-id', `${item.id}`)
row.innerHTML = `
      <td class="product-thumbnail">
        <a href="${url}/product/${item.id}"><img src="${item.image_href}" alt="cart-image" /></a>
      </td>
      <td class="product-name"><a href="${url}/product/${item.id}">${item.name}</a></td>
      <td class="product-price"><span class="amount">${item.price}₽</span></td>
      <td class="product-sale">${item.sale ? item.sale + '%' : '0%'}</td>
      <td class="product-quantity"><input type="number" onchange="updateQuantity(this)" data-price="${item.price_with_sale}" data-id="${item.id}" value="${item.quantity}"></td>
      <td class="product-subtotal"><span class="amount" id="subtotal-${item.id}">${item.price_with_sale * item.quantity}₽</span></td>
      <td class="product-remove"><button class="product-remove-btn"><i class="fa fa-times" aria-hidden="true"></i></button></td>
    `;
cartItemsContainer.appendChild(row);
});
// Получение кнопок "Удалить" со страницы
const removeFromCartButtons = document.querySelectorAll('.product-remove-btn');

// Добавление обработчика события клика на каждую кнопку
removeFromCartButtons.forEach(button => {
  button.addEventListener('click', () => {
    const row = button.closest('tr'); // Получение родительской строки
    const productId = row.dataset.id; // Получение id товара из атрибута data
    removeFromCart(productId); // Удаление товара из корзины
    row.remove(); // Удаление строки из таблицы
    updateCart(); // Обновление общей стоимости корзины
  });
});

// Получение кнопки "Очистить корзину"
const clearCartButton = document.querySelector('.clear-cart');

// Добавление обработчика события клика на кнопку
clearCartButton.addEventListener('click', () => {
  clearCart(); // Очистка корзины
  const cartItemsContainer = document.getElementById('cart-items');
  cartItemsContainer.innerHTML = ''; // Удаление всех товаров из таблицы
  updateCart(); // Обновление общей стоимости корзины
});
