## How to run the application

### To run the Backend application, follow the steps below:

1. Clone the repository
```bash
git clone https://github.com/Ankuraxz/nutrition_ai.git
```
2. Change the working directory
```bash
cd nutrition_ai/backend
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Run the application
```bash
uvicorn main:app --reload --port 8000
```
5. Open the browser and go to `http://localhost:8000`
6. You can now use the application



### To run the Frontend application, follow the steps below:

1. Clone the repository
```bash
git clone https://github.com/Ankuraxz/nutrition_ai.git
```
2. Change the working directory
```bash
cd nutrition_ai/frontend
```
3. Install dependencies
```bash
npm install
```
4. Run the application
```bash
npm start
```
5. Open the browser and go to `http://localhost:3000`


### Deployment
#### Backend
Deployment Guide: [Backend Deployment Guide](https://learn.microsoft.com/en-us/azure/developer/python/tutorial-containerize-simple-web-app-for-app-service?tabs=web-app-flask)

#### Frontend
Deployment Guide: [Frontend Deployment Guide](https://learn.microsoft.com/en-us/azure/static-web-apps/deploy-react?pivots=github)


### CI/CD
We have used GitHub Actions for CI/CD. The workflow file can be found [here](https://docs.github.com/en/actions/deployment/deploying-to-your-cloud-provider/deploying-to-azure)
