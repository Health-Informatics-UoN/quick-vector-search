import marimo

__generated_with = "0.14.16"
app = marimo.App(width="columns", app_title="Quick Vector Search")


@app.cell
def _(mo):
    mo.md(
        r"""
    ## Simple vector search

    You can search an OMOP CDM database with an added embeddings table with this tool. If it's not working, you probably need to set up a .env file for your database. I tried to make sensible defaults.

    You need to select one or more for the vocabulary_id and domain_id, configurable in the menu below.
    """
    )
    return


@app.cell
def _():
    import marimo as mo
    from settings import Settings
    from db import OmopConnector
    return OmopConnector, mo


@app.cell
def _(OmopConnector):
    omop_connector = OmopConnector()
    return (omop_connector,)


@app.cell
def _(mo, omop_connector):
    vocab_table = mo.ui.table(
        [
            {"vocab": row[0], "count": row[1]}
            for row in omop_connector.get_all_vocabs()
        ]
    )
    domain_table = mo.ui.table(
        [
            {"domain": row[0], "count": row[1]}
            for row in omop_connector.get_all_domains()
        ]
    )
    return domain_table, vocab_table


@app.cell
def _(mo):
    standard_concept = mo.ui.checkbox(label="Standard concepts only?", value=True)
    valid_concept = mo.ui.checkbox(label="Valid concepts only?", value=True)
    return standard_concept, valid_concept


@app.cell
def _(vocab_table):
    active_vocabs = [v["vocab"] for v in vocab_table.value]
    return (active_vocabs,)


@app.cell
def _(domain_table):
    active_domains = [v["domain"] for v in domain_table.value]
    return (active_domains,)


@app.cell
def _(domain_table, mo, standard_concept, valid_concept, vocab_table):
    mo.accordion(
        {
            "Filter standard/valid": mo.vstack([standard_concept, valid_concept]),
            "Filter by vocabulary": vocab_table,
            "Filter by domain": domain_table,
        }
    )
    return


@app.cell
def _(
    active_domains,
    active_vocabs,
    mo,
    omop_connector,
    standard_concept,
    valid_concept,
):
    n_concepts = omop_connector.check_concept_id_filter(
        vocabulary_ids=active_vocabs,
        domain_ids=active_domains,
        standard_concept=standard_concept.value,
        valid_concept=valid_concept.value,
    )[0][0]
    mo.md(f"With these settings, you're searching through {n_concepts} concepts")
    return


@app.cell
def _(mo, omop_connector):
    n_embeddings = omop_connector.count_vectors()[0][0]

    mo.md(f"Your database contains {n_embeddings} embeddings.")
    return


@app.cell
def _(mo):
    search_term = mo.ui.text(value="Paracetamol", label="Search Term").form()
    search_term
    return (search_term,)


@app.cell
def _(
    active_domains,
    active_vocabs,
    mo,
    omop_connector,
    search_term,
    standard_concept,
    valid_concept,
):
    if search_term.value is not None:
        result = omop_connector.vector_search(
            search_term=search_term.value,
            domain_ids=active_domains,
            vocabulary_ids=active_vocabs,
            standard_concept=standard_concept.value,
            valid_concept=valid_concept.value,
        )
    else:
        result = [(0, "no matching concept", 0)]

    mo.ui.table(
        [
            {"concept_id": row[0], "concept_name": row[1], "score": row[2]}
            for row in result
        ]
    )
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
