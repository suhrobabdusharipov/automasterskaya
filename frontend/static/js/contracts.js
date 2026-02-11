document.addEventListener('DOMContentLoaded', function() {
    // Подстановка сегодняшней даты
    const dateInput = document.querySelector('input[name="date"]');
    if (dateInput && !dateInput.value) {
        const today = new Date().toISOString().split('T')[0];
        dateInput.value = today;
    }
    
    // Динамическая загрузка автомобилей клиента
    const clientSelect = document.getElementById('clientSelect');
    const carSelect = document.getElementById('carSelect');
    
    if (clientSelect && carSelect) {
        clientSelect.addEventListener('change', function() {
            const clientId = this.value;
            if (!clientId) {
                carSelect.innerHTML = '<option value="">-- Сначала выберите клиента --</option>';
                carSelect.disabled = true;
                return;
            }
            
            // Загружаем автомобили клиента
            fetch(`/api/clients/${clientId}/cars`)
                .then(response => response.json())
                .then(cars => {
                    carSelect.innerHTML = '<option value="">-- Выберите автомобиль --</option>';
                    
                    if (cars.length === 0) {
                        carSelect.innerHTML += '<option value="">У клиента нет автомобилей</option>';
                    } else {
                        cars.forEach(car => {
                            const option = document.createElement('option');
                            option.value = car.id;
                            option.textContent = `${car.brand} ${car.model} (${car.year}) - ${car.vin}`;
                            carSelect.appendChild(option);
                        });
                    }
                    
                    carSelect.disabled = false;
                })
                .catch(error => {
                    console.error('Ошибка загрузки автомобилей:', error);
                    carSelect.innerHTML = '<option value="">Ошибка загрузки</option>';
                });
        });
    }
});