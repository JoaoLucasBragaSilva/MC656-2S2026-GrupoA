document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-votante');
    if (!form) return;

    const cpf = document.getElementById('cpf');
    const email = document.getElementById('email');
    const senha = document.getElementById('senha');
    const confirmar = document.getElementById('confirmar_senha');
    const termos = document.getElementById('termos');

    // Máscara CPF
    cpf.addEventListener('input', (e) => {
        e.target.value = maskCPF(e.target.value);
        if (e.target.value.length === 14) {
            if (validateCPF(e.target.value)) clearError(cpf);
            else setError(cpf, 'CPF inválido.');
        } else {
            clearError(cpf);
        }
    });

    // Limpar erros ao digitar
    [email, senha, confirmar].forEach(input => {
        input.addEventListener('input', () => clearError(input));
    });

    // Força da senha
    bindPasswordStrength('senha', 'strength-senha');

    // Validação no blur
    email.addEventListener('blur', () => {
        if (email.value && !validateEmail(email.value)) {
            setError(email, 'Informe um e-mail válido.');
        }
    });

    confirmar.addEventListener('blur', () => {
        if (confirmar.value && confirmar.value !== senha.value) {
            setError(confirmar, 'As senhas não coincidem.');
        }
    });

    // Submit
    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let valid = true;

        const nome = document.getElementById('nome');
        const nascimento = document.getElementById('nascimento');

        if (!nome.value.trim()) { setError(nome, 'Informe seu nome completo.'); valid = false; }
        else clearError(nome);

        if (!cpf.value || !validateCPF(cpf.value)) { setError(cpf, 'CPF inválido.'); valid = false; }
        else clearError(cpf);

        if (!nascimento.value) { setError(nascimento, 'Informe sua data de nascimento.'); valid = false; }
        else clearError(nascimento);

        if (!email.value || !validateEmail(email.value)) { setError(email, 'Informe um e-mail válido.'); valid = false; }
        else clearError(email);

        if (!senha.value || senha.value.length < 8) { setError(senha, 'A senha deve ter no mínimo 8 caracteres.'); valid = false; }
        else clearError(senha);

        if (confirmar.value !== senha.value) { setError(confirmar, 'As senhas não coincidem.'); valid = false; }
        else clearError(confirmar);

        if (!termos.checked) {
            const label = termos.closest('.checkbox-label');
            label.classList.add('error');
            const errorEl = form.querySelector('[data-error-for="termos"]');
            errorEl.textContent = 'Você precisa aceitar os termos.';
            errorEl.classList.add('show');
            valid = false;
        } else {
            termos.closest('.checkbox-label').classList.remove('error');
            const errorEl = form.querySelector('[data-error-for="termos"]');
            errorEl.classList.remove('show');
        }

        if (valid) {
            console.log('✅ Formulário válido — pronto para enviar ao backend.');
            // Aqui você fará o fetch/axios para o backend Django
        } else {
            // Focar no primeiro erro
            const firstError = form.querySelector('.error');
            if (firstError) firstError.focus();
        }
    });

    // Remover erro do checkbox ao marcar
    termos.addEventListener('change', () => {
        if (termos.checked) {
            termos.closest('.checkbox-label').classList.remove('error');
            form.querySelector('[data-error-for="termos"]').classList.remove('show');
        }
    });
});