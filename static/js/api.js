// Verificar se API já existe para evitar redeclaração
window.API = window.API || {
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
            console.log('Enviando dados:', dados);
            const result = await Utils.fetchWithRetry('/api/consultas', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            
            // O resultado já está em formato JSON
            Utils.mostrarFeedback('Consulta criada com sucesso!');
            return result;
        } catch (error) {
            console.error('Erro ao criar consulta:', error);
            Utils.mostrarFeedback(
                error.message || 'Erro ao criar consulta. Tente novamente.',
                'danger'
            );
            throw error;
        }
    },

    async atualizarConsulta(id, dados) {
        try {
            const result = await Utils.fetchWithRetry(`/api/consultas/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dados)
            });
            Utils.mostrarFeedback('Consulta atualizada com sucesso!');
            return result;
        } catch (error) {
            Utils.mostrarFeedback(error.message, 'danger');
            throw error;
        }
    },

    async realizarConsulta(id) {
        try {
            return await Utils.fetchWithRetry(`/api/consultas/${id}/realizar`, {
                method: 'PUT'
            });
        } catch (error) {
            Utils.mostrarFeedback(error.message, 'danger');
            throw error;
        }
    },

    async cancelarConsulta(id) {
        try {
            return await Utils.fetchWithRetry(`/api/consultas/${id}/cancelar`, {
                method: 'PUT'
            });
        } catch (error) {
            Utils.mostrarFeedback(error.message, 'danger');
            throw error;
        }
    },

    async obterConsulta(id) {
        try {
            console.log(`Obtendo consulta ${id}`);
            const result = await Utils.fetchWithRetry(`/api/consultas/${id}`, {
                method: 'GET',
                headers: { 'Accept': 'application/json' }
            });
            return result;
        } catch (error) {
            console.error('Erro ao obter consulta:', error);
            Utils.mostrarFeedback(
                'Erro ao carregar dados da consulta. Tente novamente.',
                'danger'
            );
            throw error;
        }
    },

    // Prontuários
    async criarProntuario(dados) {
        return await Utils.fetchWithRetry('/api/prontuarios', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
    },

    async atualizarProntuario(id, dados) {
        return await Utils.fetchWithRetry(`/api/prontuarios/${id}/atualizar`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
    },

    async imprimirProntuario(id) {
        const result = await Utils.fetchWithRetry(`/api/prontuarios/${id}/imprimir`);
        window.open(`/api/prontuarios/${id}/imprimir`, '_blank');
        return result;
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