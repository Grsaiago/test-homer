CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TYPE TemperaturaDoLead AS ENUM('Quente', 'Frio', 'Morno');

CREATE TABLE IF NOT EXISTS lead_info (
    id SERIAL PRIMARY KEY,  -- pk autoincrement
    nome_do_lead		VARCHAR NULL DEFAULT NULL,
    quantidade_de_quartos   	INTEGER NULL DEFAULT NULL,  -- número de quartos que a pessoa quer
    bairro			VARCHAR NULL DEFAULT NULL,
    orcamento			INTEGER NULL DEFAULT NULL,
    temperatura_do_lead		TemPeraturaDoLead NOT NULL DEFAULT TemperaturaDoLead.Quente,
    data_e_hora_da_chamada	VARCHAR NULL DEFAULT NULL,
    criado_em			TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em		TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE lead_info IS 'Guarda as preferências do usuário para um empreendimento específico.';
COMMENT ON COLUMN lead_info.quantidade_de_quartos IS 'Quantos quartos a pessoa quer na casa.';
COMMENT ON COLUMN lead_info.bairro IS 'O bairro em que a pessoa está procurando uma casa.';
COMMENT ON COLUMN lead_info.orcamento IS 'O valor que a pessoa tem para a compra.';
COMMENT ON COLUMN lead_info.temperatura_do_lead IS 'O quão "quente" o lead está para uma venda';
COMMENT ON COLUMN lead_info.data_e_hora_da_chamada IS 'A data e hora que a pessoa marcou para ser atendida';

-- Trigger pra tabela de preferências
CREATE TRIGGER update_timestamp_on_row_lead_info
BEFORE UPDATE ON lead_info
FOR EACH ROW
EXECUTE FUNCTION atualizar_timestamp();

