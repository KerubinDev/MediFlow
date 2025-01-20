// Utility Functions
const Utils = {
    // Feedback Visual
    mostrarFeedback: function(mensagem, tipo = 'success') {
        const feedback = document.createElement('div');
        feedback.className = `alert alert-${tipo} glass-card feedback-alert`;
        feedback.textContent = mensagem;
        document.body.appendChild(feedback);
        
        setTimeout(() => feedback.remove(), 3000);
    },

    // Loading State
    toggleLoading: function(show = true) {
        const loadingEl = document.querySelector('.loading-overlay');
        if (show) {
            if (!loadingEl) {
                const overlay = document.createElement('div');
                overlay.className = 'loading-overlay';
                overlay.innerHTML = '<div class="spinner"></div>';
                document.body.appendChild(overlay);
            }
        } else {
            loadingEl?.remove();
        }
    },

    // Form Validation
    validarFormulario: function(formId) {
        const form = document.getElementById(formId);
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.classList.add('is-invalid');
                
                // Adicionar mensagem de erro se não existir
                let feedback = input.nextElementSibling;
                if (!feedback || !feedback.classList.contains('invalid-feedback')) {
                    feedback = document.createElement('div');
                    feedback.className = 'invalid-feedback';
                    feedback.textContent = 'Este campo é obrigatório';
                    input.parentNode.insertBefore(feedback, input.nextSibling);
                }
            } else {
                input.classList.remove('is-invalid');
                const feedback = input.nextElementSibling;
                if (feedback && feedback.classList.contains('invalid-feedback')) {
                    feedback.remove();
                }
            }
        });
        
        return isValid;
    },

    // Modal Management
    limparModais: function() {
        try {
            document.querySelectorAll('.modal-backdrop').forEach(el => el.remove());
            document.body.classList.remove('modal-open');
            document.body.style.overflow = 'auto';
            document.body.style.paddingRight = '0';
            
            document.querySelectorAll('.modal').forEach(modal => {
                try {
                    const modalInstance = bootstrap.Modal.getInstance(modal);
                    if (modalInstance) {
                        modalInstance.hide();
                    }
                } catch (error) {
                    console.warn('Erro ao fechar modal:', error);
                }
                modal.classList.remove('show');
                modal.style.display = 'none';
            });
        } catch (error) {
            console.error('Erro ao limpar modais:', error);
        }
    },

    // API Calls with Retry
    fetchWithRetry: async function(url, options = {}, retries = 3) {
        try {
            Utils.toggleLoading(true);
            
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 5000);
            
            options.signal = controller.signal;
            options.headers = {
                ...options.headers,
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            };
            
            const response = await fetch(url, options);
            clearTimeout(timeoutId);
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(JSON.stringify({
                    code: response.status,
                    message: errorData.erro || errorData.description || 'Erro desconhecido'
                }));
            }
            
            return response;
        } catch (error) {
            if (retries > 0 && !error.name === 'AbortError') {
                console.warn(`Tentativa falhou, tentando novamente... (${retries} tentativas restantes)`);
                await new Promise(resolve => setTimeout(resolve, 1000));
                return Utils.fetchWithRetry(url, options, retries - 1);
            }
            throw error;
        } finally {
            Utils.toggleLoading(false);
        }
    }
};

// Debounce Function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
} 