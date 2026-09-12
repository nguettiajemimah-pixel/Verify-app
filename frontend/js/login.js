/* Login page logic */

document.getElementById('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const loading = document.getElementById('loading');
  const error = document.getElementById('error');
  const form = e.target;
  
  const email = form.email.value.trim();
  const password = form.password.value;
  
  loading.style.display = 'block';
  error.style.display = 'none';
  
  try {
    const response = await api.login(email, password);
    localStorage.setItem('access_token', response.access_token);
    window.location.href = '/dashboard.html';
  } catch (err) {
    error.textContent = err.message || 'Your email or password is incorrect.';
    error.style.display = 'block';
  } finally {
    loading.style.display = 'none';
  }
});
