Thank you for providing those clarifications. I'll now generate a comprehensive prompt based on all the information you've shared, incorporating your specific requirements and preferences.

---

## Comprehensive Prompt for Code Prompt Pro

### Project Overview

Create a full-stack web application called "Code Prompt Pro" that assists non-technical users in generating technical prompts for AI-powered IDEs. The application will use Anthropic's Claude 3.5 for AI functionalities and Supabase for storing metaprompts.

---

### Frontend Development

```typescript
// Sample React component structure
import React from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { TextField, Button } from '@material-ui/core';

const PromptGenerator: React.FC = () => {
  // Component logic here
}
```

#### Key Components:
- Implement a user-friendly interface with an interactive questionnaire
- Create a prompt customization interface
- Develop an export functionality for generated prompts (focus on Markdown format)
- Ensure responsive design for cross-device compatibility

#### Technical Stack:
- **Framework:** React with TypeScript
- **State Management:** Redux Toolkit
- **UI Library:** Material-UI
- **Routing:** React Router
- **Form Handling:** React Hook Form
- **HTTP Client:** Axios
- **Styling:** CSS Modules
- **Testing:** Jest and React Testing Library
- **Build Tool:** Webpack

---

### Backend Development

```python
# Sample Flask route
from flask import Flask, request, jsonify
from .services import generate_prompt

app = Flask(__name__)

@app.route('/generate-prompt', methods=['POST'])
def create_prompt():
    user_input = request.json
    generated_prompt = generate_prompt(user_input)
    return jsonify({"prompt": generated_prompt})
```

#### Key Features:
- Implement RESTful API endpoints for prompt generation and management
- Integrate with Anthropic's Claude 3.5 API for AI functionalities
- Set up Supabase connection for storing and retrieving metaprompts

#### Technical Stack:
- **Language:** Python 3.x
- **Framework:** Flask
- **Database:** Supabase (PostgreSQL)
- **ORM:** SQLAlchemy with Alembic for migrations
- **API Documentation:** Swagger UI using OpenAPI specifications
- **Testing:** Pytest
- **Linting and Formatting:** Flake8 and Black

---

### Database and Storage

- Use Supabase (PostgreSQL) for storing metaprompts and user data
- Implement efficient querying and indexing for optimal performance
- Set up regular automated backups

---

### Containerization and Infrastructure

```dockerfile
# Sample Dockerfile for backend
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-b", "0.0.0.0:5000", "wsgi:app"]
```

- Create Dockerfiles for both frontend and backend
- Develop a `docker-compose.yml` for local development
- Write Terraform scripts for future Linode deployment

---

### Environment Management

- Use `.env` files with `dotenv` for managing environment variables
- Implement separate configurations for development, staging, and production
- Use git-crypt for encrypting sensitive files

---

### Makefile

```makefile
# Sample Makefile targets
install:
    @echo "Installing dependencies..."
    cd frontend && npm install
    cd backend && pip install -r requirements.txt

build:
    @echo "Building the application..."
    cd frontend && npm run build
    cd backend && python setup.py build

start:
    @echo "Starting the application..."
    docker-compose up

test:
    @echo "Running tests..."
    cd frontend && npm test
    cd backend && pytest

deploy:
    @echo "Deploying the application..."
    # Add deployment commands here

help:
    @echo "Available commands:"
    @echo "  make install  - Install dependencies"
    @echo "  make build    - Build the application"
    @echo "  make start    - Start the application locally"
    @echo "  make test     - Run all tests"
    @echo "  make deploy   - Deploy the application"
```

---