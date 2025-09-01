# IT Support Agent

An AI-powered virtual assistant designed to help users solve technical problems on their devices or software through step-by-step troubleshooting guidance, automated diagnostics, and intelligent ticket management.

## Features

- **AI-Powered Support**: Intelligent problem resolution using natural language processing and machine learning
- **Knowledge Base Integration**: Quick access to FAQs and troubleshooting guides via semantic search
- **Guided Diagnostics**: Structured question-based troubleshooting for complex technical issues
- **Multi-Level Support Workflow**: Automated Level 0/1 support with intelligent escalation to Level 2
- **Vector Search**: Fast similarity search using Qdrant and sentence transformers
- **Hugging Face LLM Integration**: Advanced language model capabilities using Mistral-7B-Instruct-v0.3
- **Tool Calling System**: Dynamic function calling for knowledge base queries, issue guides, and ticket management
- **Async Database Operations**: Efficient data handling with SQLAlchemy and PostgreSQL/SQLite
- **Docker Support**: Containerized deployment for development and production environments
- **Real-time Chat Interface**: RESTful API for seamless integration with chat applications

## How It Works

The IT Support Agent operates on a sophisticated multi-level workflow:

### Level 0 (Self-Service)
- User describes their problem in natural language
- AI searches the knowledge base for similar issues and solutions
- If a solution is found, the ticket is automatically closed with the resolution

### Level 1 (Guided Support) 
- If no direct solution is found, the AI provides guided troubleshooting steps
- Uses structured issue guides with step-by-step instructions
- Covers common problems like WiFi connectivity, software installation, hardware issues

### Level 2 (Human Escalation)
- For unresolved complex issues, the system creates support tickets
- Escalates to human technicians with complete problem context
- Tracks ticket status and provides updates to users

## Architecture Overview

The IT Support Agent follows a modular architecture:

1. **API Layer**: FastAPI endpoints for authentication and chat
2. **Service Layer**: Business logic for chat processing and tool orchestration  
3. **Tool Layer**: Specialized handlers for knowledge base, guides, and tickets
4. **Data Layer**: Vector database for semantic search, SQL database for users
5. **AI Layer**: HuggingFace integration for natural language processing

This architecture enables scalable, maintainable AI-powered IT support automation.

---

**Built with**: FastAPI, HuggingFace Transformers, Qdrant, Docker


## Project Structure

The following structure shows **only** the files I added to implement the IT support agent functionality:

```
app/                                  # Main application package
├── api/                              # API endpoints
│   └── chat.py                       # Chat endpoint for AI-powered support requests
├── core/                             # Core configuration and utilities
│   ├── config/                       # YAML configuration files
│   │   ├── app.yaml                 # Application settings and parameters
│   │   ├── llm.yaml                 # LLM model configuration (Mistral-7B-Instruct-v0.3)
│   │   ├── embedding.yaml           # Embedding model settings (sentence-transformers)
│   │   ├── tools.yaml               # Tool definitions for AI function calling
│   │   └── prompt.yaml              # AI prompt templates and system messages
│   └── config.py                    # Main configuration loader and settings
├── db/                               # Data layer
│   ├── qdrant_client.py             # Vector database client for semantic search
│   └── fetch_data.py                # Data fetching operations from external database
├── llm/                              # Language model integration
│   └── hf_client.py                 # HuggingFace client for LLM inference
├── schemas/                          # Pydantic schemas
│   └── chat.py                      # Chat request/response data models
├── services/                         # Business logic layer
│   ├── chat_service.py              # Main chat processing and AI orchestration
│   ├── indexer.py                   # Document indexing for vector search
│   ├── prompt.py                    # AI prompt management and templating
│   ├── response_formatter.py        # Response formatting and structure
│   ├── tool_dispatcher.py           # Tool calling dispatcher for AI functions
│   ├── tools.py                     # Tool definitions and utility functions
│   └── tool_handlers/               # Specific tool implementations
│       ├── knowledge_base.py        # Knowledge base search handler
│       ├── guide_issue.py           # Issue guide handler
│       └── ticket.py                # Ticket management handler
└── utils/                            # Utility functions
    └── yaml_loader.py               # YAML configuration file loader utility
```

## Requirements

- Python 3.11+
- Docker (optional, recommended)
- Hugging Face API key (for LLM integration)
- Qdrant vector database (can run in Docker)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd IT-support-agent
   ```

2. Create a `.env` file with your configuration:
   ```bash
   # Required environment variables
   HF_TOKEN=your-huggingface-api-token
   HF_API_BASE=https://api-inference.huggingface.co
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=your-qdrant-api-key  # if using Qdrant Cloud
   DB_URL=http://your-ticket-system-api  # for ticket integration
   ```



3. Start the application with Docker Compose:
   ```bash
   # For development (with hot-reload)
   docker-compose -f docker-compose.dev.yml up --build

   # For production
   docker-compose up --build
   ```

4. The API will be available at http://localhost:8000

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd IT-support-agent
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables (create a `.env` file):
   ```bash
   # AI/ML Configuration
   HF_TOKEN=your-huggingface-api-token
   HF_API_BASE=https://api-inference.huggingface.co

   # Vector Database
   QDRANT_URL=http://localhost:6333
   QDRANT_API_KEY=your-qdrant-api-key

   # Ticket System Integration
   DB_URL=http://your-ticket-system-api

   # Development Settings
   DEBUG=true
   ```



5. Start the application:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

7. The API will be available at http://localhost:8000



## API Documentation

Once the application is running, you can access:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## API Endpoints

### Chat & Support
- `POST /chat` - Submit a technical problem for AI assistance
  - Accepts natural language problem descriptions
  - Returns AI-powered troubleshooting guidance
  - Automatically handles tool calling for knowledge base search, guides, and tickets

### System
- `GET /health` - Health check endpoint

## Configuration

The application is configured through environment variables set in a `.env` file:

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `HF_TOKEN` | Hugging Face API token for LLM access | - | Yes |
| `HF_API_BASE` | Hugging Face API base URL | `https://api-inference.huggingface.co` | No |
| `QDRANT_URL` | Qdrant vector database URL | `http://localhost:6333` | Yes |
| `QDRANT_API_KEY` | Qdrant API key (for cloud) | - | No |
| `DB_URL` | External ticket system API URL | `https://it-supportdatabase-1.onrender.com/` | Yes |
| `DEBUG` | Enable debug mode | `true` | No |

### External Database API Reference

The `DB_URL` environment variable should point to an external hosted FastAPI server on Render that provides access to **Tickets**, **Users**, and **Issues** stored in the IT Support database.

#### Base URL Format
```
http://localhost:3000  # for local development
https://your-app-name.onrender.com  # for hosted service on Render
```

#### Available Resources

**1. Tickets** - Support tickets created by users
```json
{
  "id": "TICKET-001",
  "user": "user1",
  "issue_code": "PR-001",
  "description": "Printer jammed when printing",
  "status": "open"
}
```

**2. Users** - Users who can create tickets
```json
{
  "id": "user1",
  "name": "John Doe",
  "email": "john@example.com"
}
```

**3. Issues** - Types of issues
```json
{
  "code": "PR-001",
  "name": "Printer Issue"
}
```

#### Key Endpoints
- `GET /tickets` - Retrieve all tickets
- `POST /tickets` - Create new tickets
- `GET /users` - Retrieve all users
- `GET /issues` - Retrieve all issue types

### Qdrant Vector Database Setup

The `QDRANT_URL` and `QDRANT_API_KEY` environment variables configure the vector database for semantic search.

#### Option 1: Local Qdrant (Recommended for development)
- Use `QDRANT_URL=http://localhost:6333` (default)
- No API key required for local setup
- Qdrant will be started automatically via Docker Compose

#### Option 2: Qdrant Cloud (Recommended for production)
- Sign up at [cloud.qdrant.io](https://cloud.qdrant.io)
- Create a new cluster
- Get your cluster URL from the dashboard (format: `https://your-cluster-id.us-east-1-0.aws.cloud.qdrant.io:6333`)
- Generate an API key in the API Keys section
- Set `QDRANT_URL` to your cluster URL and `QDRANT_API_KEY` to your generated key

## Usage Examples

### Basic Support Request

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "messages": [
      {
        "role": "user",
        "content": "My computer wont connect to WiFi"
      }
    ]
  }'
```

### Response Example
```json
{
  "user_id": "user123",
  "messages": [
    {
      "role": "assistant",
      "content": "I understand you're having trouble connecting to WiFi. Let me help you troubleshoot this issue.\n\nFirst, let's check some basic things:\n1. Make sure your WiFi is turned on\n2. Check if you're in range of your WiFi network\n3. Try restarting your computer\n\nIf these don't work, I can guide you through more advanced troubleshooting steps."
    }
  ]
}
```

## Data Processing

The system uses vector embeddings for efficient knowledge retrieval:

### Document Indexing
- **Knowledge Base**: FAQ articles and solutions converted to vectors
- **Issue Guides**: Troubleshooting procedures and step-by-step guides
- **Embedding Model**: `sentence-transformers/all-mpnet-base-v2` (768 dimensions)
- **Vector Database**: Qdrant with HNSW indexing for fast similarity search

### AI Models
- **LLM**: `mistralai/Mistral-7B-Instruct-v0.3`
- **Parameters**: Configurable temperature, top_p, and max tokens
- **Tool Calling**: Function calling for dynamic knowledge retrieval and ticket creation

## Development

### Running Tests
```bash
pytest
```

### Code Quality Tools
The project uses several tools to ensure code quality:

- **Black**: Code formatter
- **isort**: Import sorter  
- **mypy**: Static type checking
- **pre-commit**: Git hooks for code quality checks

To set up pre-commit hooks:
```bash
pre-commit install
```

### Database Operations

#### Migrations
To create a new migration after changing models:
```bash
alembic revision --autogenerate -m "Description of changes"
```

To apply migrations:
```bash
alembic upgrade head
```

#### Supported Databases
- **SQLite**: Default for development (file-based)
- **PostgreSQL**: Recommended for production

## Docker Deployment

The project includes Docker configurations for both development and production:

- `docker-compose.yml`: Production setup with optimized settings
- `docker-compose.dev.yml`: Development setup with hot-reload and debugging
- `Dockerfile`: Multi-stage build with Python 3.11 slim base image

### Production Deployment
```bash
docker-compose up --build -d
```

### Development with Live Reload
```bash
docker-compose -f docker-compose.dev.yml up --build
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

