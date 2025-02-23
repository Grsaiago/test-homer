-- CRUD lead_info

-- C lead_info

-- name: CreateLead :one
INSERT INTO lead_info (
	nome_do_lead
) VALUES ( NULL ) RETURNING *;

-- name: CreateLeadWithName :one
INSERT INTO lead_info (
	nome_do_lead
) VALUES ( $1 ) RETURNING *;

-- R lead_info

-- name: GetLeadById :one
SELECT	*
FROM lead_info as li
	WHERE li.id = $1;

-- name: GetLeadByName :one
SELECT	*
FROM lead_info as li
	WHERE li.nome_do_lead = $1;

-- U lead_info

-- name: UpdateLeadName :one
UPDATE	lead_info
	SET nome_do_lead = $2
	WHERE id = $1
RETURNING *;

-- name: UpdateRoomAmmount :exec
UPDATE	lead_info
	SET quantidade_de_quartos = $2
	WHERE id = $1;

-- name: UpdateWithSuite :exec
UPDATE	lead_info
	SET com_suite = $2
	WHERE id = $1;

-- name: UpdateMeansOfContact :exec
UPDATE	lead_info
	SET meio_de_contato = $2
	WHERE id = $1;

-- name: UpdateBudget :exec
UPDATE	lead_info
	SET orcamento = $2
	WHERE id = $1;
