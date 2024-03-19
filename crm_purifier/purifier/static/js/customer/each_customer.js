function togglePasswordVisibility(toggleElement, passwordInput) {
    let clickCount = 0;

    toggleElement.addEventListener('click', function () {
        clickCount++;
        const type = clickCount % 2 === 1 ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
    });
}

const togglePassword = document.querySelector('.toggle-password-icon');
const passwordInput = document.querySelector('#customerInitialPassword');

togglePasswordVisibility(togglePassword, passwordInput);
