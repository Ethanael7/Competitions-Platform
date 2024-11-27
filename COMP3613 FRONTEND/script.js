const toggleButton = document.getElementById('toggle-button');
const toggleMessage = document.getElementById('toggle-message');
const formTitle = document.getElementById('form-title');
const extraFields = document.getElementById('extra-fields');

toggleButton.addEventListener('click', () => {
  if (formTitle.textContent === 'Login') {
    formTitle.textContent = 'Sign Up';
    toggleMessage.textContent = 'Already have an account?';
    toggleButton.textContent = 'Login';
    extraFields.classList.remove('hidden');
  } else {
    formTitle.textContent = 'Login';
    toggleMessage.textContent = "Don't have an account?";
    toggleButton.textContent = 'Sign up';
    extraFields.classList.add('hidden');
  }
});

document.addEventListener('DOMContentLoaded', () => {
    const username = "Student123"; // Replace with actual data
    const profileHeader = document.createElement('h2');
    profileHeader.textContent = `Welcome, ${username}!`;
    document.body.prepend(profileHeader);
  });