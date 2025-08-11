# Django Project Management System 🚀

A comprehensive project management application built with Django, featuring user management, project tracking, and administrative functionality.

## Features

- **Project Management**: Create, track, and manage projects
- **User Management**: Custom user system with role-based access
- **Admin Panel**: Enhanced administrative interface
- **Manager Dashboard**: Management tools and analytics
- **Responsive Design**: Mobile-friendly interface
- **Docker Support**: Containerized development and deployment

## Tech Stack

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL 15
- **Frontend**: HTML, CSS, JavaScript with Django Templates
- **Containerization**: Docker & Docker Compose
- **Web Server**: Gunicorn (production ready)

## Quick Start with Docker 🐳

### Prerequisites
- Docker and Docker Compose installed
- Git

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd Project_Management
```

### 2. Build and Run
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

### 3. Access Application
- **Main Application**: http://localhost:8000
- **Admin Panel**: http://localhost:8000/admin
- **Default Admin**: username: `admin`, password: `admin123`

### 4. Stop Services
```bash
docker-compose down
```

## Development Setup

### Docker Commands
```bash
# Start development server
docker-compose up

# View logs
docker-compose logs -f

# Access Django shell
docker-compose exec web python manage.py shell

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Collect static files
docker-compose exec web python manage.py collectstatic
```

### Local Development (Alternative)
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up database (PostgreSQL required)
export DATABASE_URL="postgres://user:password@localhost:5432/dbname"

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

## Project Structure

```
Project_Management/
├── adminpanel/          # Custom admin functionality
├── manager/             # Management tools and dashboards
├── projects/            # Project management app
├── users/               # Custom user management
├── project_manage/      # Main Django project settings
├── static/              # Static files (CSS, JS, images)
├── staticfiles/         # Collected static files
├── templates/           # HTML templates
├── media/               # User uploaded files
├── docker-compose.yml   # Docker services configuration
├── Dockerfile           # Docker image configuration
├── entrypoint.sh        # Docker entrypoint script
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

## Environment Variables

Create a `.env` file for environment-specific settings:

```bash
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL)
DATABASE_URL=postgres://postgres:postgres@db:5432/project_management

# Or individual database settings
DB_NAME=project_management
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

## Features Overview

### 🏗️ Project Management
- Create and manage projects
- Track project progress
- Assign team members
- Set deadlines and milestones

### 👥 User Management
- Custom user model
- Role-based permissions
- User profiles and authentication
- Team collaboration features

### 📊 Admin Panel
- Enhanced Django admin interface
- Custom admin views
- Data management tools
- System monitoring

### 🎛️ Manager Dashboard
- Project analytics
- Team performance metrics
- Resource allocation
- Reporting tools

## API Endpoints

The application provides various endpoints for different functionalities:

- `/admin/` - Django admin interface
- `/projects/` - Project management views
- `/users/` - User management
- `/manager/` - Management dashboard

## Testing

```bash
# Run tests in Docker
docker-compose exec web python manage.py test

# Run specific app tests
docker-compose exec web python manage.py test projects

# Run with coverage
docker-compose exec web coverage run manage.py test
docker-compose exec web coverage report
```

## Deployment

### Production Deployment
1. Set `DEBUG=False` in environment variables
2. Configure proper database credentials
3. Set up static file serving (Nginx)
4. Use environment-specific Docker compose file
5. Configure SSL/HTTPS
6. Set up monitoring and logging

### Environment Configuration
- **Development**: `docker-compose.yml`
- **Production**: `docker-compose.prod.yml` (create as needed)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## Troubleshooting

### Common Issues

**Docker containers won't start:**
```bash
# Check Docker is running
docker --version
docker-compose --version

# View logs
docker-compose logs
```

**Database connection issues:**
```bash
# Verify database container is healthy
docker-compose ps
docker-compose logs db
```

**Static files not loading:**
```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

**Permission issues:**
```bash
# Make entrypoint executable
chmod +x entrypoint.sh
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the GitHub repository
- Check the troubleshooting section above
- Review Docker and Django documentation

---

**Built with ❤️ using Django and Docker**