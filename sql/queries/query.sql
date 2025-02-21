-- name: UpdateRoomAmmount :exec
UPDATE lead_info
	SET quantidade_de_quartos = $2
	WHERE nome_do_usuario = $1;

-- name: UpdateSunIncidence :exec
UPDATE lead_info
	SET posicao_do_sol = $2
	WHERE nome_do_usuario = $1;
