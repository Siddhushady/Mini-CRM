# Mini CRM (Simple Demo)

## Automated CI/CD Deployment Workflow

This Mini CRM web application follows a fully automated CI/CD (Continuous Integration and Continuous Deployment) pipeline. Any changes pushed to the source code are automatically built, deployed, and made available to users without manual intervention.

### Workflow

1. **Developer Pushes Code to GitHub**
   - The developer implements new features, bug fixes, or enhancements.
   - The updated code is committed and pushed to the GitHub repository.

2. **Jenkins CI/CD Pipeline**
   - Jenkins continuously monitors the GitHub repository for new commits.
   - Once a code change is detected, Jenkins automatically triggers the CI/CD pipeline.
   - The pipeline performs the following tasks:
     - Pulls the latest source code from the GitHub repository.
     - Builds a new Docker image containing the updated application.
     - Tags the Docker image with the latest version.
     - Pushes the updated Docker image to the configured container registry (if applicable).
     - Updates the Kubernetes deployment with the newly built Docker image.

3. **Kubernetes Container Orchestration**
   - Kubernetes detects that a newer Docker image is available.
   - It gradually replaces the existing application containers with new containers running the updated image.
   - Rolling updates ensure minimal downtime while maintaining application availability throughout the deployment.

4. **AWS Infrastructure Provisioning**
   - Terraform provisions and manages the required AWS infrastructure, including EC2 instances, networking resources, and supporting cloud components.
   - Ansible automates the configuration and deployment of the application on the provisioned infrastructure.
   - Once Kubernetes deploys the latest Docker image, the infrastructure managed through Terraform and Ansible ensures that the updated application is served from the AWS EC2 instance.

5. **Application Updated**
   - The deployment completes automatically.
   - Users accessing the Mini CRM web application are immediately served the latest version without requiring any manual deployment.

---

## Run Locally (Without Docker)

### 1. Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate      # Linux/macOS
# or
.venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

### 2. Initialize the database

```bash
python init_db.py
```

### 3. Start the application

```bash
python app.py
```

### 4. Open the application

Visit:

```
http://localhost:5000
```

---

## Run with Docker

### 1. Build and start the containers

```bash
docker compose up --build
```

### 2. Open the application

Visit:

```
http://localhost:5000
```

---

## Useful Endpoints

| Endpoint | Description |
|----------|-------------|
| `/` | Dashboard |
| `/leads` | View all leads |
| `/lead/add` | Add a new lead |
| `GET /api/leads` | Retrieve all leads (REST API) |
| `POST /api/leads` | Create a new lead (REST API) |
| `POST /automation/run` | Execute automation workflow |
| `GET /api/automation/preview` | Preview automation changes without committing them |
