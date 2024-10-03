Thank you for providing the additional information. I'll now create a comprehensive prompt to guide the AI in building your Color Analysis X application. Here's the prompt:

---

## Project: Color Analysis X

### Project Description
Color Analysis X is a web application that captures multiple pictures of the user from their webcam, provides helpful hints and lighting tips for accurate results, and uses AI-powered analysis to give users a comprehensive color analysis.

---

### Key Features
1. Webcam integration for capturing 5 pictures per session
2. Real-time hints and lighting tips for optimal photo quality
3. AI-powered color analysis using OpenAI API through LangChain
4. Comprehensive color analysis results based on the 12-season color system
5. Sleek, modern, and easy-to-use UI with 3-4 main components

---

### Technical Requirements

#### Frontend
- Framework: React 3.0.1 with TypeScript
- Routing: React Router
- State Management: Context API
- Styling: Styled Components
- Testing: Jest and React Testing Library
- Linting and Formatting: ESLint and Prettier

#### Backend
- Language: Python 3.x
- Framework: Flask
- ORM: SQLAlchemy
- Serialization: Marshmallow
- Testing: Pytest
- Linting and Formatting: Flake8 and Black

#### Database
- PostgreSQL with SQLAlchemy ORM

#### API Integration
- OpenAI API through LangChain for multimodal data processing

#### Containerization
- Docker and Docker Compose

#### Infrastructure
- Terraform scripts for Linode provisioning

#### CI/CD
- GitHub Actions for automated testing and deployment

---

### Application Structure

```
project-root/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── WebcamCapture.tsx
│   │   │   ├── AnalysisResults.tsx
│   │   │   ├── TipsGuide.tsx
│   │   │   └── ProgressIndicator.tsx
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   └── Analysis.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── utils/
│   │   │   └── colorHelper.ts
│   │   ├── App.tsx
│   │   └── index.tsx
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── models/
│   │   ├── routes/
│   │   ├── services/
│   │   │   └── color_analysis.py
│   │   └── utils/
│   ├── tests/
│   ├── config.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile.frontend
├── Dockerfile.backend
├── terraform/
│   └── main.tf
├── .github/
│   └── workflows/
│       └── ci-cd.yml
└── Makefile
```

---

### Implementation Steps

1. Set up the project structure as outlined above.

2. Frontend Development:
   - Create a sleek, modern UI with the following main components:
     a. WebcamCapture: For taking 5 pictures of the user
     b. TipsGuide: To display helpful hints and lighting tips
     c. ProgressIndicator: To show the user's progress through the analysis process
     d. AnalysisResults: To display the comprehensive color analysis results
   - Implement webcam integration using a library like react-webcam
   - Create a state management system using Context API to handle the application's state
   - Implement client-side routing using React Router

3. Backend Development:
   - Set up a Flask application with SQLAlchemy ORM
   - Create necessary models and database schemas
   - Implement API endpoints for:
     a. Receiving and storing captured images
     b. Initiating the color analysis process
     c. Returning analysis results
   - Integrate with OpenAI API using LangChain for multimodal data processing

4. Color Analysis Implementation:
   - Use the provided comprehensive color analysis guide