# Service Registry Platform
> A microservices service registry and discovery system built with FastAPI. 
> Services can register themselves, be discovered by other services, and provide health status.

## Provisions
- **Service Registration**: Services register with name, URL, version, and health endpoint
- **Service Discovery**: Query for specific services by name
- **Health Checks**: Platform and service health monitoring
- **RESTful API**: Simple HTTP endpoints for all operations

## Architecture
```lua
┌─────────────┐
│   Service   │──register──▶┌──────────────┐
│   (Client)  │             │   Registry   │
└─────────────┘◀──discover──│   Platform   │
                            └──────────────┘
                                   │
                            ┌──────▼──────┐
                            │  Database   │
                            └─────────────┘
```

### Tech
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **Python 3.10+** - Programming language

### Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register a new service |
| GET | `/services` | List all registered services |
| GET | `/services/{name}` | Get specific service details |
| DELETE | `/services/{name}` | Deregister a service |
| GET | `/health` | Platform health check |
| GET | `/discover/{name}` | Service discovery lookup |

## Run locally

### Prereqs
- Python 3.10 or higher
- pip (Python package manager)

### Setup
1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/service-registry-platform.git
   cd service-registry-platform
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Register a service
```bash
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "user-service",
    "url": "http://localhost:3000",
    "version": "1.0.0",
    "health_endpoint": "/health"
  }'
```

### Discover a service
```bash
curl http://localhost:8000/discover/user-service
```

### Check platform health
```bash
curl http://localhost:8000/health
```



## 🔗 Links

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Service Registry Pattern](https://microservices.io/patterns/service-registry.html)
