function openDialog() {
    var orderDialog = document.getElementById('orderDialog');
    orderDialog.showModal();
}

function closeDialog() {
    var orderDialog = document.getElementById('orderDialog');
    orderDialog.close();
}

function submitOrder() {
    var name = document.getElementById("nameInput").value;
    var surname = document.getElementById("surnameInput").value;
    var contact = document.getElementById("contactInput").value;
    var total = document.querySelector('.total-amount').textContent;
    
    // Проверка корректности данных
    var namePattern = /^[a-zA-Zа-яА-Я]+$/; // Регулярное выражение для имени
    var surnamePattern = /^[a-zA-Zа-яА-Я]+$/; // Регулярное выражение для фамилии
    var contactPattern = /^\+?[1-9]\d{1,14}$/; // Регулярное выражение для проверки мобильного телефона
    
    var nameNotification = document.getElementById("nameNotification");
    var surnameNotification = document.getElementById("surnameNotification");
    var contactNotification = document.getElementById("contactNotification");
    
    nameNotification.textContent = "";
    surnameNotification.textContent = "";
    contactNotification.textContent = "";
    
    if (!name.match(namePattern)) {
        showNotification(nameNotification, "Введите корректное имя.");
    }
    
    if (!surname.match(surnamePattern)) {
        showNotification(surnameNotification, "Введите корректную фамилию.");
    }
    
    if (!contact.match(contactPattern)) {
        showNotification(contactNotification, "Введите корректный мобильный телефон.");
    }
    if (!name.match(namePattern) || !surname.match(surnamePattern) || !contact.match(contactPattern)) {
        return;
    }
    
    // Отправка данных на сервер
    var orderData = {
        name: name,
        surname: surname,
        contact: contact,
        cart: getCartItems(),
        total: total
    };
    
    // Отправка данных на сервер в формате JSON
    fetch('/get_user_data', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(orderData)
      })
    .then(function(response) {
    if (response.ok) {
        showAlertModal('УСПЕШНО ОТПРАВЛЕН ЗАКАЗ!', 'Ваш заказ был успешно отправлен.');
    } else {
        showAlertModal('ОШИБКА ОТПРАВКИ ЗАКАЗА!', 'При отправке заказа произошла ошибка.');
    }
    })
    .catch(function(error) {
        showAlertModal('ОШИБКА СЕРВЕРА!', 'При сервере произошла ошибка.');
    });
    }
function showAlertModal(title, message) {
    var successDialog = document.getElementById('successDialog');
    var modalTitle = successDialog.querySelector('h2');
    var modalMessage = successDialog.querySelector('p');
    modalTitle.textContent = title;
    modalMessage.textContent = message;
    closeDialog();
    successDialog.showModal();
}
function showNotification(message, type) {
    // Создание элемента уведомления
    var notification = document.createElement('div');
    notification.className = 'notification ' + type;
    notification.textContent = message;

    // Добавление уведомления в документ
    var container = document.getElementById('notificationContainer');
    container.appendChild(notification);

    // Удаление уведомления через некоторое время
    setTimeout(function() {
    container.removeChild(notification);
    }, 3000); // Время отображения уведомления в миллисекундах
}
function closeSuccessDialog() {
    var successDialog = document.getElementById('successDialog');
    successDialog.close();
  }