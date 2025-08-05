from settings import Settings
from typing import List
from sentence_transformers import SentenceTransformer
import psycopg as pg
from pgvector.psycopg import register_vector
from psycopg import sql

config = Settings()

class OmopConnector():
    def __init__(self) -> None:
        self.uri = config.db_uri()
        self.db_schema = config.db_schema
        self.embeddings_table = config.db_vectable
        self.embeddings_model = SentenceTransformer(config.embeddings_model)
        self.vector_dim = self.embeddings_model.get_sentence_embedding_dimension()

    def vector_search(
            self,
            search_term: str,
            vocabulary_ids: List[str],
            domain_ids: List[str],
            standard_concept: bool = True,
            valid_concept: bool = True,
            ):
        embedding = self.embeddings_model.encode(search_term)
        query_str = """
        WITH embedding_result AS (
            SELECT 
                {embed_table}.concept_id AS concept_id,
                {embed_table}.embedding <=> %(embedding)s AS score 
            FROM {embed_table} 
            WHERE {embed_table}.concept_id IN (
              SELECT {concept_table}.concept_id
              FROM {concept_table}
              WHERE {concept_table}.vocabulary_id = ANY(%(vocabulary_ids)s)
              AND {concept_table}.domain_id = ANY(%(domain_ids)s)"""

        if standard_concept:
            query_str += "AND {concept_table}.standard_concept = 'S'"
        if valid_concept:
            query_str += "AND {concept_table}.invalid_reason IS NULL"

        query_str += """
            )
            ORDER BY score 
             LIMIT 5)
             SELECT {concept_table}.concept_id AS id, {concept_table}.concept_name AS content, embedding_result.score 
            FROM embedding_result JOIN {concept_table} ON {concept_table}.concept_id = embedding_result.concept_id
        """

        query = sql.SQL(query_str).format(
                embed_table = sql.Identifier(self.embeddings_table),
                concept_table = sql.Identifier('concept')
                )

        with pg.connect(self.uri) as conn:
            register_vector(conn)
            conn.execute(sql.SQL("SET SEARCH_PATH to {}, public").format(self.db_schema))
            with conn.cursor() as cur:
                return cur.execute(
                    query,
                    {"embedding": embedding, "vector_dim": self.vector_dim, "vocabulary_ids": vocabulary_ids, "domain_ids": domain_ids}
                    ).fetchall()
    
    def check_concept_id_filter(
            self,
            vocabulary_ids: List[str],
            domain_ids: List[str],
            standard_concept: bool,
            valid_concept: bool,
            ):
        query_str = """
        SELECT COUNT({concept_table}.concept_id)
            FROM {concept_table}
            WHERE {concept_table}.vocabulary_id = ANY(%(vocabulary_ids)s)
            AND {concept_table}.domain_id = ANY(%(domain_ids)s)
        """

        if standard_concept:
            query_str += "AND {concept_table}.standard_concept = 'S'"
        if valid_concept:
            query_str += "AND {concept_table}.invalid_reason IS NULL"

        query = sql.SQL(query_str).format(
                concept_table = sql.Identifier('concept')
                )

        with pg.connect(self.uri) as conn:
            conn.execute(sql.SQL("SET SEARCH_PATH to {}").format(self.db_schema))
            with conn.cursor() as cur:
                return cur.execute(
                        query,
                        {"vocabulary_ids": vocabulary_ids, "domain_ids": domain_ids}
                        ).fetchall()

    def get_all_vocabs(self):
        query = sql.SQL(
                """
                SELECT DISTINCT(vocabulary_id), COUNT(*)
                FROM {}
                GROUP BY vocabulary_id
                ORDER BY COUNT(*) DESC
                """
                ).format(sql.Identifier('concept'))
        with pg.connect(self.uri) as conn:
            conn.execute(sql.SQL("SET SEARCH_PATH to {}").format(sql.Identifier(self.db_schema)))
            return conn.execute(query).fetchall()

    def get_all_domains(self):
        query = sql.SQL(
                """
                SELECT DISTINCT(domain_id), COUNT(*)
                FROM {}
                GROUP BY domain_id
                ORDER BY COUNT(*) DESC
                """
                ).format(sql.Identifier('concept'))
        with pg.connect(self.uri) as conn:
            conn.execute(sql.SQL("SET SEARCH_PATH to {}").format(sql.Identifier(self.db_schema)))
            return conn.execute(query)
