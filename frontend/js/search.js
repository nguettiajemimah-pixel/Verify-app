/* Search page logic */

document.getElementById('search-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const loading = document.getElementById('loading');
  const results = document.getElementById('results');
  const form = e.target;
  
  const query = form.query.value.trim();
  const category = form.category.value || null;
  
  loading.style.display = 'block';
  results.style.display = 'none';
  
  try {
    const products = await api.searchProducts(query, category);
    displayResults(products);
  } catch (error) {
    results.innerHTML = `
      <div class="card" style="border: 2px solid var(--error);">
        <div class="card__title" style="color: var(--error);">Error</div>
        <div class="card__content">
          <p>${error.message || 'Search failed. Please try again.'}</p>
        </div>
      </div>
    `;
    results.style.display = 'block';
  } finally {
    loading.style.display = 'none';
  }
});

function displayResults(products) {
  const results = document.getElementById('results');
  
  if (products.length === 0) {
    results.innerHTML = `
      <div class="card">
        <div class="card__title">No Results Found</div>
        <div class="card__content">
          <p>No matching registry record was found.</p>
          <p style="margin-top: 0.5rem; color: var(--text-light); font-size: 0.9rem;">
            This does not prove that the product is fake. You may try another search or submit an inconsistency report.
          </p>
          <div style="margin-top: 1rem;">
            <a href="/report.html" class="btn btn--outline">Report an Inconsistency</a>
          </div>
        </div>
      </div>
    `;
  } else {
    results.innerHTML = `
      <h2 style="margin-bottom: 1rem;">Found ${products.length} Result${products.length !== 1 ? 's' : ''}</h2>
      ${products.map(product => `
        <div class="card">
          <div class="card__title">${product.name}</div>
          <div class="card__content">
            <p><strong>Registration:</strong> ${product.registration_number}</p>
            <p><strong>Manufacturer:</strong> ${product.manufacturer}</p>
            <p><strong>Category:</strong> ${product.category}</p>
            <p><strong>Status:</strong> ${product.status}</p>
            <p style="font-size: 0.85rem; color: var(--text-light); margin-top: 0.5rem;">
              Last Updated: ${new Date(product.updated_at).toLocaleDateString()}
            </p>
            <div style="margin-top: 1rem;">
              <a href="/verify.html" class="btn btn--primary" onclick="prefillVerification('${product.registration_number}', '${product.name}', '${product.manufacturer}')">
                Verify This Product
              </a>
            </div>
          </div>
        </div>
      `).join('')}
    `;
  }
  
  results.style.display = 'block';
}

function prefillVerification(registrationNumber, productName, manufacturer) {
  // Store in localStorage for prefilling on verify page
  localStorage.setItem('prefill_verification', JSON.stringify({
    registration_number: registrationNumber,
    product_name: productName,
    manufacturer: manufacturer,
  }));
}
