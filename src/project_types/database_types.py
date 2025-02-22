from psycopg_pool.pool import ConnectionPool
from sqlalchemy import (
    create_engine,
)  # https://docs.sqlalchemy.org/en/20/core/engines.html#sqlalchemy.create_engine
from sqlalchemy import URL

from db.models import LeadInfo
from db.query import GetLeadByNameRow, Querier
from project_types.state_types import PosicaoDoSol
from .env_types import envs
from sqlalchemy.engine import Engine


class DatabaseLayer:
    llm_db_engine: Engine | None = (
        None  # this will connect to the db with write permissions only to the tables that the llm will write to
    )
    lang_graph_pool: ConnectionPool | None = (
        None  # this will be used by langGraph's PostgresSaver class
    )

    def __init__(self, db_user: str, db_passwd: str, db_host: str, db_name: str):
        # create psycopgpool
        psyco_pool_connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        psyco_pool_connection_string = (
            f"postgresql://{db_user}:{db_passwd}@{db_host}:5432/{db_name}"
        )
        self.lang_graph_pool = ConnectionPool(
            conninfo=psyco_pool_connection_string,
            max_size=20,
            kwargs=psyco_pool_connection_kwargs,
        )

        # create alchemysql Engine using the psycopg pool
        sqlalchemy_opts = URL.create(
            "postgresql+psycopg2",
            username=db_user,
            password=db_passwd,
            host=db_host,
            database=db_name,
        )
        self.llm_db_engine = create_engine(
            sqlalchemy_opts,
        )

    def get_llm_db_engine(self) -> Engine:
        """
        Retuns a reference to the singleton's sqlalchemy engine.
        This method should be used to get a new sqlalchemy connection to be used in sqlc generated queries.
        """
        assert self.llm_db_engine is not None
        return self.llm_db_engine

    def get_lang_graph_pool(self) -> ConnectionPool:
        """
        Retuns a reference to the singleton's connection_pool made with psycopg_pool
        """
        assert self.lang_graph_pool is not None
        return self.lang_graph_pool

    ## Access to the database layer, this should be an interface reexporting sqlc generated functions, but well it's python xD
    def update_room_ammount(
        self, nome_do_usuario: str, quantidade_de_quartos: int
    ) -> None:
        with self.get_llm_db_engine().connect() as connection:
            Querier(connection).update_room_ammount(
                nome_do_usuario=nome_do_usuario,
                quantidade_de_quartos=quantidade_de_quartos,
            )
            connection.commit()
        return None

    def update_sun_incidence(
        self, nome_do_usuario: str, sun_position: PosicaoDoSol
    ) -> None:
        with self.get_llm_db_engine().connect() as connection:
            Querier(connection).update_sun_incidence(
                nome_do_usuario=nome_do_usuario,
                posicao_do_sol=sun_position,
            )
            connection.commit()
        return None

    # crud for lead
    def get_lead_by_name(self, lead: str) -> GetLeadByNameRow | None:
        with self.get_llm_db_engine().connect() as connection:
            found_lead = Querier(connection).get_lead_by_name(nome_do_usuario=lead)
            connection.commit()
        return found_lead

    def create_lead_by_name(self, new_lead_name: str) -> GetLeadByNameRow:
        with self.get_llm_db_engine().connect() as connection:
            new_lead = Querier(connection).create_new_lead(
                nome_do_usuario=new_lead_name
            )
            assert new_lead is not None
            connection.commit()
        return GetLeadByNameRow(
            nome_do_usuario=new_lead.nome_do_usuario,
            posicao_do_sol=new_lead.posicao_do_sol,
            quantidade_de_quartos=new_lead.quantidade_de_quartos,
        )

    def get_or_insert_lead_by_name(self, lead_name: str) -> GetLeadByNameRow:
        lead = self.get_lead_by_name(lead_name)
        if lead is None:
            lead = self.create_lead_by_name(lead_name)
        return lead


database_layer = DatabaseLayer(envs.db_user, envs.db_passwd, envs.db_host, envs.db_name)
