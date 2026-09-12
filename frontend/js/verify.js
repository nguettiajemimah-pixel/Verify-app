/* Verification page logic */

document.getElementById('verification-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const loading = document.getElementById('loading');
  const result = document.getElementById('result');
  const form = e.target;
  
  const formData = {
    registration_number: form.registration_number.value.trim(),
    product_name: form.product_name.value.trim() || null,
    manufacturer: form.manufacturer.value.trim() || null,
  };
  
  loading.style.display = 'block';
  result.style.display = 'none';
  
  try {
    const response = await api.createVerification(formData);
    displayResult(response, formData);
  } catch (error) {
    result.innerHTML = `
      <div class="card" style="border: 2px solid var(--error);">
        <div class="card__title" style="color: var(--error);">Error</div>
        <div class="card__content">
          <p>${error.message || 'Verification failed. Please try again.'}</p>
        </div>
      </div>
    `;
    result.style.display = 'block';
  } finally {
    loading.style.display = 'none';
  }
});

function displayResult(verification, submittedData) {
  const result = document.getElementById('result');
  const statusClass = getStatusClass(verification.match_status);
  
  const matchedFields = verification.matched_fields ? verification.matched_fields.split(',') : [];
  const mismatchedFields = verification.mismatched_fields ? verification.mismatched_fields.split(',') : [];
  const unavailableFields = verification.unavailable_fields ? verification.unavailable_fields.split(',') : [];
  
  let comparisonHtml = '';
  
  if (matchedFields.length > 0 || mismatchedFields.length > 0) {
    comparisonHtml = '<div class="comparison">';
    
    if (submittedData.registration_number) {
      comparisonHtml += createComparisonRow(
        'Registration Number',
        submittedData.registration_number,
        verification.product_id ? 'Found in registry' : 'Not found',
        matchedFields.includes('registration_number')
      );
    }
    
    if (submittedData.product_name) {
      comparisonHtml += createComparisonRow(
        'Product Name',
        submittedData.product_name,
        matchedFields.includes('product_name') ? submittedData.product_name : 'Different in registry',
        matchedFields.includes('product_name')
      );
    }
    
    if (submittedData.manufacturer) {
      comparisonHtml += createComparisonRow(
        'Manufacturer',
        submittedData.manufacturer,
        matchedFields.includes('manufacturer') ? submittedData.manufacturer : 'Different in registry',
        matchedFields.includes('manufacturer')
      );
    }
    
    comparisonHtml += '</div>';
  }
  
  result.innerHTML = `
    <div class="card">
      <div class="status ${statusClass}">${verification.match_status}</div>
      <div class="card__content">
        <p style="margin-bottom: 1.5rem; font-size: 1.1rem;">${verification.explanation}</p>
        
        ${comparisonHtml}
        
        <div style="margin-top: 2rem; padding: 1rem; background-color: var(--background); border-radius: 0.5rem;">
          <p style="font-weight: 600; margin-bottom: 0.5rem;">Registry Information</p>
          <p style="font-size: 0.9rem; color: var(--text-light);">
            Registry Version: ${verification.registry_version}<br>
            This prototype uses demonstration data.
          </p>
        </div>
        
        <div style="margin-top: 2rem; display: flex; gap: 1rem; flex-wrap: wrap;">
          ${verification.match_status === 'DOES_NOT_MATCH' || verification.match_status === 'PARTIAL_MATCH' ? 
            `<a href="/report.html" class="btn btn--primary">Report an Inconsistency</a>` : ''}
          <a href="/verify.html" class="btn btn--secondary">Verify Another Product</a>
        </div>
      </div>
    </div>
  `;
  
  result.style.display = 'block';
}

function createComparisonRow(field, submitted, registry, isMatch) {
  const resultClass = isMatch ? 'comparison__result--match' : 'comparison__result--different';
  const resultText = isMatch ? 'Match' : 'Different';
  
  return `
    <div class="comparison__row">
      <div class="comparison__field">${field}</div>
      <div class="comparison__submitted">Submitted: ${submitted}</div>
      <div class="comparison__registry">Registry: ${registry}</div>
      <div class="comparison__result ${resultClass}">${resultText}</div>
    </div>
  `;
}

function getStatusClass(status) {
  switch (status) {
    case 'MATCH':
      return 'status--match';
    case 'PARTIAL_MATCH':
      return 'status--partial-match';
    case 'DOES_NOT_MATCH':
      return 'status--does-not-match';
    case 'NOT_FOUND':
      return 'status--not-found';
    default:
      return '';
  }
}
