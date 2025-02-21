CREATE TYPE PosicaoDoSol AS ENUM ('Tarde', 'Manhã');

-- A tabela de preferências do usuário
CREATE TABLE user_preferences (
	id SERIAL PRIMARY KEY,  -- pk autoincrement
	quantidade_de_quartos INTEGER NULL,  -- número de quartos que a pessoa quer
	posicao_do_sol PosicaoDoSol NULL,
	criado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
	atualizado_em TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION atualizar_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.atualizado_em = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER atualizar_timestamp_da_linha
BEFORE UPDATE ON user_preferences
FOR EACH ROW
EXECUTE FUNCTION atualizar_timestamp();

COMMENT ON TABLE user_preferences IS 'Guarda as preferências do usuário para um empreendimento específico';
COMMENT ON COLUMN user_preferences.quantidade_de_quartos IS 'A quantidade de quartos que a pessoa quer num apto.';
COMMENT ON COLUMN user_preferences.posicao_do_sol IS 'Um enum que diz se a pessoa quer sol da manhã ou da tarde';
