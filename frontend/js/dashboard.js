/* Dashboard page logic */

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

// Load dashboard data
async function loadDashboard() {
  const loading = document.getElementById('loading');
  const content = document.getElementById('dashboard-content');
  
  loading.style.display = 'block';
  content.style.display = 'none';
  
  try {
    const [summary, recentReports] = await Promise.all([
      api.getDashboardSummary(),
      api.getRecentReports(10),
    ]);
    
    displaySummary(summary);
    displayRecentReports(recentReports);
    
    content.style.display = 'block';
  } catch (error) {
    content.innerHTML = `
      <div class="card" style="border: 2px solid var(--error);">
        <div class="card__title" style="color: var(--error);">Error</div>
        <div class="card__content">
          <p>${error.message || 'Failed to load dashboard data.'}</p>
          <a href="/login.html" class="btn btn--primary" style="margin-top: 1rem;">Re-login</a>
        </div>
      </div>
    `;
    content.style.display = 'block';
  } finally {
    loading.style.display = 'none';
  }
}

function displaySummary(summary) {
  document.getElementById('total-reports').textContent = summary.reports.total;
  document.getElementById('new-reports').textContent = summary.reports.new;
  document.getElementById('under-review').textContent = summary.reports.under_review;
  document.getElementById('resolved').textContent = summary.reports.resolved;
  
  document.getElementById('match-count').textContent = summary.verifications.match;
  document.getElementById('partial-match-count').textContent = summary.verifications.partial_match;
  document.getElementById('does-not-match-count').textContent = summary.verifications.does_not_match;
  document.getElementById('not-found-count').textContent = summary.verifications.not_found;
}

function displayRecentReports(reports) {
  const container = document.getElementById('recent-reports');
  
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
          Issue: ${report.issue_type}
        </p>
        <p style="font-size: 0.9rem; color: var(--text-light); margin: 0.25rem 0;">
          Location: ${report.location}
        </p>
        <p style="font-size: 0.85rem; color: var(--text-light); margin-top: 0.5rem;">
          ${new Date(report.created_at).toLocaleString()}
        </p>
      </div>
    </div>
  `).join('');
}

// Load dashboard on page load
loadDashboard();
