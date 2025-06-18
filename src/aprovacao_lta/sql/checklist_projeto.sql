-- Criação do schema para organização lógica
CREATE SCHEMA IF NOT EXISTS aprovacao_projeto;

-- Criação da tabela principal de checklist
CREATE TABLE IF NOT EXISTS aprovacao_projeto.checklist (
    id SERIAL PRIMARY KEY,
    numero_item INT NOT NULL UNIQUE, -- número sequencial da pergunta
    pergunta TEXT NOT NULL, -- pergunta técnica
    texto_legal TEXT, -- texto da norma ou artigo legal
    interpretacao_legal TEXT, -- explicação ou resumo da exigência
    orientacao_documentacao TEXT, -- instrução para representação gráfica
    base_legal TEXT, -- ex: Lei 13.146/2015
    observacao_fluxo TEXT, -- Observações sobre o fluxo de avaliação/inspeção

    resposta VARCHAR(20) CHECK (resposta IN ('SIM', 'NÃO')), -- RESTAURADO PARA APENAS 'SIM' E 'NÃO'
    
    atende BOOLEAN, -- opcional
    nao_atende BOOLEAN, -- opcional
    medida_mitigatoria TEXT, -- justificativa técnica ou compensação
    -- REMOVIDO: justificativa_nao_se_aplica TEXT, -- explicação para "NÃO SE APLICA"
    
    comentario_requerente TEXT, -- opcional
    comentario_avaliador TEXT, -- avaliação do técnico
    
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    
    -- ADICIONE AQUI UMA COLUNA PARA CONTROLAR SE A PERGUNTA SE APLICA OU NÃO, SE NECESSÁRIO
    -- Por exemplo:
    -- se_aplica_a_projeto BOOLEAN DEFAULT TRUE,
    -- ou
    -- tipo_de_projeto_aplicavel VARCHAR(50) -- 'TODOS', 'RESIDENCIAL', 'COMERCIAL', etc.
);