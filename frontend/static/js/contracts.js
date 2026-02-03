// Инициализация страницы договоров
document.addEventListener('DOMContentLoaded', function() {
    initContractsPage();
});

function initContractsPage() {
    // Загрузка договоров для страницы списка
    if (document.getElementById('contractsTable')) {
        loadContracts();
        initTableActions();
    }
    
    // Инициализация страницы деталей договора
    if (document.getElementById('contractDetail')) {
        initContractDetailPage();
    }
    
    // Инициализация формы генерации документов
    if (document.getElementById('contractForm')) {
        initDocumentGenerator();
    }
}

// Загрузка списка договоров
async function loadContracts() {
    try {
        const response = await fetch('/api/v1/contracts/?limit=100');
        if (!response.ok) throw new Error('Ошибка загрузки договоров');
        
        const contracts = await response.json();
        renderContractsTable(contracts);
        
    } catch (error) {
        console.error('Error loading contracts:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка загрузки договоров', 'error');
        }
    }
}

// Рендеринг таблицы договоров
function renderContractsTable(contracts) {
    const tbody = document.querySelector('#contractsTable tbody');
    if (!tbody) return;
    
    tbody.innerHTML = '';
    
    contracts.forEach(contract => {
        const row = document.createElement('tr');
        row.dataset.contractId = contract.id;
        
        const statusClass = `status-${contract.status}`;
        const date = contract.date ? new Date(contract.date).toLocaleDateString('ru-RU') : '-';
        const amount = contract.total_amount ? contract.total_amount.toFixed(2) : '0.00';
        
        row.innerHTML = `
            <td>
                <input type="checkbox" class="contract-checkbox" value="${contract.id}" 
                       onchange="updateDownloadButton()">
            </td>
            <td>${contract.id}</td>
            <td>${contract.client?.full_name || 'Неизвестно'}</td>
            <td>
                ${contract.car ? `${contract.car.brand} ${contract.car.model} (${contract.car.year})` : 'Не указан'}
            </td>
            <td>${date}</td>
            <td>${amount} ₽</td>
            <td>
                <span class="status-badge ${statusClass}">
                    ${contract.status}
                </span>
            </td>
            <td>
                <div class="action-buttons">
                    <a href="/contracts/${contract.id}" class="btn-small btn-view" title="Просмотр">
                        👁️
                    </a>
                    <button onclick="downloadContract('docx', ${contract.id})" 
                            class="btn-small btn-docx" title="Скачать DOCX">
                        📄
                    </button>
                    <button onclick="downloadContract('pdf', ${contract.id})" 
                            class="btn-small btn-pdf" title="Скачать PDF">
                        📊
                    </button>
                    <button onclick="showQuickDownloadMenu(${contract.id})" 
                            class="btn-small btn-more" title="Быстрое скачивание">
                        ⬇️
                    </button>
                </div>
            </td>
        `;
        
        tbody.appendChild(row);
    });
}

// Инициализация действий в таблице
function initTableActions() {
    // Обработчик для чекбокса "Выбрать все"
    const selectAll = document.getElementById('selectAll');
    if (selectAll) {
        selectAll.addEventListener('change', function() {
            const checkboxes = document.querySelectorAll('.contract-checkbox');
            checkboxes.forEach(cb => {
                cb.checked = this.checked;
            });
            updateDownloadButton();
        });
    }
    
    // Обработчик кликов вне меню быстрого скачивания
    document.addEventListener('click', function(event) {
        const menu = document.getElementById('quickDownloadMenu');
        const menuBtn = event.target.closest('.btn-more');
        
        if (menu && menu.style.display === 'block' && !menu.contains(event.target) && !menuBtn) {
            closeQuickDownloadMenu();
        }
    });
}

// Обновление кнопки скачивания
function updateDownloadButton() {
    const checkboxes = document.querySelectorAll('.contract-checkbox:checked');
    const downloadBtn = document.getElementById('downloadSelectedBtn');
    const selectAllCheckbox = document.getElementById('selectAll');
    
    if (downloadBtn) {
        downloadBtn.disabled = checkboxes.length === 0;
    }
    
    if (selectAllCheckbox) {
        const allCheckboxes = document.querySelectorAll('.contract-checkbox');
        selectAllCheckbox.checked = checkboxes.length === allCheckboxes.length;
        selectAllCheckbox.indeterminate = checkboxes.length > 0 && checkboxes.length < allCheckboxes.length;
    }
}

// Скачивание договора
function downloadContract(format, contractId) {
    const url = `/api/v1/contract-documents/contract/${contractId}/download/${format}`;
    
    if (window.utils) {
        window.utils.showNotification(`Скачиваем договор №${contractId}...`, 'info');
        window.utils.downloadFile(url);
        
        setTimeout(() => {
            window.utils.showNotification('Договор успешно скачан!', 'success');
        }, 1000);
    }
}

// Меню быстрого скачивания
let selectedContractId = null;

function showQuickDownloadMenu(contractId, event) {
    selectedContractId = contractId;
    const menu = document.getElementById('quickDownloadMenu');
    
    if (!menu) return;
    
    menu.style.display = 'block';
    
    // Позиционирование
    const btn = event?.target?.closest('button') || event;
    if (btn) {
        const rect = btn.getBoundingClientRect();
        menu.style.top = `${rect.bottom + window.scrollY}px`;
        menu.style.left = `${rect.left + window.scrollX}px`;
    }
}

function closeQuickDownloadMenu() {
    const menu = document.getElementById('quickDownloadMenu');
    if (menu) {
        menu.style.display = 'none';
    }
    selectedContractId = null;
}

function downloadSelectedFormat(format) {
    if (selectedContractId) {
        downloadContract(format, selectedContractId);
        closeQuickDownloadMenu();
    }
}

// Массовое скачивание
async function downloadSelectedContracts() {
    const checkboxes = document.querySelectorAll('.contract-checkbox:checked');
    if (checkboxes.length === 0) return;
    
    const contractIds = Array.from(checkboxes).map(cb => cb.value);
    
    try {
        if (window.utils) {
            window.utils.showNotification(`Подготовка ${contractIds.length} договоров...`, 'info');
        }
        
        const response = await fetch('/api/v1/contract-documents/download-multiple', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contract_ids: contractIds,
                format: 'pdf'
            })
        });
        
        if (!response.ok) throw new Error('Ошибка создания архива');
        
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        
        if (window.utils) {
            window.utils.downloadFile(url, `contracts_${new Date().toISOString().slice(0, 10)}.zip`);
            window.utils.showNotification(`Архив с ${contractIds.length} договорами скачан!`, 'success');
        }
        
    } catch (error) {
        console.error('Error downloading multiple contracts:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка при создании архива', 'error');
        }
    }
}

async function downloadAllContracts() {
    try {
        const response = await fetch('/api/v1/contracts/');
        if (!response.ok) throw new Error('Ошибка загрузки договоров');
        
        const contracts = await response.json();
        
        if (contracts.length === 0) {
            if (window.utils) {
                window.utils.showNotification('Нет договоров для скачивания', 'warning');
            }
            return;
        }
        
        const contractIds = contracts.map(c => c.id);
        
        if (window.utils) {
            window.utils.showNotification(`Подготовка всех договоров (${contracts.length})...`, 'info');
        }
        
        const downloadResponse = await fetch('/api/v1/contract-documents/download-multiple', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                contract_ids: contractIds,
                format: 'pdf'
            })
        });
        
        if (!downloadResponse.ok) throw new Error('Ошибка создания архива');
        
        const blob = await downloadResponse.blob();
        const url = window.URL.createObjectURL(blob);
        
        if (window.utils) {
            window.utils.downloadFile(url, `all_contracts_${new Date().toISOString().slice(0, 10)}.zip`);
            window.utils.showNotification(`Все договоры (${contracts.length}) скачаны!`, 'success');
        }
        
    } catch (error) {
        console.error('Error downloading all contracts:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка при создании архива', 'error');
        }
    }
}

// Страница деталей договора
function initContractDetailPage() {
    // Инициализация кнопок скачивания на странице деталей
    const downloadButtons = document.querySelectorAll('[onclick*="downloadContract"]');
    downloadButtons.forEach(btn => {
        const match = btn.getAttribute('onclick').match(/downloadContract\('(\w+)',\s*(\d+)\)/);
        if (match) {
            const [_, format, contractId] = match;
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                downloadContract(format, contractId);
            });
        }
    });
}

// Форма генерации документов
function initDocumentGenerator() {
    const contractSelect = document.getElementById('contractSelect');
    if (contractSelect) {
        loadContractsForSelect();
        
        contractSelect.addEventListener('change', function() {
            if (this.value) {
                loadContractDetails(this.value);
            } else {
                hideContractDetails();
            }
        });
    }
}

async function loadContractsForSelect() {
    try {
        const response = await fetch('/api/v1/contracts/');
        if (!response.ok) throw new Error('Ошибка загрузки договоров');
        
        const contracts = await response.json();
        const select = document.getElementById('contractSelect');
        
        select.innerHTML = '<option value="">-- Выберите договор --</option>';
        
        contracts.forEach(contract => {
            const option = document.createElement('option');
            option.value = contract.id;
            option.textContent = `Договор №${contract.id} от ${contract.date ? new Date(contract.date).toLocaleDateString('ru-RU') : '-'}`;
            select.appendChild(option);
        });
        
    } catch (error) {
        console.error('Error loading contracts for select:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка загрузки договоров', 'error');
        }
    }
}

async function loadContractDetails(contractId) {
    try {
        const response = await fetch(`/api/v1/contracts/${contractId}`);
        if (!response.ok) throw new Error('Ошибка загрузки деталей договора');
        
        const contract = await response.json();
        displayContractDetails(contract);
        
    } catch (error) {
        console.error('Error loading contract details:', error);
        if (window.utils) {
            window.utils.showNotification('Ошибка загрузки деталей договора', 'error');
        }
    }
}

function displayContractDetails(contract) {
    const container = document.getElementById('contractDetails');
    if (!container) return;
    
    // Здесь можно добавить рендеринг деталей договора
    container.style.display = 'block';
}

function hideContractDetails() {
    const container = document.getElementById('contractDetails');
    if (container) {
        container.style.display = 'none';
    }
}

// Экспорт функций
window.contracts = {
    loadContracts,
    downloadContract,
    downloadSelectedContracts,
    downloadAllContracts,
    showQuickDownloadMenu,
    closeQuickDownloadMenu,
    downloadSelectedFormat
};