// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Инициализация утилит
    if (window.utils) {
        window.utils.checkApiHealth().then(isHealthy => {
            if (!isHealthy) {
                console.warn('API недоступен');
            }
        });
    }
    
    // Инициализация всех динамических элементов
    initDynamicElements();
    
    // Инициализация горячих клавиш
    initHotkeys();
    
    // Инициализация обработчиков форм
    initForms();
    
    // Инициализация модальных окон
    initModals();
});

// Инициализация динамических элементов
function initDynamicElements() {
    // Инициализация выпадающих меню
    const dropdowns = document.querySelectorAll('.dropdown');
    dropdowns.forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            // Удаляем старые обработчики
            const newToggle = toggle.cloneNode(true);
            toggle.parentNode.replaceChild(newToggle, toggle);
            
            newToggle.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                
                // Закрываем все другие меню
                document.querySelectorAll('.dropdown-menu.show').forEach(m => {
                    if (m !== menu) m.classList.remove('show');
                });
                
                menu.classList.toggle('show');
            });
        }
    });
    
    // Закрытие при клике вне меню
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.dropdown')) {
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
        }
    });
    
    // Инициализация табов
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            const tabId = this.dataset.tab;
            const tabContent = document.querySelector(`.tab-content[data-tab="${tabId}"]`);
            
            if (tabContent) {
                // Скрываем все табы
                document.querySelectorAll('.tab.active').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content.active').forEach(c => c.classList.remove('active'));
                
                // Показываем выбранный таб
                this.classList.add('active');
                tabContent.classList.add('active');
            }
        });
    });
}

// Инициализация модальных окон
function initModals() {
    const modals = document.querySelectorAll('.modal');
    
    modals.forEach(modal => {
        // Кнопки закрытия
        const closeBtns = modal.querySelectorAll('.modal-close, .btn-close, [data-dismiss="modal"]');
        closeBtns.forEach(btn => {
            btn.addEventListener('click', function() {
                modal.style.display = 'none';
                modal.classList.remove('show');
            });
        });
        
        // Закрытие при клике на фон
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
                modal.classList.remove('show');
            }
        });
        
        // Закрытие по ESC
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.style.display === 'block') {
                modal.style.display = 'none';
                modal.classList.remove('show');
            }
        });
    });
}

// Инициализация горячих клавиш
function initHotkeys() {
    document.addEventListener('keydown', function(event) {
        // Ctrl+S / Cmd+S - сохранить
        if ((event.ctrlKey || event.metaKey) && event.key === 's') {
            event.preventDefault();
            const saveBtn = document.querySelector('.btn-save, .btn-primary[type="submit"]');
            if (saveBtn) saveBtn.click();
        }
        
        // Ctrl+F - поиск
        if ((event.ctrlKey || event.metaKey) && event.key === 'f') {
            event.preventDefault();
            const searchInput = document.querySelector('input[type="search"], .search-input');
            if (searchInput) searchInput.focus();
        }
        
        // Esc - закрыть модальные окна, меню
        if (event.key === 'Escape') {
            document.querySelectorAll('.modal[style*="display: block"]').forEach(modal => {
                modal.style.display = 'none';
                modal.classList.remove('show');
            });
            
            document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
                menu.classList.remove('show');
            });
            
            // Закрытие меню быстрого скачивания договоров
            const quickMenu = document.getElementById('quickDownloadMenu');
            if (quickMenu && quickMenu.style.display === 'block') {
                quickMenu.style.display = 'none';
            }
        }
        
        // F5 - обновить таблицу
        if (event.key === 'F5') {
            event.preventDefault();
            const refreshBtn = document.querySelector('.btn-refresh, [data-action="refresh"]');
            if (refreshBtn) refreshBtn.click();
        }
    });
}

// Инициализация форм
function initForms() {
    const forms = document.querySelectorAll('form:not(.no-auto-init)');
    forms.forEach(form => {
        // Валидация на лету
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        inputs.forEach(input => {
            // Удаляем старые обработчики
            const newInput = input.cloneNode(true);
            input.parentNode.replaceChild(newInput, input);
            
            newInput.addEventListener('blur', function() {
                validateField(this);
            });
            
            newInput.addEventListener('input', function() {
                clearFieldError(this);
            });
            
            newInput.addEventListener('change', function() {
                clearFieldError(this);
            });
        });
        
        // Обработка отправки формы
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                if (window.utils) {
                    window.utils.showNotification('Пожалуйста, исправьте ошибки в форме', 'error');
                }
                
                // Прокрутка к первому полю с ошибкой
                const firstError = this.querySelector('.error');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
        });
    });
}

// Валидация поля
function validateField(field) {
    clearFieldError(field);
    
    if (!field.checkValidity()) {
        showFieldError(field, getValidationMessage(field));
        return false;
    }
    
    // Дополнительная валидация
    if (field.type === 'email' && field.value && window.utils && !window.utils.isValidEmail(field.value)) {
        showFieldError(field, 'Введите корректный email адрес');
        return false;
    }
    
    if (field.type === 'tel' && field.value && window.utils && !window.utils.isValidPhone(field.value)) {
        showFieldError(field, 'Введите корректный номер телефона (11 цифр, начиная с 7,8 или 9)');
        return false;
    }
    
    return true;
}

// Показать ошибку поля
function showFieldError(field, message) {
    field.classList.add('error');
    
    let errorElement = field.nextElementSibling;
    if (!errorElement || !errorElement.classList.contains('error-message')) {
        errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        field.parentNode.insertBefore(errorElement, field.nextSibling);
    }
    
    errorElement.textContent = message;
    errorElement.style.display = 'block';
}

// Очистить ошибку поля
function clearFieldError(field) {
    field.classList.remove('error');
    
    const errorElement = field.nextElementSibling;
    if (errorElement && errorElement.classList.contains('error-message')) {
        errorElement.style.display = 'none';
        errorElement.textContent = '';
    }
}

// Получить сообщение валидации
function getValidationMessage(field) {
    if (field.validity.valueMissing) {
        return 'Это поле обязательно для заполнения';
    }
    
    if (field.validity.typeMismatch) {
        if (field.type === 'email') return 'Введите корректный email';
        if (field.type === 'url') return 'Введите корректный URL';
    }
    
    if (field.validity.tooShort) {
        return `Минимальная длина: ${field.minLength} символов`;
    }
    
    if (field.validity.tooLong) {
        return `Максимальная длина: ${field.maxLength} символов`;
    }
    
    if (field.validity.patternMismatch) {
        return 'Неверный формат';
    }
    
    if (field.validity.rangeUnderflow) {
        return `Минимальное значение: ${field.min}`;
    }
    
    if (field.validity.rangeOverflow) {
        return `Максимальное значение: ${field.max}`;
    }
    
    return 'Неверное значение';
}

// Валидация всей формы
function validateForm(form) {
    let isValid = true;
    const fields = form.querySelectorAll('input[required], select[required], textarea[required]');
    
    fields.forEach(field => {
        if (!validateField(field)) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Обновление данных на странице
async function refreshData(url, containerId, templateFunction) {
    if (!url || !containerId) {
        console.error('URL and containerId are required');
        return null;
    }
    
    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Ошибка загрузки данных');
        
        const data = await response.json();
        const container = document.getElementById(containerId);
        
        if (container && templateFunction && typeof templateFunction === 'function') {
            container.innerHTML = templateFunction(data);
        }
        
        return data;
    } catch (error) {
        console.error('Error refreshing data:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка загрузки данных', 'error');
        }
        return null;
    }
}

// Показать/скрыть загрузчик
function showLoader(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.add('loading');
    }
}

function hideLoader(containerId) {
    const container = document.getElementById(containerId);
    if (container) {
        container.classList.remove('loading');
    }
}

// Экспорт функций
window.main = {
    initDynamicElements,
    initHotkeys,
    initForms,
    initModals,
    validateField,
    validateForm,
    refreshData,
    showLoader,
    hideLoader
};