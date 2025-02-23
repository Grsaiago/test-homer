CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS lead_info (
    id SERIAL PRIMARY KEY,  -- pk autoincrement
    nome_do_lead		VARCHAR NULL DEFAULT NULL,
    quantidade_de_quartos   	INTEGER NULL DEFAULT NULL,  -- número de quartos que a pessoa quer
    com_suite		    	BOOLEAN NULL DEFAULT NULL,
    meio_de_contato		VARCHAR NULL DEFAULT NULL,
    orcamento			INTEGER NULL DEFAULT NULL,
    criado_em			TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    atualizado_em		TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE lead_info IS 'Guarda as preferências do usuário para um empreendimento específico.';
COMMENT ON COLUMN lead_info.quantidade_de_quartos IS 'Quantos quartos a pessoa quer na casa.';
COMMENT ON COLUMN lead_info.com_suite IS 'Se a pessoa quer suítes ou não.';
COMMENT ON COLUMN lead_info.meio_de_contato IS 'A forma que a pessoa prefere ser contactada.';
COMMENT ON COLUMN lead_info.orcamento IS 'O valor que a pessoa tem para a compra';

-- Trigger pra tabela de preferências
CREATE TRIGGER update_timestamp_on_row_lead_info
BEFORE UPDATE ON lead_info
FOR EACH ROW
EXECUTE FUNCTION atualizar_timestamp();

