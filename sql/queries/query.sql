-- name: UpdateRoomAmmount :exec
UPDATE	lead_info
	SET quantidade_de_quartos = $2
	WHERE nome_do_lead = $1;

-- name: UpdateSunIncidence :exec
UPDATE	lead_info as li
	SET posicao_do_sol = $2
	WHERE nome_do_lead = $1;

-- name: GetLeadByName :one
SELECT	li.nome_do_lead,
	li.quantidade_de_quartos,
	li.posicao_do_sol
FROM lead_info as li
	WHERE li.nome_do_lead = $1;

-- name: CreateNewLead :one
INSERT INTO lead_info (
	nome_do_lead
) VALUES ( $1 ) RETURNING *;
