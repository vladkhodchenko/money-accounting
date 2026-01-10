const deposits = [{
        id: 1,
        name: "Сбербанк вклад",
        name_bank: "Sberbank",
        date_from: "2023-01-15",
        initial_amount: 100000,
        final_amount: 104500,
        term_months: 3,
        interest_rate: 18,
        capitalization_type_id: "Monthly",
        deposit_type_id: "Deposit"
    },
    {
        id: 2,
        name_bank: "VTB",
        date_from: "2023-03-20",
        initial_amount: 200000,
        final_amount: 219000,
        term_months: 6,
        interest_rate: 19,
        capitalization_id: "Monthly",
        deposit_type_id: "Deposit"
    },
    {
        id: 3,
        name: "Alfa-Bank вклад",
        name_bank: "Alfa-Bank",
        date_from: "2023-05-10",
        initial_amount: 10000,
        final_amount: 16666.67,
        term_months: 4,
        interest_rate: 20,
        capitalization_id: "Monthly",
        deposit_type_id: "Deposit"
    },
];

// UI state
let darkMode = false;
let viewMode = 'grid';
let editingDepositId = null;
let calendarMonth = new Date().getMonth();
let calendarYear = new Date().getFullYear();

// DOM elements
const body = document.body;
const darkModeBtn = document.getElementById('dark-mode-btn');
const addDepositBtn = document.getElementById('add-deposit-btn');
const depositModal = document.getElementById('deposit-modal');
const closeModalBtn = document.getElementById('close-modal-btn');
const depositForm = document.getElementById('deposit-form');
const modalTitle = document.getElementById('modal-title');
const depositIdInput = document.getElementById('deposit-id');
const depositNameInput = document.getElementById('deposit-name');
const bankNameInput = document.getElementById('bank-name');
const startDateInput = document.getElementById('start-date');
const initialAmountInput = document.getElementById('initial-amount');
const termMonthsInput = document.getElementById('term-months');
const interestRateInput = document.getElementById('interest-rate');
const finalAmountInput = document.getElementById('final-amount');
const depositsContainer = document.getElementById('deposits-container');
const gridViewBtn = document.getElementById('grid-view-btn');
const listViewBtn = document.getElementById('list-view-btn');
const calendarBtn = document.getElementById('calendar-btn');
const viewCalendarBtn = document.getElementById('view-calendar-btn');
const calendarModal = document.getElementById('calendar-modal');
const closeCalendarBtn = document.getElementById('close-calendar-btn');
const prevMonthBtn = document.getElementById('prev-month-btn');
const nextMonthBtn = document.getElementById('next-month-btn');
const calendarMonthYear = document.getElementById('calendar-month-year');
const calendarGrid = document.getElementById('calendar-grid');
const totalDepositsEl = document.getElementById('total-deposits');
const totalFinalAmountEl = document.getElementById('total-final-amount');
const totalEarningsEl = document.getElementById('total-earnings');
const saveDepositBtn = document.getElementById("save-deposit")

// Helper functions
function calculateFinalAmount(initial, rate, months) {
    const monthlyRate = rate / 100 / 12;
    return initial * Math.pow(1 + monthlyRate, months);
}

function calculateEndDate(date_from, months) {
    const date = new Date(date_from);
    date.setMonth(date.getMonth() + parseInt(months));
    return date.toISOString().split('T')[0];
}

function formatDate(dateStr) {
    const date = new Date(dateStr);
    return date.toLocaleDateString();
}

function formatCurrency(amount) {
    return '₽' + amount.toLocaleString();
}

function updateSummary() {
    const totalDeposits = deposits.reduce((sum, d) => sum + d.initial_amount, 0);
    const totalFinalAmount = deposits.reduce((sum, d) => sum + d.final_amount, 0);
    const totalEarnings = totalFinalAmount - totalDeposits;

    totalDepositsEl.textContent = formatCurrency(totalDeposits);
    totalFinalAmountEl.textContent = formatCurrency(totalFinalAmount);
    totalEarningsEl.textContent = formatCurrency(totalEarnings);
}

async function saveDeposit() {
    const url = "http://127.0.0.1:8000/deposits";

    const form = document.getElementById("deposit-form")
    const formData = new FormData(form);
    console.log(JSON.stringify(formData))

    const data = {};

    formData.forEach((value, key) => {
        data[key] = value;
        console.log(key, value)
    });

    console.log(data)

    const response = await fetch(url, {
        method: "POST",
        body: JSON.stringify({
            userId: 1,
            title: "Fix my bugs",
            completed: false
        }),
        headers: {
            "Content-type": "application/json; charset=UTF-8"
        }
    });
}

async function renderDeposits() {

    const url = "http://127.0.0.1:8000/deposits";
    const response = await fetch(url, {

        mode: 'cors', // Явно указываем режим CORS
        headers: {
            'Content-Type': 'application/json',
            // Добавьте другие заголовки, если требуется сервером
        }
    });

    const data = await response.json();

    depositsContainer.innerHTML = '';

    if (deposits.length === 0) {
        depositsContainer.innerHTML = `
                    <div class="col-span-full bg-white rounded-xl shadow-md p-8 text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-gray-400 mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
                        </svg>
                        <h3 class="text-xl font-semibold text-gray-700 mb-2">No deposits found</h3>
                        <p class="text-gray-500 mb-4">Get started by adding your first deposit</p>
                        <button id="empty-add-deposit-btn" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition duration-300">
                            Add Deposit
                        </button>
                    </div>
                `;

        document.getElementById('empty-add-deposit-btn').addEventListener('click', openDepositModal);
        return;
    }

    deposits.forEach(deposit => {
        const endDate = calculateEndDate(deposit.date_from, deposit.term_months);

        const depositCard = document.createElement('div');
        depositCard.className = `deposit-card bg-white hover:shadow-lg rounded-xl shadow-md transition duration-300 overflow-hidden border ${darkMode ? 'border-gray-700' : 'border-gray-100'}`;
        depositCard.innerHTML = `
                    <div class="p-6">
                        <div class="flex justify-between items-start">
                            <h2 class="text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}">${deposit.name}</h2>
                            <span class="px-2 py-1 text-xs font-medium rounded-full ${darkMode ? 'bg-indigo-900 text-indigo-200' : 'bg-indigo-100 text-indigo-800'}">
                                ${deposit.term_months} months
                            </span>
                        </div>
                        
                        <div class="mt-4 space-y-2">
                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">Bank:</span>
                                <span class="font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}">
                                    ${deposit.name_bank}
                                </span>
                            </div>
                            
                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">Start Date:</span>
                                <span class="font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}">
                                    ${formatDate(deposit.date_from)}
                                </span>
                            </div>
                            
                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">End Date:</span>
                                <span class="font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}">
                                    ${formatDate(endDate)}
                                </span>
                            </div>
                            
                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">Initial Amount:</span>
                                <span class="font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}">
                                    ${formatCurrency(deposit.initial_amount)}
                                </span>
                            </div>
                            
                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">Final Amount:</span>
                                <span class="font-medium text-green-600">
                                    ${formatCurrency(deposit.final_amount)}
                                </span>
                            </div>
                            
                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">Interest Rate:</span>
                                <span class="font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}">
                                    ${deposit.interest_rate}%
                                </span>
                            </div>
                            

                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">Deposit type</span>
                                <span class="font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}">
                                    ${deposit.deposit_type_id}
                                </span>
                            </div>

                            <div class="flex justify-between">
                                <span class="${darkMode ? 'text-gray-400' : 'text-gray-500'}">Capitalization type</span>
                                <span class="font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}">
                                    ${deposit.capitalization_id}
                                </span>
                            </div>
                            
                        
                        </div>
                        
                        <div class="mt-6 flex justify-end space-x-2">
                            <button class="edit-btn ${darkMode ? 'text-blue-400 hover:bg-gray-700' : 'text-blue-600 hover:bg-blue-50'} p-2 rounded-full transition duration-200" data-id="${deposit.id}">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                </svg>
                            </button>
                            <button class="delete-btn ${darkMode ? 'text-red-400 hover:bg-gray-700' : 'text-red-600 hover:bg-red-50'} p-2 rounded-full transition duration-200" data-id="${deposit.id}">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 001 1v-8z" clip-rule="evenodd" />
                                </svg>
                            </button>
                        </div>
                    </div>
                `;

        depositsContainer.appendChild(depositCard);
    });

    // Add event listeners to edit and delete buttons
    document.querySelectorAll('.edit-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(btn.dataset.id);
            editDeposit(id);
        });
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const id = parseInt(btn.dataset.id);
            deleteDeposit(id);
        });
    });
}

function generateCalendarDays() {
    const firstDay = new Date(calendarYear, calendarMonth, 1);
    const lastDay = new Date(calendarYear, calendarMonth + 1, 0);
    const prevMonthDays = new Date(calendarYear, calendarMonth, 0).getDate();
    const calendarDays = [];

    const firstDayOfWeek = firstDay.getDay();
    for (let i = firstDayOfWeek - 1; i >= 0; i--) {
        calendarDays.push({
            date: new Date(calendarYear, calendarMonth - 1, prevMonthDays - i),
            isCurrentMonth: false
        });
    }

    for (let i = 1; i <= lastDay.getDate(); i++) {
        calendarDays.push({
            date: new Date(calendarYear, calendarMonth, i),
            isCurrentMonth: true
        });
    }

    const remainingDays = 42 - calendarDays.length;
    for (let i = 1; i <= remainingDays; i++) {
        calendarDays.push({
            date: new Date(calendarYear, calendarMonth + 1, i),
            isCurrentMonth: false
        });
    }

    return calendarDays;
}

function getDepositMarkers(date) {
    const dateString = date.toISOString().split('T')[0];
    const markers = {
        start: false,
        end: false
    };

    deposits.forEach(deposit => {
        if (deposit.date_from === dateString) {
            markers.start = true;
        }

        if (calculateEndDate(deposit.date_from, deposit.term_months) === dateString) {
            markers.end = true;
        }
    });

    return markers;
}

function renderCalendar() {
    const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    calendarMonthYear.textContent = `${monthNames[calendarMonth]} ${calendarYear}`;

    const calendarDays = generateCalendarDays();
    calendarGrid.innerHTML = '';

    calendarDays.forEach(day => {
        const {
            start,
            end
        } = getDepositMarkers(day.date);
        const dayElement = document.createElement('div');
        dayElement.className = `calendar-day ${
                    day.isCurrentMonth
                        ? darkMode ? 'text-white' : 'text-gray-900'
                        : darkMode ? 'text-gray-500' : 'text-gray-400'
                } ${
                    start || end ? 'font-bold' : ''
                } ${
                    day.isCurrentMonth
                        ? (darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100')
                        : ''
                }`;

        dayElement.innerHTML = `
                    <div class="relative">
                        ${start ? '<div class="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full"></div>' : ''}
                        ${end ? '<div class="absolute -bottom-1 -left-1 w-3 h-3 bg-green-500 rounded-full"></div>' : ''}
                        <span class="relative z-10">${day.date.getDate()}</span>
                    </div>
                `;

        calendarGrid.appendChild(dayElement);
    });
}

// Modal functions
function openDepositModal() {
    depositModal.style.display = 'flex';
}

function closeDepositModal() {
    depositModal.style.display = 'none';
    resetForm();
}

function openCalendarModal() {
    renderCalendar();
    calendarModal.style.display = 'flex';
}

function closeCalendarModal() {
    calendarModal.style.display = 'none';
}

function resetForm() {
    depositForm.reset();
    depositIdInput.value = '';
    modalTitle.textContent = 'Add New Deposit';
    editingDepositId = null;
}

function editDeposit(id) {
    const deposit = deposits.find(d => d.id === id);
    if (!deposit) return;

    editingDepositId = id;
    depositIdInput.value = deposit.id;
    depositNameInput.value = deposit.name;
    bankNameInput.value = deposit.name_bank;
    startDateInput.value = deposit.date_from;
    initialAmountInput.value = deposit.initial_amount;
    termMonthsInput.value = deposit.term_months;
    interestRateInput.value = deposit.interest_rate;
    finalAmountInput.value = deposit.final_amount;

    modalTitle.textContent = 'Edit Deposit';
    openDepositModal();
}

function deleteDeposit(id) {
    if (confirm('Are you sure you want to delete this deposit?')) {
        const index = deposits.findIndex(d => d.id === id);
        if (index !== -1) {
            deposits.splice(index, 1);
            renderDeposits();
            updateSummary();
        }
    }
}

function calculateFinalAmountFromForm() {
    if (initialAmountInput.value && interestRateInput.value && termMonthsInput.value) {
        const final_amount = calculateFinalAmount(
            parseFloat(initialAmountInput.value),
            parseFloat(interestRateInput.value),
            parseInt(termMonthsInput.value)
        ).toFixed(2);
        finalAmountInput.value = final_amount;
    }
}

// Event listeners
darkModeBtn.addEventListener('click', () => {
    darkMode = !darkMode;
    if (darkMode) {
        body.classList.add('dark');
        body.classList.remove('bg-gray-50', 'text-gray-900');
        body.classList.add('bg-gray-900', 'text-white');
        darkModeBtn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                    </svg>
                `;
    } else {
        body.classList.remove('dark');
        body.classList.remove('bg-gray-900', 'text-white');
        body.classList.add('bg-gray-50', 'text-gray-900');
        darkModeBtn.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                    </svg>
                `;
    }
    renderDeposits();
});

addDepositBtn.addEventListener('click', openDepositModal);
closeModalBtn.addEventListener('click', closeDepositModal);
saveDepositBtn.addEventListener('click', saveDeposit)

depositForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const depositData = {
        id: editingDepositId || Date.now(),
        name: depositNameInput.value,
        name_bank: bankNameInput.value,
        date_from: startDateInput.value,
        initial_amount: parseFloat(initialAmountInput.value),
        term_months: parseInt(termMonthsInput.value),
        interest_rate: parseFloat(interestRateInput.value),
        final_amount: parseFloat(finalAmountInput.value)
    };

    if (editingDepositId) {
        const index = deposits.findIndex(d => d.id === editingDepositId);
        if (index !== -1) {
            deposits[index] = depositData;
        }
    } else {
        deposits.push(depositData);
    }

    renderDeposits();
    updateSummary();
    closeDepositModal();
});

initialAmountInput.addEventListener('input', calculateFinalAmountFromForm);
interestRateInput.addEventListener('input', calculateFinalAmountFromForm);
termMonthsInput.addEventListener('input', calculateFinalAmountFromForm);

gridViewBtn.addEventListener('click', () => {
    viewMode = 'grid';
    gridViewBtn.classList.remove('text-gray-700', 'hover:bg-gray-100');
    gridViewBtn.classList.add('bg-indigo-600', 'text-white');
    listViewBtn.classList.remove('bg-indigo-600', 'text-white');
    listViewBtn.classList.add('text-gray-700', 'hover:bg-gray-100');
    depositsContainer.className = 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6';
});

listViewBtn.addEventListener('click', () => {
    viewMode = 'list';
    listViewBtn.classList.remove('text-gray-700', 'hover:bg-gray-100');
    listViewBtn.classList.add('bg-indigo-600', 'text-white');
    gridViewBtn.classList.remove('bg-indigo-600', 'text-white');
    gridViewBtn.classList.add('text-gray-700', 'hover:bg-gray-100');
    depositsContainer.className = 'grid grid-cols-1 gap-6';
});

calendarBtn.addEventListener('click', openCalendarModal);
viewCalendarBtn.addEventListener('click', openCalendarModal);
closeCalendarBtn.addEventListener('click', closeCalendarModal);

prevMonthBtn.addEventListener('click', () => {
    if (calendarMonth === 0) {
        calendarMonth = 11;
        calendarYear--;
    } else {
        calendarMonth--;
    }
    renderCalendar();
});

nextMonthBtn.addEventListener('click', () => {
    if (calendarMonth === 11) {
        calendarMonth = 0;
        calendarYear++;
    } else {
        calendarMonth++;
    }
    renderCalendar();
});

// Initialize
updateSummary();
renderDeposits();