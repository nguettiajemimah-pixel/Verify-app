/* Reports page logic */

// Check authentication
const token = localStorage.getItem('access_token');
if (!token) {
  window.location.href = '/login.html';
}

// Logout handler
document.getElementById('logout').addEventListener('click', (e) => {
  e.preventDefault();
  localStorage.removeItem('access_token');
  window.location.href = '/index.html';
});

// Load reports
async function loadReports(status = null) {
  const loading = document.getElementById('loading');
  const container = document.getElementById('reports-container');
  
  loading.style.display = 'block';
  
  try {
    const reports = await api.getReports(status);
    displayReports(reports);
  } catch (error) {
    container.innerHTML = `
      <div class="card" style="border: 2px solid var(--error);">
        <div class="card__title" style="color: var(--error);">Error</div>
        <div class="card__content">
          <p>${error.message || 'Failed to load reports.'}</p>
        </div>
      </div>
    `;
  } finally {
    loading.style.display = 'none';
  }
}

function displayReports(reports) {
  const container = document.getElementById('reports-container');
  
  if (reports.length === 0) {
    container.innerHTML = `
      <div class="card">
        <div class="card__content">
          <p>No reports found.</p>
          <p style="color: var(--text-light); font-size: 0.9rem;">
            Reports submitted by consumers will appear here.
          </p>
        </div>
      </div>
    `;
    return;
  }
  
  container.innerHTML = reports.map(report => `
    <div class="card">
      <div class="card__content">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 0.5rem;">
          <div>
            <strong>${report.report_id}</strong>
            <p style="margin: 0.25rem 0;">${report.product_name}</p>
          </div>
          <span style="padding: 0.25rem 0.75rem; border-radius: 0.25rem; font-size: 0.875rem; font-weight: 600; background-color: var(--background);">
            ${report.status}
          </span>
        </div>
        <p style="font-size: 0.9rem; color: var(--text-light); margin: 0.25rem 0;">
          Registration: ${report.registration_number || 'Not provided'}
        </p>
        <p style="font-size: 0.9rem; color: var(--text-light); margin: 0.25rem 0;">
          Manufacturer: ${report.manufacturer || 'Not provided'}
        </p>
        <p style="font-size: 0.9rem; color: var(--text-light); margin: 0.25rem 0;">
          Issue: ${report.issue_type}
        </p>
        <p style="font-size: 0.9rem; color: var(--text-light); margin: 0.25rem 0;">
          Location: ${report.location}
        </p>
        <p style="font-size: 0.85rem; color: var(--text-light); margin-top: 0.5rem;">
          ${new Date(report.created_at).toLocaleString()}
        </p>
        <div style="margin-top: 1rem;">
          <button class="btn btn--primary btn--small" onclick="viewReport('${report.report_id}')">
            View Details
          </button>
        </div>
      </div>
    </div>
  `).join('');
}

// Filter handler
document.getElementById('apply-filter').addEventListener('click', () => {
  const status = document.getElementById('filter-status').value || null;
  loadReports(status);
});

// View report details
function viewReport(reportId) {
  // For MVP, we'll just show an alert. In a full implementation, this would navigate to a detail page.
  alert(`View report ${reportId} - Detail page to be implemented`);
}

// Load reports on page load
loadReports();
