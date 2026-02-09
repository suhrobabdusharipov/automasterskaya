// Уведомления
function showNotification(message, type = 'info', duration = 5000) {
    // Удаляем старые уведомления
    const oldNotifications = document.querySelectorAll('.notification');
    oldNotifications.forEach(n => n.remove());
    
    // Создаем новое уведомление
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="notification-icon">${getNotificationIcon(type)}</span>
        <span class="notification-text">${message}</span>
    `;
    
    document.body.appendChild(notification);
    
    // Анимация появления
    setTimeout(() => {
        notification.style.animation = 'slideIn 0.3s ease-out';
    }, 10);
    
    // Автоматически удаляем
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out forwards';
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

function getNotificationIcon(type) {
    switch(type) {
        case 'success': return '✅';
        case 'error': return '❌';
        case 'warning': return '⚠️';
        case 'info': return 'ℹ️';
        default: return '💡';
    }
}

// Прогресс-бар
function showProgress(message = 'Подготовка документа...') {
    const container = document.getElementById('progressContainer');
    const text = document.getElementById('progressText');
    
    if (container && text) {
        text.textContent = message;
        container.style.display = 'block';
        
        // Анимация прогресса
        let progress = 0;
        const interval = setInterval(() => {
            progress += 5;
            if (progress > 90) {
                clearInterval(interval);
            }
            updateProgressBar(progress);
        }, 100);
        
        // Сохраняем interval ID
        container.dataset.intervalId = interval;
    }
}

function hideProgress() {
    const container = document.getElementById('progressContainer');
    if (container) {
        container.style.display = 'none';
        updateProgressBar(0);
        
        // Очищаем interval
        if (container.dataset.intervalId) {
            clearInterval(container.dataset.intervalId);
        }
    }
}

function updateProgressBar(percent) {
    const bar = document.getElementById('progressBar');
    if (bar) {
        bar.style.width = `${percent}%`;
    }
}

// Загрузка файла
function downloadFile(url, filename = null) {
    const a = document.createElement('a');
    a.href = url;
    
    if (filename) {
        a.download = filename;
    }
    
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
}

// Форматирование даты
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
}

function formatDateTime(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Форматирование цены
function formatPrice(amount) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 2
    }).format(amount);
}

// Валидация email
function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

// Валидация телефона (российский формат)
function isValidPhone(phone) {
    const re = /^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$/;
    return re.test(phone);
}

// Дебаунс
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Обработка ошибок
function handleError(error, userMessage = 'Произошла ошибка') {
    console.error(error);
    showNotification(`${userMessage}: ${error.message || 'Неизвестная ошибка'}`, 'error');
    hideProgress();
}

// Проверка подключения к API
async function checkApiHealth() {
    try {
        const response = await fetch('/health');
        return response.ok;
    } catch {
        return false;
    }
}

// Экспорт функций
window.utils = {
    showNotification,
    showProgress,
    hideProgress,
    downloadFile,
    formatDate,
    formatDateTime,
    formatPrice,
    isValidEmail,
    isValidPhone,
    debounce,
    handleError,
    checkApiHealth
};