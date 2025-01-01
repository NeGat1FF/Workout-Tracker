# Workout API

## Overview

Wokrout API is a FastAPI-based application that allows users to manage their workouts, exercises, and workout reports. The application provides endpoints for user registration, login, workout management, workout reports, and scheduling workouts.

## Features

- User registration and authentication
- CRUD operations for workouts
- CRUD operations for exercises
- Scheduling workouts
- Generating workout reports

## Getting Started

### Prerequisites

- Python 3.12
- Docker
- Docker Compose

### Installation

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create a *.env* file based on the *.env.example*:
    ```sh
    cp .env.example .env
    ```

3. Update the *.env* file with your JWT secret.

4. Build and run the Docker containers:
    ```sh
    docker-compose up --build
    ```

### Running the Application

The application will be available at `http://localhost:8000`.

### API Documentation

The API documentation is available at `http://localhost:8000/docs`.

## Running Migrations

Migrations are automatically applied when the application starts. You can find the migration files in the *migrations* directory.

## Seeding the Database

The database is seeded with initial data using the *seeder.py* script. This script is automatically run when the application starts.


[](https://roadmap.sh/projects/fitness-workout-tracker)