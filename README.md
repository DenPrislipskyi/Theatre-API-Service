# Theatre-API-Service

#### This API serves as an online platform for visitors of the local theatre to make reservations and select seats without physically visiting the theatre.

#### DB Structure
![DB Structure](photo_readme/DB_strucrture.png)

## Features
- **CRUD Operations**: Perform Create, Read, Update, and Delete operations.
- **JWT Authentication**: Secure endpoints with JSON Web Token authentication.
- **Granular Permissions**: Fine-grained permissions ensure controlled access.
- **Play and Performance Filtering**: Streamline searches based on plays and performances.
- **Comprehensive Documentation**: Extensive documentation available for developers.
- **Admin Panel**: Intuitive administration interface for managing the API.
- **Pagination**: Divides data, simplifies navigation, enhances accessibility


### Installation & Run in Docker

Clone the repository:
```
git clone https://github.com/DenPrislipskyi/Theatre-API-Service.git
```
Ensure that the Python environment is set up:

For macOS:
```
python3 -m venv venv
```
```
source venv/bin/activate
```

For windows:
```
python -m venv venv
```
```
source venv/scripts/activate
```

Create a `.env` file and add the following configurations using the command:

For macOS:
```
cp .env-sample .env
```

For windows:
```
copy .env-sample .env
```

Once everything is set up, proceed to run the application using Docker Compose:
```
docker-compose up --build
```

You can use following superuser (or create another one by yourself)
```
email: admin@admin.com
password: admin
```

### Go to site: http://127.0.0.1:8000/api/theatre/

### **Documentation**
#### http://127.0.0.1:8000/api/doc/swagger/

![Swagger](photo_readme/Swagger.png)

### [**API**](http://127.0.0.1:8000/api/theatre/)
![API_page](photo_readme/API.png)
