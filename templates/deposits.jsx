import React, { useState, useEffect } from 'react';

const App = () => {
  // Mock data for deposits with separate deposit name and bank name
  const [deposits, setDeposits] = useState([
    {
      id: 1,
      depositName: "Sberbank Deposit",
      bankName: "Sberbank",
      startDate: "2023-01-15",
      initialAmount: 100000,
      finalAmount: 105000,
      termMonths: 12,
      interestRate: 5.0
    },
    {
      id: 2,
      depositName: "VTB Premium Deposit",
      bankName: "VTB",
      startDate: "2023-03-20",
      initialAmount: 250000,
      finalAmount: 268750,
      termMonths: 18,
      interestRate: 4.5
    },
    {
      id: 3,
      depositName: "Alfa-Bank Classic",
      bankName: "Alfa-Bank",
      startDate: "2023-05-10",
      initialAmount: 50000,
      finalAmount: 52500,
      termMonths: 6,
      interestRate: 5.0
    }
  ]);

  // UI states
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingDeposit, setEditingDeposit] = useState(null);
  const [formData, setFormData] = useState({
    depositName: "",
    bankName: "",
    startDate: "",
    initialAmount: "",
    termMonths: "",
    interestRate: ""
  });
  const [viewMode, setViewMode] = useState('grid');
  const [darkMode, setDarkMode] = useState(false);
  const [showCalendar, setShowCalendar] = useState(false);
  const [calendarMonth, setCalendarMonth] = useState(new Date().getMonth());
  const [calendarYear, setCalendarYear] = useState(new Date().getFullYear());

  // Calculate final amount with compound interest
  const calculateFinalAmount = (initial, rate, months) => {
    const monthlyRate = rate / 100 / 12;
    return initial * Math.pow(1 + monthlyRate, months);
  };

  // Calculate end date
  const calculateEndDate = (startDate, months) => {
    const date = new Date(startDate);
    date.setMonth(date.getMonth() + parseInt(months));
    return date.toISOString().split('T')[0];
  };

  // Generate calendar days
  const generateCalendarDays = () => {
    const firstDay = new Date(calendarYear, calendarMonth, 1);
    const lastDay = new Date(calendarYear, calendarMonth + 1, 0);
    
    // Get the number of days in the previous month
    const prevMonthDays = new Date(calendarYear, calendarMonth, 0).getDate();
    
    // Create array of all days in the calendar grid
    const calendarDays = [];
    
    // Add days from previous month
    const firstDayOfWeek = firstDay.getDay();
    for (let i = firstDayOfWeek - 1; i >= 0; i--) {
      calendarDays.push({
        date: new Date(calendarYear, calendarMonth - 1, prevMonthDays - i),
        isCurrentMonth: false
      });
    }
    
    // Add days from current month
    for (let i = 1; i <= lastDay.getDate(); i++) {
      calendarDays.push({
        date: new Date(calendarYear, calendarMonth, i),
        isCurrentMonth: true
      });
    }
    
    // Add days from next month
    const remainingDays = 42 - calendarDays.length; // 42 days in a 6x7 calendar grid
    for (let i = 1; i <= remainingDays; i++) {
      calendarDays.push({
        date: new Date(calendarYear, calendarMonth + 1, i),
        isCurrentMonth: false
      });
    }
    
    return calendarDays;
  };

  // Check if a date is a start date or end date of any deposit
  const getDepositMarkers = (date) => {
    const dateString = date.toISOString().split('T')[0];
    const markers = {
      start: false,
      end: false
    };
    
    deposits.forEach(deposit => {
      if (deposit.startDate === dateString) {
        markers.start = true;
      }
      
      if (calculateEndDate(deposit.startDate, deposit.termMonths) === dateString) {
        markers.end = true;
      }
    });
    
    return markers;
  };

  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => {
      const updated = { ...prev, [name]: value };
      
      if (updated.initialAmount && updated.interestRate && updated.termMonths) {
        updated.finalAmount = calculateFinalAmount(
          parseFloat(updated.initialAmount),
          parseFloat(updated.interestRate),
          parseInt(updated.termMonths)
        ).toFixed(2);
      }
      
      return updated;
    });
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    
    const newDeposit = {
      ...formData,
      id: editingDeposit ? editingDeposit.id : Date.now(),
      initialAmount: parseFloat(formData.initialAmount),
      finalAmount: parseFloat(formData.finalAmount),
      termMonths: parseInt(formData.termMonths),
      interestRate: parseFloat(formData.interestRate)
    };
    
    if (editingDeposit) {
      setDeposits(deposits.map(d => d.id === editingDeposit.id ? newDeposit : d));
    } else {
      setDeposits([...deposits, newDeposit]);
    }
    
    setIsModalOpen(false);
    setEditingDeposit(null);
    setFormData({
      depositName: "",
      bankName: "",
      startDate: "",
      initialAmount: "",
      termMonths: "",
      interestRate: ""
    });
  };

  // Open edit modal
  const handleEdit = (deposit) => {
    setEditingDeposit(deposit);
    setFormData({
      depositName: deposit.depositName,
      bankName: deposit.bankName,
      startDate: deposit.startDate,
      initialAmount: deposit.initialAmount.toString(),
      termMonths: deposit.termMonths.toString(),
      interestRate: deposit.interestRate.toString()
    });
    setIsModalOpen(true);
  };

  // Delete deposit
  const handleDelete = (id) => {
    setDeposits(deposits.filter(d => d.id !== id));
  };

  // Calculate summary statistics
  const totalDeposits = deposits.reduce((sum, d) => sum + d.initialAmount, 0);
  const totalFinalAmount = deposits.reduce((sum, d) => sum + d.finalAmount, 0);
  const totalEarnings = totalFinalAmount - totalDeposits;

  // Navigate calendar
  const goToPreviousMonth = () => {
    if (calendarMonth === 0) {
      setCalendarMonth(11);
      setCalendarYear(calendarYear - 1);
    } else {
      setCalendarMonth(calendarMonth - 1);
    }
  };

  const goToNextMonth = () => {
    if (calendarMonth === 11) {
      setCalendarMonth(0);
      setCalendarYear(calendarYear + 1);
    } else {
      setCalendarMonth(calendarMonth + 1);
    }
  };

  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900 text-white' : 'bg-gray-50 text-gray-900'} transition-colors duration-300`}>
      {/* Header */}
      <header className={`${darkMode ? 'bg-gray-800' : 'bg-gradient-to-r from-blue-600 to-indigo-700'} text-white shadow-lg`}>
        <div className="container mx-auto px-4 py-6">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold">Bank Deposit Tracker</h1>
            <div className="flex space-x-4">
              <button 
                onClick={() => setShowCalendar(true)}
                className="p-2 rounded-full hover:bg-gray-700 transition duration-300"
                aria-label="Show calendar"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
              </button>
              <button 
                onClick={() => setDarkMode(!darkMode)}
                className="p-2 rounded-full hover:bg-gray-700 transition duration-300"
                aria-label="Toggle dark mode"
              >
                {darkMode ? (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z" />
                  </svg>
                )}
              </button>
              <button 
                onClick={() => setIsModalOpen(true)}
                className="bg-white text-indigo-700 hover:bg-indigo-50 px-4 py-2 rounded-lg font-medium transition duration-300 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
                Add Deposit
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Summary Section */}
      <section className={`${darkMode ? 'bg-gray-800' : 'bg-gradient-to-r from-blue-50 to-indigo-50'} py-8`}>
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} p-6 rounded-xl shadow-md`}>
              <div className="flex items-center">
                <div className={`p-3 rounded-full ${darkMode ? 'bg-blue-900 text-blue-300' : 'bg-blue-100 text-blue-600'} mr-4`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-500'}`}>Total Deposits</p>
                  <p className="text-2xl font-bold">₽{totalDeposits.toLocaleString()}</p>
                </div>
              </div>
            </div>
            
            <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} p-6 rounded-xl shadow-md`}>
              <div className="flex items-center">
                <div className={`p-3 rounded-full ${darkMode ? 'bg-green-900 text-green-300' : 'bg-green-100 text-green-600'} mr-4`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-500'}`}>Total Value</p>
                  <p className="text-2xl font-bold">₽{totalFinalAmount.toLocaleString()}</p>
                </div>
              </div>
            </div>
            
            <div className={`${darkMode ? 'bg-gray-700' : 'bg-white'} p-6 rounded-xl shadow-md`}>
              <div className="flex items-center">
                <div className={`p-3 rounded-full ${darkMode ? 'bg-purple-900 text-purple-300' : 'bg-purple-100 text-purple-600'} mr-4`}>
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <p className={`text-sm ${darkMode ? 'text-gray-300' : 'text-gray-500'}`}>Total Earnings</p>
                  <p className={`text-2xl font-bold ${totalEarnings > 0 ? 'text-green-600' : 'text-red-600'}`}>
                    ₽{totalEarnings.toLocaleString()}
                  </p>
                </div>
              </div>
              <div className={`mt-4 ${darkMode ? 'bg-gray-600' : 'bg-gray-50'} p-3 rounded-lg max-h-40 overflow-y-auto`}>
                <h4 className={`text-sm font-semibold mb-2 ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>Breakdown:</h4>
                {deposits.map(deposit => (
                  <div key={deposit.id} className="flex justify-between text-sm">
                    <span>{deposit.depositName}:</span>
                    <span>₽{(deposit.finalAmount).toLocaleString()}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* View Toggle and Calendar Button */}
      <div className="container mx-auto px-4 py-4 flex justify-end">
        <div className="flex space-x-4">
          <div className={`inline-flex rounded-md shadow-sm ${darkMode ? 'bg-gray-700' : 'bg-white'}`}>
            <button
              type="button"
              onClick={() => setViewMode('grid')}
              className={`px-4 py-2 text-sm font-medium rounded-l-md ${
                viewMode === 'grid' 
                  ? (darkMode ? 'bg-indigo-600 text-white' : 'bg-indigo-600 text-white')
                  : (darkMode ? 'text-gray-300 hover:bg-gray-600' : 'text-gray-700 hover:bg-gray-100')
              }`}
            >
              Grid View
            </button>
            <button
              type="button"
              onClick={() => setViewMode('list')}
              className={`px-4 py-2 text-sm font-medium rounded-r-md ${
                viewMode === 'list' 
                  ? (darkMode ? 'bg-indigo-600 text-white' : 'bg-indigo-600 text-white')
                  : (darkMode ? 'text-gray-300 hover:bg-gray-600' : 'text-gray-700 hover:bg-gray-100')
              }`}
            >
              List View
            </button>
          </div>
          
          <button
            onClick={() => setShowCalendar(true)}
            className={`inline-flex items-center px-4 py-2 rounded-lg font-medium ${
              darkMode 
                ? 'bg-gray-700 text-white hover:bg-gray-600' 
                : 'bg-white text-gray-700 hover:bg-gray-100'
            } shadow-sm transition duration-300`}
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
            </svg>
            View Calendar
          </button>
        </div>
      </div>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className={`grid ${viewMode === 'grid' ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' : 'grid-cols-1'} gap-6`}>
          {deposits.map(deposit => {
            const endDate = calculateEndDate(deposit.startDate, deposit.termMonths);
            
            return (
              <div 
                key={deposit.id} 
                className={`${darkMode ? 'bg-gray-800 hover:bg-gray-750' : 'bg-white hover:shadow-lg'} rounded-xl shadow-md transition duration-300 overflow-hidden border ${darkMode ? 'border-gray-700' : 'border-gray-100'}`}
              >
                <div className="p-6">
                  <div className="flex justify-between items-start">
                    <h2 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>{deposit.depositName}</h2>
                    <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                      darkMode ? 'bg-indigo-900 text-indigo-200' : 'bg-indigo-100 text-indigo-800'
                    }`}>
                      {deposit.termMonths} months
                    </span>
                  </div>
                  
                  <div className="mt-4 space-y-2">
                    <div className="flex justify-between">
                      <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Bank:</span>
                      <span className={`font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                        {deposit.bankName}
                      </span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Start Date:</span>
                      <span className={`font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                        {new Date(deposit.startDate).toLocaleDateString()}
                      </span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>End Date:</span>
                      <span className={`font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                        {new Date(endDate).toLocaleDateString()}
                      </span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Initial Amount:</span>
                      <span className={`font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                        ₽{deposit.initialAmount.toLocaleString()}
                      </span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Final Amount:</span>
                      <span className="font-medium text-green-600">
                        ₽{deposit.finalAmount.toLocaleString()}
                      </span>
                    </div>
                    
                    <div className="flex justify-between">
                      <span className={`${darkMode ? 'text-gray-400' : 'text-gray-500'}`}>Interest Rate:</span>
                      <span className={`font-medium ${darkMode ? 'text-gray-200' : 'text-gray-700'}`}>
                        {deposit.interestRate}%
                      </span>
                    </div>
                  </div>
                  
                  <div className="mt-6 flex justify-end space-x-2">
                    <button 
                      onClick={() => handleEdit(deposit)}
                      className={`${darkMode ? 'text-blue-400 hover:bg-gray-700' : 'text-blue-600 hover:bg-blue-50'} p-2 rounded-full transition duration-200`}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                      </svg>
                    </button>
                    <button 
                      onClick={() => handleDelete(deposit.id)}
                      className={`${darkMode ? 'text-red-400 hover:bg-gray-700' : 'text-red-600 hover:bg-red-50'} p-2 rounded-full transition duration-200`}
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 001 1v-8z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
          
          {deposits.length === 0 && (
            <div className={`col-span-full ${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-md p-8 text-center`}>
              <svg xmlns="http://www.w3.org/2000/svg" className={`h-16 w-16 mx-auto ${darkMode ? 'text-gray-600' : 'text-gray-400'} mb-4`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M7 15h1m4 0h1m-7 4h12a3 3 0 003-3V8a3 3 0 00-3-3H6a3 3 0 00-3 3v8a3 3 0 003 3z" />
              </svg>
              <h3 className={`text-xl font-semibold ${darkMode ? 'text-gray-200' : 'text-gray-700'} mb-2`}>No deposits found</h3>
              <p className={`${darkMode ? 'text-gray-400' : 'text-gray-500'} mb-4`}>Get started by adding your first deposit</p>
              <button 
                onClick={() => setIsModalOpen(true)}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition duration-300"
              >
                Add Deposit
              </button>
            </div>
          )}
        </div>
      </main>

      {/* Add/Edit Deposit Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div 
            className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-2xl max-w-md w-full max-h-[90vh] overflow-y-auto`}
            onClick={(e) => e.stopPropagation()}
          >
            <div className={`p-6 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
              <div className="flex justify-between items-center">
                <h2 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                  {editingDeposit ? 'Edit Deposit' : 'Add New Deposit'}
                </h2>
                <button 
                  onClick={() => setIsModalOpen(false)}
                  className={`${darkMode ? 'text-gray-400 hover:text-gray-200' : 'text-gray-500 hover:text-gray-700'}`}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
            
            <form onSubmit={handleSubmit} className="p-6 space-y-4">
              <div>
                <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Deposit Name</label>
                <input
                  type="text"
                  name="depositName"
                  value={formData.depositName}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ${
                    darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'border-gray-300'
                  }`}
                  required
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Bank Name</label>
                <input
                  type="text"
                  name="bankName"
                  value={formData.bankName}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ${
                    darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'border-gray-300'
                  }`}
                  required
                />
              </div>
              
              <div>
                <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Start Date</label>
                <input
                  type="date"
                  name="startDate"
                  value={formData.startDate}
                  onChange={handleInputChange}
                  className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ${
                    darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'border-gray-300'
                  }`}
                  required
                />
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Initial Amount (RUB)</label>
                  <input
                    type="number"
                    name="initialAmount"
                    value={formData.initialAmount}
                    onChange={handleInputChange}
                    min="0"
                    step="0.01"
                    className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ${
                      darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'border-gray-300'
                    }`}
                    required
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Term (Months)</label>
                  <input
                    type="number"
                    name="termMonths"
                    value={formData.termMonths}
                    onChange={handleInputChange}
                    min="1"
                    className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ${
                      darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'border-gray-300'
                    }`}
                    required
                  />
                </div>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Interest Rate (%)</label>
                  <input
                    type="number"
                    name="interestRate"
                    value={formData.interestRate}
                    onChange={handleInputChange}
                    min="0"
                    step="0.01"
                    className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ${
                      darkMode ? 'bg-gray-700 border-gray-600 text-white' : 'border-gray-300'
                    }`}
                    required
                  />
                </div>
                
                <div>
                  <label className={`block text-sm font-medium mb-1 ${darkMode ? 'text-gray-300' : 'text-gray-700'}`}>Final Amount (RUB)</label>
                  <input
                    type="number"
                    value={formData.finalAmount || ''}
                    readOnly
                    className={`w-full px-4 py-2 rounded-lg cursor-not-allowed ${
                      darkMode ? 'bg-gray-700 border-gray-600 text-gray-400' : 'bg-gray-50 border-gray-300 text-gray-500'
                    }`}
                  />
                </div>
              </div>
              
              <div className="pt-4">
                <button
                  type="submit"
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 px-4 rounded-lg font-medium transition duration-300"
                >
                  {editingDeposit ? 'Update Deposit' : 'Add Deposit'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Calendar Modal */}
      {showCalendar && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div 
            className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-2xl w-full max-w-3xl max-h-[90vh] overflow-y-auto`}
            onClick={(e) => e.stopPropagation()}
          >
            <div className={`p-6 border-b ${darkMode ? 'border-gray-700' : 'border-gray-200'}`}>
              <div className="flex justify-between items-center">
                <h2 className={`text-xl font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                  Deposit Calendar
                </h2>
                <button 
                  onClick={() => setShowCalendar(false)}
                  className={`${darkMode ? 'text-gray-400 hover:text-gray-200' : 'text-gray-500 hover:text-gray-700'}`}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
              
              {/* Calendar Header */}
              <div className="mt-6 flex justify-between items-center">
                <button
                  onClick={goToPreviousMonth}
                  className={`p-2 rounded-full ${
                    darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                  } transition duration-200`}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
                
                <h3 className={`text-lg font-semibold ${darkMode ? 'text-white' : 'text-gray-800'}`}>
                  {new Date(calendarYear, calendarMonth).toLocaleString('default', { month: 'long', year: 'numeric' })}
                </h3>
                
                <button
                  onClick={goToNextMonth}
                  className={`p-2 rounded-full ${
                    darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100'
                  } transition duration-200`}
                >
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
                  </svg>
                </button>
              </div>
              
              {/* Calendar Days Header */}
              <div className="mt-6 grid grid-cols-7 gap-2">
                {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
                  <div key={day} className="text-center text-sm font-medium py-2">
                    {day}
                  </div>
                ))}
              </div>
              
              {/* Calendar Days Grid */}
              <div className="mt-2 grid grid-cols-7 gap-2">
                {generateCalendarDays().map((day, index) => {
                  const { start, end } = getDepositMarkers(day.date);
                  const dateStr = day.date.toISOString().split('T')[0];
                  
                  return (
                    <div
                      key={index}
                      className={`aspect-square flex flex-col items-center justify-center rounded-lg transition duration-200 ${
                        day.isCurrentMonth
                          ? darkMode ? 'text-white' : 'text-gray-900'
                          : darkMode ? 'text-gray-500' : 'text-gray-400'
                      } ${
                        start || end ? 'font-bold' : ''
                      } ${
                        day.isCurrentMonth
                          ? (darkMode ? 'hover:bg-gray-700' : 'hover:bg-gray-100')
                          : ''
                      }`}
                    >
                      <div className="relative">
                        {start && (
                          <div className="absolute -top-1 -right-1 w-3 h-3 bg-blue-500 rounded-full"></div>
                        )}
                        {end && (
                          <div className="absolute -bottom-1 -left-1 w-3 h-3 bg-green-500 rounded-full"></div>
                        )}
                        <span className="relative z-10">{day.date.getDate()}</span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className={`${darkMode ? 'bg-gray-800 text-gray-400' : 'bg-gray-100 text-gray-600'} py-6 mt-12`}>
        <div className="container mx-auto px-4 text-center">
          <p>© 2023 Bank Deposit Tracker. Manage your deposits effectively.</p>
        </div>
      </footer>
    </div>
  );
};

export default App;