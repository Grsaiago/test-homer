-- CRUD lead_info
-- U lead_info

-- name: UpdateRoomAmmount :exec
UPDATE	lead_info
	SET quantidade_de_quartos = $2
	WHERE nome_do_lead = $1;

-- name: UpdateSunIncidence :exec
UPDATE	lead_info
	SET posicao_do_sol = $2
	WHERE nome_do_lead = $1;

-- name: UpdateLeadName :one
UPDATE	lead_info
	SET nome_do_lead = $2
	WHERE id = $1
	RETURNING *;

-- R lead_info

-- name: GetLeadById :one
SELECT	*
FROM lead_info as li
	WHERE li.id = $1;

-- name: GetLeadByName :one
SELECT	*
FROM lead_info as li
	WHERE li.nome_do_lead = $1;

-- C lead_info

-- name: CreateLead :one
INSERT INTO lead_info (
	nome_do_lead, quantidade_de_quartos, posicao_do_sol
) VALUES ( NULL, NULL, NULL ) RETURNING *;

-- name: CreateLeadWithName :one
INSERT INTO lead_info (
	nome_do_lead
) VALUES ( $1 ) RETURNING *;
