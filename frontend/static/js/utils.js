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
        notification.classList.add('show');
    }, 10);
    
    // Автоматически удаляем
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, duration);
}

function getNotificationIcon(type) {
    const icons = {
        'success': '✅',
        'error': '❌',
        'warning': '⚠️',
        'info': 'ℹ️'
    };
    return icons[type] || '💡';
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
            clearInterval(parseInt(container.dataset.intervalId));
            delete container.dataset.intervalId;
        }
    }
}

function updateProgressBar(percent) {
    const bar = document.getElementById('progressBar');
    if (bar) {
        bar.style.width = `${percent}%`;
        bar.setAttribute('aria-valuenow', percent);
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
    
    // Небольшая задержка перед удалением
    setTimeout(() => {
        document.body.removeChild(a);
    }, 100);
}

// Форматирование даты
function formatDate(dateString) {
    if (!dateString) return '-';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit'
        });
    } catch (e) {
        return dateString;
    }
}

function formatDateTime(dateString) {
    if (!dateString) return '-';
    
    try {
        const date = new Date(dateString);
        return date.toLocaleString('ru-RU', {
            year: 'numeric',
            month: '2-digit',
            day: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    } catch (e) {
        return dateString;
    }
}

// Форматирование цены
function formatPrice(amount) {
    const num = parseFloat(amount);
    if (isNaN(num)) return '0,00 ₽';
    
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(num);
}

// Валидация email
function isValidEmail(email) {
    if (!email) return false;
    const re = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
    return re.test(email);
}

// Валидация телефона (российский формат)
function isValidPhone(phone) {
    if (!phone) return false;
    // Убираем все нецифровые символы
    const cleaned = phone.replace(/\D/g, '');
    // Проверяем длину и начинается с 7,8 или 9
    return cleaned.length === 11 && /^[789]/.test(cleaned);
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
    } catch (error) {
        console.warn('API health check failed:', error);
        return false;
    }
}

// Получение параметров из URL
function getUrlParams() {
    const params = new URLSearchParams(window.location.search);
    const result = {};
    for (const [key, value] of params.entries()) {
        result[key] = value;
    }
    return result;
}

// Копирование в буфер обмена
async function copyToClipboard(text) {
    try {
        await navigator.clipboard.writeText(text);
        showNotification('Скопировано в буфер обмена', 'success');
        return true;
    } catch (err) {
        console.error('Failed to copy:', err);
        showNotification('Не удалось скопировать', 'error');
        return false;
    }
}

// Экспорт в CSV
function exportToCSV(data, filename = 'export.csv') {
    if (!data || !data.length) {
        showNotification('Нет данных для экспорта', 'warning');
        return;
    }
    
    // Получаем заголовки
    const headers = Object.keys(data[0]);
    
    // Формируем CSV
    let csv = headers.join(',') + '\n';
    
    data.forEach(row => {
        const values = headers.map(header => {
            const value = row[header] || '';
            // Экранируем кавычки и оборачиваем в кавычки, если есть запятые
            if (value.toString().includes(',')) {
                return `"${value.toString().replace(/"/g, '""')}"`;
            }
            return value;
        });
        csv += values.join(',') + '\n';
    });
    
    // Скачиваем
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    downloadFile(url, filename);
    URL.revokeObjectURL(url);
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
    checkApiHealth,
    getUrlParams,
    copyToClipboard,
    exportToCSV
};