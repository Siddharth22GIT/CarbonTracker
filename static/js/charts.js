// Initialize charts on dashboard page
document.addEventListener('DOMContentLoaded', function() {
    // Check if we're on a page with charts
    if (document.getElementById('emissionsPieChart')) {
        initializePieChart();
    }
    
    if (document.getElementById('emissionsTrendChart')) {
        initializeTrendChart();
    }
});

// Initialize pie chart for emissions by category
function initializePieChart() {
    const ctx = document.getElementById('emissionsPieChart').getContext('2d');
    
    // Get data from the data attribute
    const chartDataElement = document.getElementById('chartData');
    
    if (!chartDataElement) {
        console.error('Chart data element not found');
        return;
    }
    
    const chartData = JSON.parse(chartDataElement.textContent);
    
    // Generate random colors for each category
    const backgroundColors = generateColorPalette(chartData.labels.length);
    
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: chartData.labels,
            datasets: [{
                data: chartData.data,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                    labels: {
                        color: '#fff'
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} kg CO2e (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Initialize trend chart for emissions over time
function initializeTrendChart() {
    const ctx = document.getElementById('emissionsTrendChart').getContext('2d');
    
    // Get data from the data attribute
    const trendDataElement = document.getElementById('trendData');
    
    if (!trendDataElement) {
        console.error('Trend data element not found');
        return;
    }
    
    const trendData = JSON.parse(trendDataElement.textContent);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendData.labels,
            datasets: [{
                label: 'Monthly Emissions',
                data: trendData.data,
                borderColor: '#0dcaf0',
                backgroundColor: 'rgba(13, 202, 240, 0.1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true,
                pointBackgroundColor: '#0dcaf0',
                pointBorderColor: '#fff',
                pointRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.raw} kg CO2e`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    }
                },
                y: {
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#fff'
                    },
                    beginAtZero: true
                }
            }
        }
    });
}

// Generate a color palette for the charts
function generateColorPalette(count) {
    const baseColors = [
        '#0d6efd', // blue
        '#6610f2', // indigo
        '#6f42c1', // purple
        '#d63384', // pink
        '#dc3545', // red
        '#fd7e14', // orange
        '#ffc107', // yellow
        '#198754', // green
        '#20c997', // teal
        '#0dcaf0', // cyan
    ];
    
    let colors = [];
    
    // If we need more colors than available, cycle through the base colors
    for (let i = 0; i < count; i++) {
        colors.push(baseColors[i % baseColors.length]);
    }
    
    return colors;
}

// Handle target progress bars
document.addEventListener('DOMContentLoaded', function() {
    // Update all progress bars
    const progressBars = document.querySelectorAll('[data-progress]');
    
    progressBars.forEach(bar => {
        const progress = parseFloat(bar.getAttribute('data-progress'));
        const target = parseFloat(bar.getAttribute('data-target'));
        
        // Calculate percentage (capped at 100%)
        let percentage = Math.min((progress / target) * 100, 100);
        
        // Update width
        bar.style.width = percentage + '%';
        
        // Update color based on progress
        if (percentage < 50) {
            bar.classList.add('bg-success');
        } else if (percentage < 75) {
            bar.classList.add('bg-warning');
        } else {
            bar.classList.add('bg-danger');
        }
    });
});

// Filter handling for activities and reports
document.addEventListener('DOMContentLoaded', function() {
    const filterForms = document.querySelectorAll('.filter-form');
    
    filterForms.forEach(form => {
        // Auto-submit on category change
        const categorySelect = form.querySelector('select[name="category"]');
        if (categorySelect) {
            categorySelect.addEventListener('change', function() {
                form.submit();
            });
        }
        
        // Date picker handling
        const dateInputs = form.querySelectorAll('input[type="date"]');
        dateInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Only submit if both dates are filled or both are empty
                const fromDate = form.querySelector('input[name="from_date"]');
                const toDate = form.querySelector('input[name="to_date"]');
                
                if ((fromDate.value && toDate.value) || (!fromDate.value && !toDate.value)) {
                    form.submit();
                }
            });
        });
    });
});
