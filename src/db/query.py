# Code generated by sqlc. DO NOT EDIT.
# versions:
#   sqlc v1.28.0
# source: query.sql
from typing import Optional

import sqlalchemy
import sqlalchemy.ext.asyncio

from db import models


CREATE_LEAD = """-- name: create_lead \\:one


INSERT INTO lead_info (
	nome_do_lead
) VALUES ( NULL ) RETURNING id, nome_do_lead, quantidade_de_quartos, com_suite, meio_de_contato, orcamento, criado_em, atualizado_em
"""


CREATE_LEAD_WITH_NAME = """-- name: create_lead_with_name \\:one
INSERT INTO lead_info (
	nome_do_lead
) VALUES ( :p1 ) RETURNING id, nome_do_lead, quantidade_de_quartos, com_suite, meio_de_contato, orcamento, criado_em, atualizado_em
"""


GET_LEAD_BY_ID = """-- name: get_lead_by_id \\:one

SELECT	id, nome_do_lead, quantidade_de_quartos, com_suite, meio_de_contato, orcamento, criado_em, atualizado_em
FROM lead_info as li
	WHERE li.id = :p1
"""


GET_LEAD_BY_NAME = """-- name: get_lead_by_name \\:one
SELECT	id, nome_do_lead, quantidade_de_quartos, com_suite, meio_de_contato, orcamento, criado_em, atualizado_em
FROM lead_info as li
	WHERE li.nome_do_lead = :p1
"""


UPDATE_BUDGET = """-- name: update_budget \\:exec
UPDATE	lead_info
	SET orcamento = :p2
	WHERE id = :p1
"""


UPDATE_LEAD_NAME = """-- name: update_lead_name \\:one

UPDATE	lead_info
	SET nome_do_lead = :p2
	WHERE id = :p1
RETURNING id, nome_do_lead, quantidade_de_quartos, com_suite, meio_de_contato, orcamento, criado_em, atualizado_em
"""


UPDATE_MEANS_OF_CONTACT = """-- name: update_means_of_contact \\:exec
UPDATE	lead_info
	SET meio_de_contato = :p2
	WHERE id = :p1
"""


UPDATE_ROOM_AMMOUNT = """-- name: update_room_ammount \\:exec
UPDATE	lead_info
	SET quantidade_de_quartos = :p2
	WHERE id = :p1
"""


UPDATE_WITH_SUITE = """-- name: update_with_suite \\:exec
UPDATE	lead_info
	SET com_suite = :p2
	WHERE id = :p1
"""


class Querier:
    def __init__(self, conn: sqlalchemy.engine.Connection):
        self._conn = conn

    def create_lead(self) -> Optional[models.LeadInfo]:
        row = self._conn.execute(sqlalchemy.text(CREATE_LEAD)).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    def create_lead_with_name(self, *, nome_do_lead: Optional[str]) -> Optional[models.LeadInfo]:
        row = self._conn.execute(sqlalchemy.text(CREATE_LEAD_WITH_NAME), {"p1": nome_do_lead}).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    def get_lead_by_id(self, *, id: int) -> Optional[models.LeadInfo]:
        row = self._conn.execute(sqlalchemy.text(GET_LEAD_BY_ID), {"p1": id}).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    def get_lead_by_name(self, *, nome_do_lead: Optional[str]) -> Optional[models.LeadInfo]:
        row = self._conn.execute(sqlalchemy.text(GET_LEAD_BY_NAME), {"p1": nome_do_lead}).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    def update_budget(self, *, id: int, orcamento: Optional[int]) -> None:
        self._conn.execute(sqlalchemy.text(UPDATE_BUDGET), {"p1": id, "p2": orcamento})

    def update_lead_name(self, *, id: int, nome_do_lead: Optional[str]) -> Optional[models.LeadInfo]:
        row = self._conn.execute(sqlalchemy.text(UPDATE_LEAD_NAME), {"p1": id, "p2": nome_do_lead}).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    def update_means_of_contact(self, *, id: int, meio_de_contato: Optional[str]) -> None:
        self._conn.execute(sqlalchemy.text(UPDATE_MEANS_OF_CONTACT), {"p1": id, "p2": meio_de_contato})

    def update_room_ammount(self, *, id: int, quantidade_de_quartos: Optional[int]) -> None:
        self._conn.execute(sqlalchemy.text(UPDATE_ROOM_AMMOUNT), {"p1": id, "p2": quantidade_de_quartos})

    def update_with_suite(self, *, id: int, com_suite: Optional[bool]) -> None:
        self._conn.execute(sqlalchemy.text(UPDATE_WITH_SUITE), {"p1": id, "p2": com_suite})


class AsyncQuerier:
    def __init__(self, conn: sqlalchemy.ext.asyncio.AsyncConnection):
        self._conn = conn

    async def create_lead(self) -> Optional[models.LeadInfo]:
        row = (await self._conn.execute(sqlalchemy.text(CREATE_LEAD))).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    async def create_lead_with_name(self, *, nome_do_lead: Optional[str]) -> Optional[models.LeadInfo]:
        row = (await self._conn.execute(sqlalchemy.text(CREATE_LEAD_WITH_NAME), {"p1": nome_do_lead})).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    async def get_lead_by_id(self, *, id: int) -> Optional[models.LeadInfo]:
        row = (await self._conn.execute(sqlalchemy.text(GET_LEAD_BY_ID), {"p1": id})).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    async def get_lead_by_name(self, *, nome_do_lead: Optional[str]) -> Optional[models.LeadInfo]:
        row = (await self._conn.execute(sqlalchemy.text(GET_LEAD_BY_NAME), {"p1": nome_do_lead})).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    async def update_budget(self, *, id: int, orcamento: Optional[int]) -> None:
        await self._conn.execute(sqlalchemy.text(UPDATE_BUDGET), {"p1": id, "p2": orcamento})

    async def update_lead_name(self, *, id: int, nome_do_lead: Optional[str]) -> Optional[models.LeadInfo]:
        row = (await self._conn.execute(sqlalchemy.text(UPDATE_LEAD_NAME), {"p1": id, "p2": nome_do_lead})).first()
        if row is None:
            return None
        return models.LeadInfo(
            id=row[0],
            nome_do_lead=row[1],
            quantidade_de_quartos=row[2],
            com_suite=row[3],
            meio_de_contato=row[4],
            orcamento=row[5],
            criado_em=row[6],
            atualizado_em=row[7],
        )

    async def update_means_of_contact(self, *, id: int, meio_de_contato: Optional[str]) -> None:
        await self._conn.execute(sqlalchemy.text(UPDATE_MEANS_OF_CONTACT), {"p1": id, "p2": meio_de_contato})

    async def update_room_ammount(self, *, id: int, quantidade_de_quartos: Optional[int]) -> None:
        await self._conn.execute(sqlalchemy.text(UPDATE_ROOM_AMMOUNT), {"p1": id, "p2": quantidade_de_quartos})

    async def update_with_suite(self, *, id: int, com_suite: Optional[bool]) -> None:
        await self._conn.execute(sqlalchemy.text(UPDATE_WITH_SUITE), {"p1": id, "p2": com_suite})
