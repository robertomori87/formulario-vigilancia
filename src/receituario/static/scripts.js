document.addEventListener('DOMContentLoaded', function() {
    // Referências aos elementos HTML
    const thirdPartyYes = document.getElementById('third_party_yes');
    const thirdPartyNo = document.getElementById('third_party_no');
    const nomeTerceiro = document.getElementById('nome_terceiro');
    const cpfTerceiro = document.getElementById('cpf_terceiro');
    const thirdPartyFieldsDiv = document.getElementById('third_party_fields');

    /**
     * Alterna a visibilidade e acessibilidade dos campos do terceiro autorizado.
     * Se 'Sim' for selecionado, os campos são habilitados e tornados obrigatórios.
     * Se 'Não' for selecionado, os campos são desabilitados, seus valores limpos e a obrigatoriedade removida.
     */
    function toggleThirdPartyFields() {
        const isThirdParty = thirdPartyYes.checked; // Verifica se a opção 'Sim' está marcada

        // Habilita/desabilita os campos de input
        nomeTerceiro.disabled = !isThirdParty;
        cpfTerceiro.disabled = !isThirdParty;

        // Torna os campos obrigatórios ou não, dependendo da seleção
        nomeTerceiro.required = isThirdParty;
        cpfTerceiro.required = isThirdParty;

        // Limpa os valores dos campos se eles forem desabilitados
        if (!isThirdParty) {
            nomeTerceiro.value = '';
            cpfTerceiro.value = '';
            // Opcional: Adicionar estilo para indicar que estão desabilitados
            thirdPartyFieldsDiv.classList.add('opacity-50', 'pointer-events-none');
        } else {
            // Opcional: Remover estilo de desabilitado
            thirdPartyFieldsDiv.classList.remove('opacity-50', 'pointer-events-none');
        }
    }

    // Adiciona event listeners para as mudanças nos rádio buttons
    thirdPartyYes.addEventListener('change', toggleThirdPartyFields);
    thirdPartyNo.addEventListener('change', toggleThirdPartyFields);

    // Chamada inicial para configurar o estado dos campos ao carregar a página
    toggleThirdPartyFields();
});

/**
 * Função de validação de formulário.
 * Incorpora a lógica para validar campos de terceiro autorizado condicionalmente.
 * @returns {boolean} True se o formulário for válido, false caso contrário.
 */
function validarFormulario() {
    const nome = document.getElementById("nome").value;
    const cpfCnpj = document.getElementById("cpf_cnpj").value.replace(/\D/g, '');
    const telefone = document.getElementById("telefone").value.replace(/\D/g, '');
    
    const thirdPartyYesChecked = document.getElementById('third_party_yes').checked;

    // Validações gerais
    if (/\d/.test(nome) || nome.length < 3) {
        alert("Nome inválido.");
        return false;
    }
    if (telefone.length < 10 || telefone.length > 11) {
        alert("Telefone inválido.");
        return false;
    }
    if (cpfCnpj.length !== 11 && cpfCnpj.length !== 14) {
        alert("CPF ou CNPJ inválido.");
        return false;
    }

    // Validação condicional para o terceiro autorizado
    if (thirdPartyYesChecked) { // Apenas valida se a opção 'Sim' estiver marcada
        const nomeTerceiro = document.getElementById("nome_terceiro").value;
        const cpfTerceiro = document.getElementById("cpf_terceiro").value.replace(/\D/g, '');

        if (/\d/.test(nomeTerceiro) || nomeTerceiro.length < 3) {
            alert("Nome do terceiro inválido.");
            return false;
        }
        if (cpfTerceiro.length !== 11) { // Considerando que CPF tem 11 dígitos
            alert("CPF do terceiro inválido.");
            return false;
        }
    }

    return true;
}