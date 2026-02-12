// Общие функции для заказ-нарядов
function initOrders() {
    // Инициализация таблицы заказ-нарядов
    const contractsTable = document.getElementById('contractsTable');
    if (contractsTable) {
        initDataTable(contractsTable);
    }
}

// Функция для инициализации формы заказ-наряда (новая)
function initOrderForm() {
    const contractSelect = document.getElementById('contractSelect');
    
    if (contractSelect) {
        contractSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            updateContractDetails(selectedOption);
        });
        
        // Автоматически показываем детали при загрузке, если выбран договор
        if (contractSelect.value) {
            const selectedOption = contractSelect.options[contractSelect.selectedIndex];
            updateContractDetails(selectedOption);
        }
    }
    
    const addServiceBtn = document.getElementById('addServiceBtn');
    const addPartBtn = document.getElementById('addPartBtn');
    
    if (addServiceBtn) {
        addServiceBtn.addEventListener('click', addServiceRow);
    }
    
    if (addPartBtn) {
        addPartBtn.addEventListener('click', addPartRow);
    }
}

// Функция для обновления деталей договора (новая)
function updateContractDetails(option) {
    const detailsCard = document.getElementById('contractDetails');
    
    if (!detailsCard) return;
    
    if (!option || !option.value) {
        detailsCard.classList.add('hidden');
        return;
    }
    
    const clientName = option.getAttribute('data-client');
    const clientPhone = option.getAttribute('data-client-phone');
    const clientEmail = option.getAttribute('data-client-email');
    const carInfo = option.getAttribute('data-car');
    const carYear = option.getAttribute('data-car-year');
    const carVin = option.getAttribute('data-car-vin');
    
    const clientEl = document.getElementById('contractClient');
    const phoneEl = document.getElementById('contractClientPhone');
    const emailEl = document.getElementById('contractClientEmail');
    const carEl = document.getElementById('contractCar');
    const yearEl = document.getElementById('contractCarYear');
    const vinEl = document.getElementById('contractCarVin');
    
    if (clientEl) clientEl.textContent = clientName || '-';
    if (phoneEl) phoneEl.textContent = clientPhone || '-';
    if (emailEl) emailEl.textContent = clientEmail || '-';
    if (carEl) carEl.textContent = carInfo || '-';
    if (yearEl) yearEl.textContent = carYear || '-';
    if (vinEl) vinEl.textContent = carVin || '-';
    
    detailsCard.classList.remove('hidden');
}

// Функция для добавления строки услуги (новая)
function addServiceRow(serviceData = null) {
    const servicesTable = document.getElementById('servicesTable');
    if (!servicesTable) return;
    
    const tbody = servicesTable.querySelector('tbody');
    const noServicesRow = document.getElementById('noServicesRow');
    
    if (noServicesRow) {
        noServicesRow.remove();
    }
    
    // Получаем следующий индекс
    const rows = tbody.querySelectorAll('tr');
    let nextIndex = 1;
    
    if (serviceData && serviceData.counter) {
        nextIndex = serviceData.counter;
    } else if (window.serviceCounter) {
        window.serviceCounter = (window.serviceCounter || 0) + 1;
        nextIndex = window.serviceCounter;
    } else {
        nextIndex = rows.length + 1;
        window.serviceCounter = rows.length + 1;
    }
    
    const row = document.createElement('tr');
    
    if (serviceData && serviceData.name) {
        row.innerHTML = `
            <td>
                <input type="text" name="service_name_${nextIndex}" 
                       value="${serviceData.name}" required readonly class="form-control">
            </td>
            <td>
                <input type="number" name="service_quantity_${nextIndex}" 
                       min="1" value="1" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <input type="number" name="service_price_${nextIndex}" 
                       step="0.01" min="0" value="${serviceData.price || 0}" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <button type="button" class="btn-small btn-danger" 
                        onclick="removeRow(this)">Удалить</button>
            </td>
        `;
    } else {
        row.innerHTML = `
            <td>
                <input type="text" name="service_name_${nextIndex}" 
                       placeholder="Наименование услуги" required class="form-control">
            </td>
            <td>
                <input type="number" name="service_quantity_${nextIndex}" 
                       min="1" value="1" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <input type="number" name="service_price_${nextIndex}" 
                       step="0.01" min="0" placeholder="0.00" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <button type="button" class="btn-small btn-danger" 
                        onclick="removeRow(this)">Удалить</button>
            </td>
        `;
    }
    
    tbody.appendChild(row);
    
    if (typeof calculateTotal === 'function') {
        calculateTotal();
    }
}

// Функция для добавления строки запчасти (новая)
function addPartRow(partData = null) {
    const partsTable = document.getElementById('partsTable');
    if (!partsTable) return;
    
    const tbody = partsTable.querySelector('tbody');
    const noPartsRow = document.getElementById('noPartsRow');
    
    if (noPartsRow) {
        noPartsRow.remove();
    }
    
    // Получаем следующий индекс
    const rows = tbody.querySelectorAll('tr');
    let nextIndex = 1;
    
    if (partData && partData.counter) {
        nextIndex = partData.counter;
    } else if (window.partCounter) {
        window.partCounter = (window.partCounter || 0) + 1;
        nextIndex = window.partCounter;
    } else {
        nextIndex = rows.length + 1;
        window.partCounter = rows.length + 1;
    }
    
    const row = document.createElement('tr');
    
    if (partData && partData.name) {
        row.innerHTML = `
            <td>
                <input type="text" name="part_name_${nextIndex}" 
                       value="${partData.name}" required readonly class="form-control">
            </td>
            <td>
                <input type="number" name="part_quantity_${nextIndex}" 
                       min="1" value="1" max="${partData.stock_quantity || 999}" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <input type="number" name="part_price_${nextIndex}" 
                       step="0.01" min="0" value="${partData.price || 0}" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <span class="stock-badge ${partData.stock_quantity > 0 ? 'in-stock' : 'out-of-stock'}">
                    ${partData.stock_quantity || 0} шт.
                </span>
                <input type="hidden" name="part_stock_${nextIndex}" value="${partData.stock_quantity || 0}">
            </td>
            <td>
                <button type="button" class="btn-small btn-danger" 
                        onclick="removeRow(this)">Удалить</button>
            </td>
        `;
    } else {
        row.innerHTML = `
            <td>
                <input type="text" name="part_name_${nextIndex}" 
                       placeholder="Наименование запчасти" required class="form-control">
            </td>
            <td>
                <input type="number" name="part_quantity_${nextIndex}" 
                       min="1" value="1" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <input type="number" name="part_price_${nextIndex}" 
                       step="0.01" min="0" placeholder="0.00" required
                       oninput="calculateTotal()" class="form-control">
            </td>
            <td>
                <span class="stock-badge unknown">?</span>
            </td>
            <td>
                <button type="button" class="btn-small btn-danger" 
                        onclick="removeRow(this)">Удалить</button>
            </td>
        `;
    }
    
    tbody.appendChild(row);
    
    if (typeof calculateTotal === 'function') {
        calculateTotal();
    }
}

// Функция для удаления строки (новая)
function removeRow(button) {
    const row = button.closest('tr');
    if (!row) return;
    
    row.remove();
    
    if (typeof calculateTotal === 'function') {
        calculateTotal();
    }
    
    // Проверяем, нужно ли показать сообщение "нет данных"
    const table = row.closest('table');
    if (!table) return;
    
    const tbody = table.querySelector('tbody');
    if (!tbody) return;
    
    if (table.id === 'servicesTable' && tbody.querySelectorAll('tr').length === 0) {
        tbody.innerHTML = '<tr id="noServicesRow" class="empty-row"><td colspan="4">Нет добавленных услуг</td></tr>';
    }
    
    if (table.id === 'partsTable' && tbody.querySelectorAll('tr').length === 0) {
        tbody.innerHTML = '<tr id="noPartsRow" class="empty-row"><td colspan="5">Нет добавленных запчастей</td></tr>';
    }
}

// Функция для расчета итоговой суммы (новая)
function calculateTotal() {
    let servicesTotal = 0;
    let partsTotal = 0;
    
    // Считаем услуги
    const servicePriceInputs = document.querySelectorAll('input[name^="service_price_"]');
    const serviceQuantityInputs = document.querySelectorAll('input[name^="service_quantity_"]');
    
    servicePriceInputs.forEach((input, index) => {
        const price = parseFloat(input.value) || 0;
        const quantity = parseFloat(serviceQuantityInputs[index]?.value) || 1;
        servicesTotal += price * quantity;
    });
    
    // Считаем запчасти
    const partPriceInputs = document.querySelectorAll('input[name^="part_price_"]');
    const partQuantityInputs = document.querySelectorAll('input[name^="part_quantity_"]');
    
    partPriceInputs.forEach((input, index) => {
        const price = parseFloat(input.value) || 0;
        const quantity = parseFloat(partQuantityInputs[index]?.value) || 1;
        partsTotal += price * quantity;
    });
    
    // Обновляем отображение
    const servicesTotalEl = document.getElementById('servicesTotal');
    const partsTotalEl = document.getElementById('partsTotal');
    const totalAmountEl = document.getElementById('totalAmount');
    
    if (servicesTotalEl) {
        servicesTotalEl.textContent = servicesTotal.toFixed(2) + ' ₽';
    }
    
    if (partsTotalEl) {
        partsTotalEl.textContent = partsTotal.toFixed(2) + ' ₽';
    }
    
    if (totalAmountEl) {
        const totalAmount = servicesTotal + partsTotal;
        totalAmountEl.textContent = totalAmount.toFixed(2) + ' ₽';
    }
}

// Функция для загрузки доступных услуг (новая)
async function loadAvailableServices() {
    try {
        const response = await fetch('/api/v1/services');
        if (!response.ok) throw new Error('Ошибка загрузки');
        
        const services = await response.json();
        const modalBody = document.getElementById('availableServicesBody');
        
        if (!modalBody) return;
        
        modalBody.innerHTML = '';
        
        services.forEach(service => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${service.name}</td>
                <td>${service.price || 0} ₽</td>
                <td>${service.description || ''}</td>
                <td>
                    <button type="button" class="btn-small btn-primary" 
                            onclick="selectService(${JSON.stringify(service).replace(/"/g, '&quot;')})">
                        Выбрать
                    </button>
                </td>
            `;
            modalBody.appendChild(row);
        });
        
        const modal = document.getElementById('servicesModal');
        if (modal) modal.style.display = 'block';
        
    } catch (error) {
        console.error('Error loading services:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка загрузки услуг', 'error');
        }
    }
}

// Функция для загрузки доступных запчастей (новая)
async function loadAvailableParts() {
    try {
        const response = await fetch('/api/v1/spare-parts');
        if (!response.ok) throw new Error('Ошибка загрузки');
        
        const parts = await response.json();
        const modalBody = document.getElementById('availablePartsBody');
        
        if (!modalBody) return;
        
        modalBody.innerHTML = '';
        
        parts.forEach(part => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${part.name}</td>
                <td>${part.code || '—'}</td>
                <td>${part.price || 0} ₽</td>
                <td>
                    <span class="stock-badge ${part.stock_quantity > 0 ? 'in-stock' : 'out-of-stock'}">
                        ${part.stock_quantity || 0} шт.
                    </span>
                </td>
                <td>
                    <button type="button" class="btn-small btn-primary" 
                            onclick="selectPart(${JSON.stringify(part).replace(/"/g, '&quot;')})"
                            ${part.stock_quantity <= 0 ? 'disabled' : ''}>
                        Выбрать
                    </button>
                </td>
            `;
            modalBody.appendChild(row);
        });
        
        const modal = document.getElementById('partsModal');
        if (modal) modal.style.display = 'block';
        
    } catch (error) {
        console.error('Error loading parts:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка загрузки запчастей', 'error');
        }
    }
}

// Функция для поиска запчастей (новая)
function searchParts(query) {
    const rows = document.querySelectorAll('#availablePartsBody tr');
    
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        if (text.includes(query.toLowerCase())) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }
    });
}

// Функция для выбора услуги (новая)
function selectService(service) {
    if (typeof addServiceRow === 'function') {
        addServiceRow(service);
    }
    closeServicesModal();
}

// Функция для выбора запчасти (новая)
function selectPart(part) {
    if (typeof addPartRow === 'function') {
        addPartRow(part);
    }
    closePartsModal();
}

// Функция для закрытия модального окна услуг (новая)
function closeServicesModal() {
    const modal = document.getElementById('servicesModal');
    if (modal) modal.style.display = 'none';
}

// Функция для закрытия модального окна запчастей (новая)
function closePartsModal() {
    const modal = document.getElementById('partsModal');
    if (modal) modal.style.display = 'none';
}

// Функция для предпросмотра заказ-наряда (новая)
function previewOrder() {
    if (window.utils) {
        window.utils.showNotification('Функция предпросмотра в разработке', 'info');
    }
}

// Функция для удаления заказ-наряда (новая)
async function deleteOrder(orderId) {
    if (!confirm('Вы уверены, что хотите удалить заказ-наряд? Это действие нельзя отменить.')) {
        return;
    }
    
    try {
        const response = await fetch(`/orders/api/${orderId}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            if (window.utils) {
                window.utils.showNotification('Заказ-наряд успешно удален', 'success');
            }
            setTimeout(() => {
                window.location.href = '/orders';
            }, 1500);
        } else {
            const error = await response.json();
            throw new Error(error.detail || 'Ошибка при удалении');
        }
    } catch (error) {
        console.error('Error deleting order:', error);
        if (window.utils) {
            window.utils.showNotification(error.message || 'Ошибка при удалении заказ-наряда', 'error');
        }
    }
}

// Функция для проверки наличия запчастей
function checkPartsAvailability() {
    const quantityInputs = document.querySelectorAll('input[name^="part_quantity_"]');
    const stockInputs = document.querySelectorAll('input[name^="part_stock_"]');
    
    let hasIssues = false;
    
    quantityInputs.forEach((input, index) => {
        const quantity = parseInt(input.value) || 0;
        const stock = parseInt(stockInputs[index]?.value) || 0;
        
        if (quantity > stock) {
            input.style.borderColor = '#dc3545';
            hasIssues = true;
        } else {
            input.style.borderColor = '';
        }
    });
    
    return !hasIssues;
}

// Функция для загрузки деталей заказ-наряда
async function loadOrderDetails(orderId) {
    try {
        const response = await fetch(`/orders/api/${orderId}`);
        if (!response.ok) throw new Error('Ошибка загрузки данных');
        return await response.json();
    } catch (error) {
        console.error('Error loading order details:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка загрузки данных', 'error');
        }
        return null;
    }
}

// Функция для создания отчета по заказ-наряду
function generateOrderReport(orderId, format = 'pdf') {
    const url = `/api/reports/order/${orderId}/download/${format}`;
    if (window.utils) {
        window.utils.downloadFile(url);
        window.utils.showNotification('Отчет формируется...', 'info');
    }
}

// Функция для обновления статуса заказ-наряда
async function updateOrderStatus(orderId, status) {
    try {
        const response = await fetch(`/orders/api/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status })
        });
        
        if (response.ok) {
            if (window.utils) {
                window.utils.showNotification('Статус обновлен', 'success');
            }
            setTimeout(() => location.reload(), 1000);
        } else {
            throw new Error('Ошибка обновления статуса');
        }
    } catch (error) {
        console.error('Error updating order status:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка обновления статуса', 'error');
        }
    }
}

// Инициализация таблицы
function initDataTable(table) {
    if (table) {
        console.log('Table initialized:', table.id);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initOrders();
    
    // Инициализация формы заказ-наряда, если она есть на странице
    if (document.getElementById('contractSelect')) {
        initOrderForm();
        
        // Добавляем одну строку по умолчанию для новой формы
        if (!document.querySelector('#servicesTable tbody tr:not(#noServicesRow)')) {
            addServiceRow();
        }
        
        if (!document.querySelector('#partsTable tbody tr:not(#noPartsRow)')) {
            addPartRow();
        }
    }
    
    // Добавляем обработчики для динамических форм
    document.addEventListener('input', function(e) {
        if (e.target.name && (e.target.name.includes('price') || e.target.name.includes('quantity'))) {
            if (typeof calculateTotal === 'function') {
                calculateTotal();
            }
        }
    });
});

// Экспорт функций в глобальную область
window.initOrderForm = initOrderForm;
window.updateContractDetails = updateContractDetails;
window.addServiceRow = addServiceRow;
window.addPartRow = addPartRow;
window.removeRow = removeRow;
window.calculateTotal = calculateTotal;
window.loadAvailableServices = loadAvailableServices;
window.loadAvailableParts = loadAvailableParts;
window.searchParts = searchParts;
window.selectService = selectService;
window.selectPart = selectPart;
window.closeServicesModal = closeServicesModal;
window.closePartsModal = closePartsModal;
window.previewOrder = previewOrder;
window.deleteOrder = deleteOrder;
window.checkPartsAvailability = checkPartsAvailability;
window.loadOrderDetails = loadOrderDetails;
window.generateOrderReport = generateOrderReport;
window.updateOrderStatus = updateOrderStatus;