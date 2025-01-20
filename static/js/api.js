const API = {
    async handleResponse(response) {
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro na requisição');
        }
        return response.json();
    },

    // Consultas
    async criarConsulta(dados) {
        try {
            const response = await Utils.fetchWithRetry('/api/consultas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            Utils.mostrarFeedback('Consulta criada com sucesso!');
            return response.json();
        } catch (error) {
            Utils.mostrarFeedback(error.message, 'danger');
            throw error;
        }
    },

    async atualizarConsulta(id, dados) {
        try {
            const response = await Utils.fetchWithRetry(`/api/consultas/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            Utils.mostrarFeedback('Consulta atualizada com sucesso!');
            return response.json();
        } catch (error) {
            Utils.mostrarFeedback(error.message, 'danger');
            throw error;
        }
    },

    async realizarConsulta(id) {
        const response = await fetch(`/api/consultas/${id}/realizar`, {
            method: 'PUT'
        });
        return this.handleResponse(response);
    },

    async cancelarConsulta(id) {
        const response = await fetch(`/api/consultas/${id}/cancelar`, {
            method: 'PUT'
        });
        return this.handleResponse(response);
    },

    async obterConsulta(id) {
        const response = await fetch(`/api/consultas/${id}/detalhes`);
        return response.json();
    },

    // Prontuários
    async criarProntuario(dados) {
        const response = await fetch('/api/prontuarios', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        return response.json();
    },

    async atualizarProntuario(id, dados) {
        const response = await fetch(`/api/prontuarios/${id}/atualizar`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro ao atualizar prontuário');
        }
        return response.json();
    },

    async imprimirProntuario(id) {
        const response = await fetch(`/api/prontuarios/${id}/imprimir`);
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.erro || 'Erro ao imprimir prontuário');
        }
        window.open(`/api/prontuarios/${id}/imprimir`, '_blank');
    },

    // Pacientes
    async criarPaciente(dados) {
        const response = await fetch('/api/pacientes', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        return response.json();
    },

    async obterPaciente(id) {
        const response = await fetch(`/api/pacientes/${id}/detalhes`);
        return response.json();
    },

    async atualizarPaciente(id, dados) {
        const response = await fetch(`/api/pacientes/${id}/atualizar`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        return response.json();
    },

    async excluirPaciente(id) {
        const response = await fetch(`/api/pacientes/${id}/excluir`, {
            method: 'DELETE'
        });
        return response.json();
    },

    async obterHistoricoPaciente(id) {
        const response = await fetch(`/api/pacientes/${id}/historico`);
        return response.json();
    }
};

// Função para carregar detalhes do prontuário
function carregarDetalhesProntuario(prontuarioId) {
    try {
        $.ajax({
            url: `/api/prontuarios/${prontuarioId}/detalhes`,
            method: 'GET',
            success: function(response) {
                if (response && response.dados) {
                    const dados = response.dados;
                    
                    // Preencher os campos do modal
                    $('#modalProntuarioTitulo').text(
                        `Prontuário - ${dados.consulta.paciente.nome}`
                    );
                    $('#modalProntuarioData').text(
                        new Date(dados.consulta.data_hora).toLocaleDateString('pt-BR')
                    );
                    $('#modalProntuarioMedico').text(dados.consulta.medico.nome);
                    $('#modalProntuarioDiagnostico').text(dados.diagnostico || 'Não informado');
                    $('#modalProntuarioPrescricao').text(dados.prescricao || 'Não informado');
                    $('#modalProntuarioExames').text(dados.exames_solicitados || 'Não informado');
                    
                    // Exibir o modal
                    $('#modalProntuario').modal('show');
                } else {
                    console.error('Resposta inválida do servidor');
                    alert('Erro ao carregar dados do prontuário');
                }
            },
            error: function(xhr, status, error) {
                console.error('Erro na requisição:', error);
                alert('Erro ao carregar dados do prontuário');
            }
        });
    } catch (error) {
        console.error('Erro ao processar prontuário:', error);
        alert('Erro ao processar dados do prontuário');
    }
}

// Adicionar listeners quando o documento estiver pronto
$(document).ready(function() {
    // Listener para botões de visualização de prontuário
    $('.btn-ver-prontuario').click(function() {
        const prontuarioId = $(this).data('prontuario-id');
        carregarDetalhesProntuario(prontuarioId);
    });
}); 