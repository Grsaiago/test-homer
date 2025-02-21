CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TYPE PosicaoDoSol AS ENUM ('Tarde', 'Manhã');

CREATE TABLE lead_info (
	id SERIAL PRIMARY KEY,  -- pk autoincrement
	nome_do_usuario VARCHAR NULL,
	quantidade_de_quartos INTEGER NULL,  -- número de quartos que a pessoa quer
	posicao_do_sol PosicaoDoSol NULL,
	criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE lead_info IS 'Guarda as preferências do usuário para um empreendimento específico';
COMMENT ON COLUMN lead_info.quantidade_de_quartos IS 'A quantidade de quartos que a pessoa quer num apto.';
COMMENT ON COLUMN lead_info.posicao_do_sol IS 'Um enum que diz se a pessoa quer sol da manhã ou da tarde';

-- Trigger pra tabela de preferências
CREATE TRIGGER update_timestamp_on_row_lead_info
BEFORE UPDATE ON lead_info
FOR EACH ROW
EXECUTE FUNCTION atualizar_timestamp();

