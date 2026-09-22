document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('form-partido');
    if (!form) return;

    const cnpj = document.getElementById('cnpj');
    const telefone = document.getElementById('telefone');
    const email = document.getElementById('email_partido');
    const senha = document.getElementById('senha_partido');
    const confirmar = document.getElementById('confirmar_senha_partido');
    const termos = document.getElementById('termos_partido');

    // Máscara CNPJ
    cnpj.addEventListener('input', (e) => {
        e.target.value = maskCNPJ(e.target.value);
        if (e.target.value.length === 18) {
            if (validateCNPJ(e.target.value)) clearError(cnpj);
            else setError(cnpj, 'CNPJ inválido.');
        } else {
            clearError(cnpj);
        }
    });

    // Máscara telefone
    telefone.addEventListener('input', (e) => {
        e.target.value = maskPhone(e.target.value);
        clearError(telefone);
    });

    // Sigla em maiúsculas
    const sigla = document.getElementById('sigla');
    sigla.addEventListener('input', (e) => {
        e.target.value = e.target.value.toUpperCase().replace(/[^A-Z]/g, '');
        clearError(sigla);
    });

    [email, senha, confirmar].forEach(input => {
        input.addEventListener('input', () => clearError(input));
    });

    bindPasswordStrength('senha_partido', 'strength-senha_partido');

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

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        let valid = true;

        const nomePartido = document.getElementById('nome_partido');
        const presidente = document.getElementById('presidente');
        const espectro = document.getElementById('espectro');

        if (!nomePartido.value.trim()) { setError(nomePartido, 'Informe o nome do partido.'); valid = false; }
        else clearError(nomePartido);

        if (!sigla.value.trim()) { setError(sigla, 'Informe a sigla.'); valid = false; }
        else clearError(sigla);

        if (!cnpj.value || !validateCNPJ(cnpj.value)) { setError(cnpj, 'CNPJ inválido.'); valid = false; }
        else clearError(cnpj);

        if (!email.value || !validateEmail(email.value)) { setError(email, 'Informe um e-mail válido.'); valid = false; }
        else clearError(email);

        if (!telefone.value || telefone.value.replace(/\D/g, '').length < 10) {
            setError(telefone, 'Informe um telefone válido.');
            valid = false;
        } else clearError(telefone);

        if (!presidente.value.trim()) { setError(presidente, 'Informe o nome do presidente.'); valid = false; }
        else clearError(presidente);

        if (!espectro.value) { setError(espectro, 'Selecione o espectro político.'); valid = false; }
        else clearError(espectro);

        if (!senha.value || senha.value.length < 8) { setError(senha, 'A senha deve ter no mínimo 8 caracteres.'); valid = false; }
        else clearError(senha);

        if (confirmar.value !== senha.value) { setError(confirmar, 'As senhas não coincidem.'); valid = false; }
        else clearError(confirmar);

        if (!termos.checked) {
            termos.closest('.checkbox-label').classList.add('error');
            const errorEl = form.querySelector('[data-error-for="termos_partido"]');
            errorEl.textContent = 'Você precisa aceitar os termos.';
            errorEl.classList.add('show');
            valid = false;
        } else {
            termos.closest('.checkbox-label').classList.remove('error');
            form.querySelector('[data-error-for="termos_partido"]').classList.remove('show');
        }

        if (valid) {
            console.log('✅ Formulário de partido válido — pronto para enviar.');
        } else {
            const firstError = form.querySelector('.error');
            if (firstError) firstError.focus();
        }
    });

    termos.addEventListener('change', () => {
        if (termos.checked) {
            termos.closest('.checkbox-label').classList.remove('error');
            form.querySelector('[data-error-for="termos_partido"]').classList.remove('show');
        }
    });
});