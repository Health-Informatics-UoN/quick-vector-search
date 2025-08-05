# Quick Vector Search

A user-friendly interface for performing vector search on OMOP (Observational Medical Outcomes Partnership) databases with embedded Common Data Model (CDM) data.

## Overview

This tool provides a streamlined way to search through medical data using semantic vector similarity. It leverages embeddings stored alongside your OMOP CDM data to enable natural language queries and find semantically similar medical concepts, procedures, and observations.

## Features

- **Interactive GUI**: Built with Marimo for a responsive interface
- **Vector Search**: Semantic search capabilities using sentence transformers
- **OMOP Integration**: Direct integration with OMOP CDM databases
- **Natural Language Queries**: Search using plain English descriptions

## Prerequisites

- Python 3.12 or higher
- PostgreSQL database with pgvector extension
- OMOP CDM database with precomputed embeddings
- uv package manager

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/health-Informatics-UoN/quick-vector-search
   cd quick-vector-search
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Install the package in development mode:**
   ```bash
   uv pip install -e .
   ```

## Configuration

There are defaults for database connection details.

```env
DB_HOST="localhost"
DB_PORT=5432
DB_USER="postgres"
DB_PASSWORD="password"
DB_NAME="omop"
DB_SCHEMA="cdm"
DB_VECTABLE="embeddings"
EMBEDDINGS_MODEL="baai/bge-small-en-v1.5"
```

If you need to change any of these to match your database, then create a `.env` file in the project root with your database connection details.

## Usage

### Starting the UI

Launch the vector search interface:

```bash
uv run vsui
```

This will start the Marimo interface where you can enter natural language search queries.

### Project Structure

```
quick-vector-search/
│   ├── db/              # Database connection and queries
│   ├── settings/        # Configuration management
│   ├── vector_search.py  # Main UI application
│   └── run_vs_ui.py     # Entry point script
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## Development

### Adding New Features

1. **Database operations**: Add new queries in `quick_vector_search/db/`
2. **UI components**: Modify `quick_vector_search/vector_search.py`
3. **Configuration**: Update settings in `quick_vector_search/settings/`

### Code Quality

The project includes Ruff for linting and formatting:

```bash
uv run ruff check
uv run ruff format
```

## Requirements

- Your OMOP database should have embeddings precomputed and stored
- PostgreSQL must have the pgvector extension installed
- Sufficient memory for loading sentence transformer models

## Troubleshooting

### Common Issues

1. **Database Connection**: Ensure PostgreSQL is running and pgvector extension is installed
2. **Memory Issues**: Sentence transformer models can be memory-intensive
3. **Missing Embeddings**: Verify that your OMOP database includes embedded vectors

### Getting Help

- Check the Marimo documentation for UI-related issues
- Verify your database schema matches OMOP CDM standards
- Ensure pgvector extension is properly configured

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request


## Acknowledgments

- Built on the OMOP Common Data Model
- Uses the Marimo reactive notebook framework
- Powered by Hugging Face sentence transformers
