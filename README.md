# Microservice App Template

This repository provides a template for a microservice-based application using Python with FastAPI, RabbitMQ, PostgreSQL, Docker, Nginx, and New Relic. This template includes several services and is designed to be a starting point for a project.

## Project Structure

The project consists of the following services:

- **api-gateway**: Handles incoming requests and routes them to the the coordinator service.
- **coordinator-service**: Coordinates interactions between services.
- **auth-service**: Manages user authentication and authorization.
- **inventory-service**: Manages inventory-related operations.
- **product-service**: Handles product-related operations.

## Technology Stack

- **Python**: Programming language for the services.
- **FastAPI**: Modern web framework for building APIs with Python 3.7+.
- **RabbitMQ**: Message broker for asynchronous communication between services.
- **PostgreSQL**: Relational database for data storage.
- **Docker**: Containerization platform for running services.
- **Nginx**: Reverse proxy server with TLS support.
- **New Relic**: Performance monitoring and observability.

## Package Manager

This project uses [PDM](https://pdm.fming.dev/) as the package manager.

## Installation and Setup

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [PDM](https://pdm.fming.dev/) installed (for managing Python packages).

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/microservice-app-template.git
cd microservice-app-template
```

### 2. Install Dependencies

Install the Python dependencies using PDM:

```bash
pdm install
```

### 3. Set Up Environment Variables

Create a .env file in the root directory and add the required environment variables for New Relic and database configuration. Example:

```bash
NEW_RELIC_LICENSE_KEY=your_new_relic_license_key
DATABASE_URL=postgresql://user:password@localhost/dbname
RABBITMQ_URL=amqp://user:password@localhost:5672/
```

### 4. Configure Docker

The project includes a docker-compose.yml file to set up the services and infrastructure. Run the following command to start the services:

```bash
docker-compose up --build
```

### 5. Generate SSL Certificates

First, make the certificate generation script executable:

```bash
chmod +x script/gen.certs.sh
```

Then, run the script to generate SSL certificates for TLS:

```bash
./script/gen.certs.sh
```

### 6. Configure Nginx for TLS

Update the Nginx configuration files in the nginx directory to enable TLS. You will need to provide your SSL certificates and update the configuration accordingly.

### 7. Accessing Services

Once everything is up and running, you can access the services via the following URLs:
- API Gateway: http://localhost
- Auth Service: http://localhost/auth
- Coordinator Service: http://localhost/coordinator
- Inventory Service: http://localhost/inventory
- Product Service: http://localhost/product

## Notes

- This project is a template and may require modifications to suit your specific use case.
- For development purposes, you may need to adjust configurations and environment variables.

## Contributing
Feel free to fork this repository and submit pull requests. Contributions and suggestions are welcome!


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Documentation

For more information on each component, refer to their respective documentation:

- [FastAPI](https://fastapi.tiangolo.com/)
- [RabbitMQ](https://www.rabbitmq.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://docs.docker.com/)
- [Nginx](https://nginx.org/)
- [New Relic](https://newrelic.com/)