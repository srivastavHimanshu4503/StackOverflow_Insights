// Fetch and render all charts

async function fetchDataAndRender(renderer) {
  try {
    const res = await fetch(`https://srivastavhimanshu4503.pythonanywhere.com/api/top-tags-normalized`);
    const data = await res.json();
    renderer(data);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

function renderTopTagsChart(data) {
  const chartContainer = document.getElementById("topTagsChart");
  const dropdown = document.getElementById("yearDropdown");
  const years = Object.keys(data).sort((a, b) => b - a);
  years.forEach((year) => {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    dropdown.appendChild(option);
  });
  dropdown.value = "2024";

  const ctx = chartContainer.getContext("2d");
  let chartInstance;

  function updateChart(year) {
    const yearData = data[year];
    if (!yearData) return;

    const backgroundColors = yearData.tags.map(
      (_, i) => `hsl(${i * 36}, 70%, 55%)`
    );

    const chartConfig = {
      type: "bar",
      data: {
        labels: yearData.tags,
        datasets: [
          {
            label: `Top Tags in ${year}`,
            data: yearData.values,
            backgroundColor: backgroundColors,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: `Top Tags in ${year}`,
          },
          legend: {
            display: false,
          },
        },
        scales: {
          y: {
            beginAtZero: true,
            title: {
              display: true,
              text: "Tag Appearance Rate (%)",
            },
          },
        },
      },
    };

    if (chartInstance) {
      chartInstance.destroy();
    }
    chartInstance = new Chart(ctx, chartConfig);
  }

  updateChart(dropdown.value);
  dropdown.addEventListener("change", (e) => {
    updateChart(e.target.value);
  });
}

async function renderTagTrendsOverTimeChart() {
  try {
    const response = await fetch(
      "https://srivastavhimanshu4503.pythonanywhere.com/api/tag-trends-over-time"
    );
    const data = await response.json();
    const ctx = document.getElementById("tagTrendsChart").getContext("2d");

    // Generate distinct colors for each tag
    const colors = [
      "#FF6384",
      "#36A2EB",
      "#FFCE56",
      "#4BC0C0",
      "#9966FF",
      "#FF9F40",
      "#8B0000",
      "#228B22",
      "#1E90FF",
      "#DAA520",
      "#20B2AA",
      "#CD5C5C",
      "#008080",
      "#BA55D3",
      "#3CB371",
    ];

    const datasets = data.datasets.map((tagData, index) => ({
      label: tagData.label,
      data: tagData.data,
      fill: false,
      borderColor: colors[index % colors.length],
      tension: 0.3,
    }));

    new Chart(ctx, {
      type: "line",
      data: {
        labels: data.labels,
        datasets: datasets,
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: "Tag Trends Over Time (2014–2024)",
          },
          tooltip: {
            mode: "index",
            intersect: false,
          },
          legend: {
            display: true,
            position: "bottom",
          },
        },
        interaction: {
          mode: "nearest",
          axis: "x",
          intersect: false,
        },
        scales: {
          y: {
            title: {
              display: true,
              text: "Normalized Frequency (%)",
            },
            beginAtZero: true,
          },
          x: {
            title: {
              display: true,
              text: "Year",
            },
          },
        },
      },
    });
  } catch (error) {
    console.error("Error fetching tag trends over time:", error);
  }
}

async function renderTagDistributionChart(defaultYear = 2024) {
  const response = await fetch(
    `https://srivastavhimanshu4503.pythonanywhere.com/api/tag-distribution/${defaultYear}`
  );
  const data = await response.json();

  if (data.error) {
    console.error("Error fetching tag distribution:", data.error);
    return;
  }

  const ctx = document.getElementById("tagDistributionChart").getContext("2d");

  // Destroy old chart if it exists
  if (window.tagDistributionChartInstance) {
    window.tagDistributionChartInstance.destroy();
  }

  window.tagDistributionChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: data.labels,
      datasets: [
        {
          data: data.data,
          backgroundColor: data.labels.map(
            (_, i) => `hsl(${(i * 360) / data.labels.length}, 70%, 60%)`
          ),
        },
      ],
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: `Tag Distribution for ${defaultYear}`,
        },
        tooltip: {
          callbacks: {
            label: function (context) {
              return `${context.label}: ${context.raw}%`;
            },
          },
        },
      },
    },
  });
}

async function renderTagUniquenessChart() {
    try {
        const response = await fetch("https://srivastavhimanshu4503.pythonanywhere.com/api/tag-uniqueness");
        const data = await response.json();
        const ctx = document.getElementById("tagUniquenessChart").getContext("2d");

        if (window.tagUniquenessChart instanceof Chart) {
            window.tagUniquenessChart.destroy();
        }

        window.tagUniquenessChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: data.datasets
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Unique vs Repeated Tags per Year (%)'
                    },
                    tooltip: {
                        mode: 'index',
                        intersect: false
                    },
                    legend: {
                        position: 'bottom'
                    }
                },
                scales: {
                    x: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Year'
                        }
                    },
                    y: {
                        stacked: true,
                        title: {
                            display: true,
                            text: 'Percentage (%)'
                        },
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error("Error rendering tag uniqueness chart:", error);
    }
}

// Trigger loading of charts
fetchDataAndRender(renderTopTagsChart);
renderTagTrendsOverTimeChart();
renderTagDistributionChart();
document
  .getElementById("tagDistributionYear")
  .addEventListener("change", function (e) {
    e.preventDefault(); // 👈 Prevents page reload
    const selectedYear = this.value;
    renderTagDistributionChart(selectedYear);
});
document.addEventListener("DOMContentLoaded", renderTagUniquenessChart);

// Add more fetchDataAndRender calls below when other functions are added
