/* Report page logic */

document.getElementById('report-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const loading = document.getElementById('loading');
  const result = document.getElementById('result');
  const form = e.target;
  
  const formData = {
    product_name: form.product_name.value.trim(),
    registration_number: form.registration_number.value.trim() || null,
    manufacturer: form.manufacturer.value.trim() || null,
    issue_type: form.issue_type.value,
    description: form.description.value.trim(),
    location: form.location.value.trim(),
  };
  
  loading.style.display = 'block';
  result.style.display = 'none';
  
  try {
    const response = await api.createReport(formData);
    displayResult(response);
  } catch (error) {
    result.innerHTML = `
      <div class="card" style="border: 2px solid var(--error);">
        <div class="card__title" style="color: var(--error);">Error</div>
        <div class="card__content">
          <p>${error.message || 'Report submission failed. Please try again.'}</p>
        </div>
      </div>
    `;
    result.style.display = 'block';
  } finally {
    loading.style.display = 'none';
  }
});

function displayResult(report) {
  const result = document.getElementById('result');
  
  result.innerHTML = `
    <div class="card" style="border: 2px solid var(--success);">
      <div class="status status--match" style="font-size: 1.25rem;">Report Submitted</div>
      <div class="card__content">
        <p style="margin-bottom: 1rem;">Thank you for reporting this inconsistency.</p>
        <p style="margin-bottom: 1.5rem;">Your report has been submitted for review.</p>
        
        <div style="padding: 1rem; background-color: var(--background); border-radius: 0.5rem; margin-bottom: 1.5rem;">
          <p><strong>Report ID:</strong> ${report.report_id}</p>
          <p><strong>Status:</strong> ${report.status}</p>
          <p><strong>Product:</strong> ${report.product_name}</p>
        </div>
        
        <p style="font-size: 0.9rem; color: var(--text-light);">
          Note: This report is an observation, not a confirmed regulatory conclusion.
        </p>
        
        <div style="margin-top: 2rem;">
          <a href="/index.html" class="btn btn--primary">Return Home</a>
          <a href="/verify.html" class="btn btn--secondary" style="margin-left: 0.5rem;">Verify Another Product</a>
        </div>
      </div>
    </div>
  `;
  
  result.style.display = 'block';
}
