// Общие функции для заказ-нарядов
function initOrders() {
    // Инициализация таблицы заказ-нарядов
    const contractsTable = document.getElementById('contractsTable');
    if (contractsTable) {
        initDataTable(contractsTable);
    }
}

// Функция для загрузки деталей заказ-наряда
async function loadOrderDetails(orderId) {
    try {
        const response = await fetch(`/api/v1/orders/${orderId}`);
        if (!response.ok) throw new Error('Ошибка загрузки данных');
        return await response.json();
    } catch (error) {
        console.error('Error loading order details:', error);
        return null;
    }
}

// Функция для создания отчета по заказ-наряду
function generateOrderReport(orderId, format = 'pdf') {
    const url = `/api/v1/reports/order/${orderId}/download/${format}`;
    window.utils.downloadFile(url);
    
    window.utils.showNotification('Отчет формируется...', 'info');
}

// Функция для обновления статуса заказ-наряда
async function updateOrderStatus(orderId, status) {
    try {
        const response = await fetch(`/api/v1/orders/${orderId}/status`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ status })
        });
        
        if (response.ok) {
            window.utils.showNotification('Статус обновлен', 'success');
            setTimeout(() => location.reload(), 1000);
        } else {
            throw new Error('Ошибка обновления статуса');
        }
    } catch (error) {
        console.error('Error updating order status:', error);
        window.utils.showNotification('Ошибка обновления статуса', 'error');
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

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    initOrders();
    
    // Добавляем обработчики для динамических форм
    document.addEventListener('input', function(e) {
        if (e.target.name && (e.target.name.includes('price') || e.target.name.includes('quantity'))) {
            // Автоматический расчет сумм
            if (typeof calculateTotal === 'function') {
                calculateTotal();
            }
        }
    });
});

// Вспомогательные функции для работы с формами
function initDataTable(table) {
    // Простая инициализация таблицы
    if (table) {
        // Можно добавить сортировку или другие функции
        console.log('Table initialized:', table.id);
    }
}