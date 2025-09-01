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


## Architecture Overview

The IT Support Agent follows a modular architecture:

1. **API Layer**: FastAPI endpoint for chat
2. **Service Layer**: Business logic for chat processing and tool orchestration  
3. **Tool Layer**: Specialized handlers for knowledge base, guides, and tickets
4. **Data Layer**: Vector database for semantic search, custom database server for user management and data operations
5. **Prompt Layer**: Dynamic prompt building, user context integration (User Profile), database issue categories for LLM classification in RAG tool filtering, and workflow instructions
6. **AI Layer**: HuggingFace integration for natural language processing

This architecture enables scalable, maintainable AI-powered IT support automation.



## Project Structure

The following structure shows **only** the files I added to implement the IT support agent functionality:

**NOTE**: There are other files in the project that were part of the original template, but the files listed below are specifically what I implemented for the IT support agent functionality.

```
app/                                  # Main application package
├── api/                              # API endpoints
│   └── chat.py                       # Chat endpoint for AI-powered support requests
├── core/                             # Core configuration and utilities
│   ├── config/                       # YAML configuration files
│   │   ├── app.yaml                 # Application settings and parameters
│   │   ├── llm.yaml                 # LLM model configuration (model selection , decoding parameters selelection :                                      temperature - topk )
│   │   ├── embedding.yaml           # Embedding model settings (embedding model configuration)
│   │   ├── tools.yaml               # Tool definitions for AI function  
│   │   └── prompt.yaml              # AI prompt templates and system messages 
├── db/                               # Data layer
│   ├── qdrant_client.py             # Vector database client for semantic search
│   └── fetch_data.py                # Data operations from external database
├── llm/                              # Language model integration
│   └── hf_client.py                 # HuggingFace client for LLM inference (potentially more client can be added with a unified    interface)
├── schemas/                          # Pydantic schemas
│   └── chat.py                      # Chat request/response data models
├── services/                         # Business logic layer
│   ├── chat_service.py              # Main chat processing and AI orchestration
│   ├── indexer.py                   # Document indexing for vector search
│   ├── prompt.py                    # AI prompt management and templating
│   ├── response_formatter.py        # Formats fetched data from external sources to be used by the llm
│   ├── tool_dispatcher.py           # Tool calling dispatcher for AI functions (Routes invoked function by the llm to the appropriate handler)
│   ├── tools.py                     # Tool definitions 
│   └── tool_handlers/               # Intelligent response processing, relevance filtering, conversation management, error handling, and user experience optimization 
│       ├── knowledge_base.py        # Knowledge base search handler
│       ├── guide_issue.py           # Issue guide handler
│       └── ticket.py                # Ticket management handler
└── utils/                            # Utility functions
    └── yaml_loader.py               # YAML configuration file loader utility
```



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
| `HF_API_BASE` | Hugging Face API base URL | `https://api-inference.huggingface.co` | Yes |
| `QDRANT_URL` | Qdrant vector database URL | `http://localhost:6333` | Yes |
| `QDRANT_API_KEY` | Qdrant API key (for cloud) | - | Yes |
| `DB_URL` | External IT Database URL | `https://it-supportdatabase-1.onrender.com/` | Yes |

### Important: Hugging Face Token Requirements

**Critical**: When creating your Hugging Face API token, you **MUST** ensure it has permission to access **Inference API providers**. This permission is essential for the LLM integration to work properly.

**Steps to create a token with correct permissions:**
1. Go to [Hugging Face Settings > Access Tokens](https://huggingface.co/settings/tokens)
2. Click "New token"
3. Give your token a name (e.g., "IT-Support-Agent")
4. **IMPORTANT**: Set the role to "Write" and ensure "Inference API" is checked
5. Click "Generate token"
6. Copy the token and add it to your `.env` file as `HF_TOKEN=your_token_here`

**Why this matters**: Without Inference API provider permissions, the system cannot access the language models needed for AI-powered support responses.


### External Database API Reference

The `DB_URL` environment variable should point to an external hosted FastAPI server on Render that provides access to **Tickets**, **Users**, **Knowledge Base Examples**, **Issues Guide Cases** stored in the IT Support database.

**Note**: The default `DB_URL` points to a custom server I created that simulates an IT company's support database based on HP support data. You can either use this default URL or create your own database server following the API reference below.

#### Base URL Format
```
http://localhost:3000  # for local development
https://your-app-name.onrender.com  # for hosted service on Render
```

#### Available Resources

**1. Tickets** - Support tickets created by users
```json
{
    "id": "TICKET-007",
    "user": "user-123",
    "description": "User experiencing blue screen issue; initial KB steps did not resolve.",
    "status": "open"
}
```

**2. Users** - Users who can create tickets
```json
{
  "id": "USER-001",
  "name": "Alice Johnson",
  "email": "alice.johnson@example.com",
  "device_type": "Laptop",
  "product_model": "HP Pavilion x360",
  "os_version": "Windows 11",
  "location": "New York",
  "past_tickets": [
    "TICKET-001"
  ]
}
```

**3. Issues** - Issue Guide 
```json
{
  "id": "GUIDE-011",
    "category": "Printer",
    "issue_code": "PR-002",
    "issue": "Printer prints blank pages",
    "diagnostic_questions": [
      "Are the ink/toner levels sufficient?",
      "Have the protective seals been removed from the cartridges?",
      "Was a cleaning cycle performed?"
    ],
    "troubleshooting_steps": [
      "Check ink/toner levels via software or display",
      "Ensure cartridges are correctly installed and unsealed",
      "Run the printer's head cleaning utility",
      "Print a nozzle check or test page"
    ],
    "quick_fixes": [
      "Replace empty cartridges",
      "Gently shake the toner cartridge"
    ],
    "escalation_criteria": "Escalate if cleaning cycles do not resolve the issue",
    "ticketing_fields": [
      "Issue summary",
      "Printer model",
      "Cartridge type",
      "Steps attempted"
    ],
    "kb_links": [
      "https://h30434.www3.hp.com/t5/Printers-Knowledge-Base/Blank-Pages/td-p/44567"
    ]
}
```
**3. Knowledge Base** - Knowledge Base
```json
{
  {
    "id": "KB-011",
    "category": "Software",
    "issue_code": "SW-002",
    "question": "HP Smart app cannot find my printer",
    "answer": "If HP Smart cannot find your printer:\n1. Ensure printer and computer are on the same Wi-Fi network.\n2. Restart your printer, computer, and Wi-Fi router.\n3. Make sure the printer is not in sleep mode.\n4. Temporarily disable any VPN or firewall.\n5. Re-add the printer in the HP Smart app.\nFor more info: Click here.",
    "tags": [
      "software",
      "hp smart",
      "discovery"
    ],
    "source_url": "https://h30434.www3.hp.com/t5/Software-FAQ/HPSmart-Discovery/td-p/88991"
  }
}
```

#### Key Endpoints
- `GET /` - Health check and API status
- `GET /kb` - Retrieve all knowledge base articles
- `GET /kb/{id}` - Retrieve specific knowledge base article by ID
- `GET /guide` - Retrieve all issue guides
- `GET /user` - Retrieve all users
- `GET /user/{user_id}` - Retrieve specific user by ID
- `GET /tickets` - Retrieve all tickets
- `GET /tickets/{user_id}` - Retrieve tickets for a specific user
- `POST /tickets/{user_id}` - Create new ticket

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
        "role": "user",
        "content": "My computer wont connect to WiFi"
      },
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
- **Embedding Model**: `sentence-transformers/all-mpnet-base-v2` ( default, can be changed in embedding config file) 
- **Vector Database**: Qdrant with HNSW indexing for fast similarity search
- **Indexing Process**: Runs automatically on backend startup, indexing all documents from the connected external database
- **Future Enhancement**: An endpoint can be created to synchronize the vector database when the external database is updated, ensuring real-time data consistency

### AI Models
- **LLM**: `mistralai/Mistral-7B-Instruct-v0.3`(default,  can be changed in llm config file)
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

