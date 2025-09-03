document.getElementById('inventoryForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const form = e.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  const messageDiv = document.getElementById('message');
  messageDiv.textContent = 'Submitting...';
  messageDiv.className = '';

  try {
    const response = await fetch('/submit', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });

    const result = await response.json();

    if (result.success) {
      messageDiv.textContent = '✅ Data saved successfully!';
      messageDiv.className = 'success';
      form.reset();
    } else {
      messageDiv.textContent = '❌ Error: ' + result.error;
      messageDiv.className = 'error';
    }
  } catch (err) {
    messageDiv.textContent = '❌ Network error. Try again.';
    messageDiv.className = 'error';
  }
});