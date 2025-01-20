const API = {
    // Consultas
    async criarConsulta(dados) {
        const response = await fetch('/api/consultas/criar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        return response.json();
    },

    async atualizarConsulta(id, dados) {
        const response = await fetch(`/api/consultas/${id}/atualizar`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(dados)
        });
        return response.json();
    },

    async realizarConsulta(id) {
        const response = await fetch(`/api/consultas/${id}/realizar`, {
            method: 'PUT'
        });
        return response.json();
    },

    async cancelarConsulta(id) {
        const response = await fetch(`/api/consultas/${id}/cancelar`, {
            method: 'PUT'
        });
        return response.json();
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