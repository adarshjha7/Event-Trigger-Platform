# Event Trigger Platform

## Overview

The Event Trigger Platform is a Flask-based application designed to manage and trigger events based on predefined schedules or API calls. It allows users to create, manage, and trigger events, log their occurrences, and clean up old logs. The platform supports both scheduled triggers (fixed time or interval) and API triggers.

## Features

- **Scheduled Triggers**: Create triggers that fire at a specific time or at regular intervals.
- **API Triggers**: Create triggers that can be fired manually via an API call.
- **Event Logging**: Log every trigger event with details such as trigger ID, timestamp, payload, and state.
- **Cleanup**: Automatically clean up event logs older than 48 hours.
- **Dockerization**: Easily deploy the application using Docker.
- **Swagger UI**: Interactive API documentation for easy testing and exploration.

## Features I couldn't implement due to time constraints
  Deployment on Cloud.
  
  Implement an active/archived state system .

## Project Structure

- **app/**: Contains the main application code.
  - **job_scheduler.py**: Handles scheduling and triggering of events.
  - **models.py**: Defines the database models for triggers and event logs.
  - **routes.py**: Defines the API endpoints.
- **run.py**: The entry point for running the Flask application.
- **Dockerfile**: Instructions for building a Docker image of the application.
- **requirements.txt**: Lists all Python dependencies.

## Setup and Installation

### Prerequisites

- Python 3.9
- Docker (optional)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/event-trigger-platform.git
   cd event-trigger-platform
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python run.py
   ```

### Docker Installation

1. **Build the Docker image**:
   ```bash
   docker build -t event-trigger-platform .
   ```

2. **Run the Docker container**:
   ```bash
   docker run -p 5000:5000 event-trigger-platform
   ```

## API Endpoints

### Swagger UI

To explore and test the API endpoints, navigate to the Swagger UI at:
```
http://localhost:5000/swagger-ui
```

### Endpoints

1. **Create a new API trigger**
   - **POST** `/api/triggers`
   - **Request Body**:
     ```json
     {
       "api_endpoint": "string",
       "payload": {},
       "is_test": boolean
     }
     ```
   - **Response**:
     ```json
     {
       "message": "API trigger created successfully",
       "id": integer
     }
     ```

2. **Create a new scheduled trigger**
   - **POST** `/scheduled/triggers`
   - **Request Body**:
     ```json
     {
       "schedule_type": "fixed_time" or "fixed_interval",
       "schedule_value": "string",
       "is_recurring": boolean,
       "payload": {},
       "is_test": boolean
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Scheduled trigger created successfully",
       "id": integer
     }
     ```

3. **List all triggers**
   - **GET** `/triggers`
   - **Response**:
     ```json
     {
       "triggers": [
         {
           "id": integer,
           "type": "string",
           "schedule_type": "string",
           "schedule_value": "string",
           "is_recurring": boolean,
           "api_endpoint": "string",
           "payload": {},
           "is_test": boolean
         }
       ]
     }
     ```

4. **Manually trigger a trigger**
   - **POST** `/triggers/{trigger_id}/test`
   - **Response**:
     ```json
     {
       "message": "Trigger fired manually for testing"
     }
     ```

5. **List all event logs**
   - **GET** `/event_logs`
   - **Response**:
     ```json
     {
       "logs": [
         {
           "id": integer,
           "trigger_id": integer,
           "triggered_at": "string",
           "payload": {},
           "is_test": boolean,
           "state": "string"
         }
       ]
     }
     ```

6. **Edit a trigger**
   - **PUT** `/triggers/{trigger_id}`
   - **Request Body**:
     ```json
     {
       "type": "string",
       "schedule_type": "string",
       "schedule_value": "string",
       "is_recurring": boolean,
       "api_endpoint": "string",
       "payload": {},
       "is_test": boolean
     }
     ```
   - **Response**:
     ```json
     {
       "message": "Trigger updated successfully",
       "id": integer
     }
     ```

## Database

The application uses SQLite as the database. The database file is automatically created when the application is run for the first time.

## Job Scheduler

The job scheduler is responsible for managing and triggering scheduled events. It uses APScheduler to handle cron jobs and interval-based jobs.

### Key Functions

- **trigger_event**: Logs an event when a trigger fires.
- **schedule_trigger**: Schedules a trigger based on its type and schedule.
- **cleanup_old_logs**: Cleans up event logs older than 48 hours.

## Dockerization

The application is Dockerized for easy deployment. The Dockerfile sets up the environment, installs dependencies, and runs the application.

### Docker Commands

- **Build the image**:
  ```bash
  docker build -t event-trigger-platform .
  ```

- **Run the container**:
  ```bash
  docker run -p 5000:5000 event-trigger-platform
  ```

## Testing

You can test the application using the Swagger UI or by making direct API calls using tools like Postman or cURL.

## Conclusion

The Event Trigger Platform is a robust solution for managing and triggering events based on schedules or API calls. It provides a comprehensive set of features, including event logging, cleanup, and Docker support, making it easy to deploy and manage. The Swagger UI offers an interactive way to explore and test the API endpoints, ensuring a smooth development and testing experience.

## References
  https://youtu.be/_COyD1CExKU?si=UR9PqEYqnPHNs8M0
  https://youtu.be/ng8L5n6r4kw?si=0cri5MgeFieluA_1
  https://www.deepseek.com/

## Proof of Work

![Screenshot (16)](https://github.com/user-attachments/assets/64d3877b-13d6-4790-b00f-926574ccf12a)

![Screenshot (17)](https://github.com/user-attachments/assets/6883542f-8abb-4fd6-b582-2ad014a7d401)

![Screenshot (19)](https://github.com/user-attachments/assets/9f7980dd-8163-4d9f-bb0f-85cd7feec141)

![Screenshot (18)](https://github.com/user-attachments/assets/d884f488-29c7-4a53-8a4d-257ca225bde1)

