# SOCIAL APP

Welcome to the Social app repository! This project is a Django application that provides various APIs for a very basic social media app. To get started, follow the instructions below.

## Getting Started

### Prerequisites

- Docker
- Postman (optional for API testing)

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/sreesankarp/social_djangoapp_api.git
```

2. Navigate to the project directory:

```bash
cd social_djangoapp_api
```

3. Run the following command to start the application using Docker:

```bash
docker-compose up
```

Wait until the build finishes and the container is up and running.

4. Once the build is complete, you can access the Django app at [http://0.0.0.0:8000/](http://0.0.0.0:8000/).

### Testing APIs

You can test the APIs using Postman. Import the API collection provided in the repository to Postman to make it easier to test the available endpoints.

#### API Endpoints

- Signup: [http://0.0.0.0:8000/signup](http://0.0.0.0:8000/signup)
- Login: [http://0.0.0.0:8000/login](http://0.0.0.0:8000/login)
- Logout: [http://0.0.0.0:8000/logout](http://0.0.0.0:8000/logout)
- Search: [http://0.0.0.0:8000/search](http://0.0.0.0:8000/search)
- Send Request: [http://0.0.0.0:8000/sendrequest](http://0.0.0.0:8000/sendrequest)
- Accept Request: [http://0.0.0.0:8000/acceptrequest](http://0.0.0.0:8000/acceptrequest)
- Reject Request: [http://0.0.0.0:8000/rejectrequest](http://0.0.0.0:8000/rejectrequest)
- List Friends: [http://0.0.0.0:8000/listfriends](http://0.0.0.0:8000/listfriends)
- Pending Requests: [http://0.0.0.0:8000/pendingrequests](http://0.0.0.0:8000/pendingrequests)

#### Important Note

After creating a user using the signup API and calling the login API, make sure to add the `X-CSRFToken` to the headers for the subsequent API calls. You can find the CSRF token in the cookies of the login request.

For any additional details about the APIs, refer to the Postman collection provided in the repository.

Feel free to explore and contribute to this project! If you encounter any issues or have suggestions, please open an issue or submit a pull request.
