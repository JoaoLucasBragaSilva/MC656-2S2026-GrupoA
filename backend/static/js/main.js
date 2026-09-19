// Máscaras e utilitários globais

// Máscara de CPF
function maskCPF(value) {
    return value
        .replace(/\D/g, '')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d)/, '$1.$2')
        .replace(/(\d{3})(\d{1,2})$/, '$1-$2')
        .slice(0, 14);
}

// Máscara de CNPJ
function maskCNPJ(value) {
    return value
        .replace(/\D/g, '')
        .replace(/^(\d{2})(\d)/, '$1.$2')
        .replace(/^(\d{2})\.(\d{3})(\d)/, '$1.$2.$3')
        .replace(/\.(\d{3})(\d)/, '.$1/$2')
        .replace(/(\d{4})(\d)/, '$1-$2')
        .slice(0, 18);
}

// Máscara de telefone
function maskPhone(value) {
    return value
        .replace(/\D/g, '')
        .replace(/^(\d{2})(\d)/, '($1) $2')
        .replace(/(\d{4,5})(\d{4})$/, '$1-$2')
        .slice(0, 15);
}

// Validação de CPF
function validateCPF(cpf) {
    cpf = cpf.replace(/\D/g, '');
    if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

    let sum = 0;
    for (let i = 0; i < 9; i++) sum += parseInt(cpf[i]) * (10 - i);
    let digit = 11 - (sum % 11);
    if (digit >= 10) digit = 0;
    if (digit !== parseInt(cpf[9])) return false;

    sum = 0;
    for (let i = 0; i < 10; i++) sum += parseInt(cpf[i]) * (11 - i);
    digit = 11 - (sum % 11);
    if (digit >= 10) digit = 0;
    return digit === parseInt(cpf[10]);
}

// Validação de CNPJ
function validateCNPJ(cnpj) {
    cnpj = cnpj.replace(/\D/g, '');
    if (cnpj.length !== 14 || /^(\d)\1+$/.test(cnpj)) return false;

    const calc = (base, weights) => {
        let sum = 0;
        for (let i = 0; i < base.length; i++) sum += parseInt(base[i]) * weights[i];
        const rest = sum % 11;
        return rest < 2 ? 0 : 11 - rest;
    };

    const w1 = [5,4,3,2,9,8,7,6,5,4,3,2];
    const w2 = [6,5,4,3,2,9,8,7,6,5,4,3,2];

    const d1 = calc(cnpj.slice(0, 12), w1);
    const d2 = calc(cnpj.slice(0, 13), w2);

    return cnpj[12] === String(d1) && cnpj[13] === String(d2);
}

// Validação de e-mail
function validateEmail(email) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// Força da senha
function passwordStrength(password) {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) score++;
    if (/\d/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;
    return score; // 0-4
}

// Mostrar erro
function setError(input, message) {
    const form = input.closest('form');
    const errorEl = form.querySelector(`[data-error-for="${input.id}"]`);
    input.classList.add('error');
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.classList.add('show');
    }
}

// Limpar erro
function clearError(input) {
    const form = input.closest('form');
    const errorEl = form.querySelector(`[data-error-for="${input.id}"]`);
    input.classList.remove('error');
    if (errorEl) {
        errorEl.textContent = '';
        errorEl.classList.remove('show');
    }
}

// Toggle senha
document.addEventListener('click', (e) => {
    const toggle = e.target.closest('.toggle-password');
    if (!toggle) return;
    const targetId = toggle.dataset.target;
    const input = document.getElementById(targetId);
    if (!input) return;
    input.type = input.type === 'password' ? 'text' : 'password';
    toggle.style.color = input.type === 'text' ? 'var(--green-600)' : '';
});

// Atualizar força da senha
function bindPasswordStrength(inputId, strengthId) {
    const input = document.getElementById(inputId);
    const strength = document.getElementById(strengthId);
    if (!input || !strength) return;

    input.addEventListener('input', () => {
        const score = passwordStrength(input.value);
        strength.classList.remove('weak', 'fair', 'good', 'strong');
        if (!input.value) return;
        if (score <= 1) strength.classList.add('weak');
        else if (score === 2) strength.classList.add('fair');
        else if (score === 3) strength.classList.add('good');
        else strength.classList.add('strong');
    });
}