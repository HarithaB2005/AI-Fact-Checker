# AI Fact Checker

## Project Overview
AI Fact Checker is an advanced tool designed to help users verify the authenticity of information and claims made online. By utilizing cutting-edge algorithms, this project aims to provide fast and reliable fact-checking services.

## Features
- Automated fact check for claims
- User-friendly interface
- Supports multiple languages
- Integration with external APIs for data verification

## Tech Stack
- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python

## Architecture
The project follows a microservices architecture, where the frontend and backend interact through RESTful APIs.

## Setup Instructions
### Python Virtual Environment
1. Install virtualenv: `pip install virtualenv`
2. Create a virtual environment: `virtualenv venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`

### Dependency Installation
After activating the virtual environment, install the necessary dependencies:
`pip install -r requirements.txt`

### Environment Variables
Ensure to configure the necessary environment variables for API keys and database connections as per the `.env.example` file.

## Usage Steps
1. Clone the repository: `git clone https://github.com/Premananda9/AI-Fact-checker.git`
2. Navigate to the project directory: `cd AI-Fact-checker`
3. Follow the setup instructions above.
4. Run the application: `python app.py`

## API/Route Documentation
- **GET /api/facts**: Retrieve verified facts
- **POST /api/facts/check**: Submit a claim for verification

## Contributing Guidelines
1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch`
3. Implement your feature or fix a bug.
4. Submit a pull request.

## Security/Privacy Notes
- All user images and data are handled with strict confidentiality.
- Ensure to follow best practices for data security and user privacy.

## Roadmap
- [ ] Implement additional language support
- [ ] Enhance the AI algorithms for fact-checking
- [ ] Improve the user interface design

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact Information
For any queries or support, please reach out to me at @Premananda9
