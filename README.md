# Getting Started with FMMI

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
## Install

### Install Backend

#### Install python

#### Download files from healthify drive
- Log in with healthifygroup@gmail.com/420blazeit69!!!.
- Go to drive.
- Download: tfidf_matrix.npz, new_recipes.indexed.parquet, vectorizer.joblib
- Make in /Backend new folder /data.
- Move the downloaded files to the /Backend/data folder in the repo.
- make new file: apikey.txt and put in the gemini api key for this project

#### Install python packages
- open terminal /backend
- pip install scikit-learn
- pip install nltk
- pip install google-generativeai
- pip install datasets
- pip install flask
- pip install flask_cors
- uncomment line 17,18,19: nltk.download("stopwords")
  - run ones
  - comment line 17,18,19
- d

### Install Frontend

#### Install Node.js and npm
Needed for running the dev env.
NPM is also installed togheter with the node.js framework.

#### Install Node Modules

Open terminal in the root folder of this project and type `npm i` this will install all needed node modules

## Run

### Run Backend
Go to /Backend folder. Open terminal and type `python backendapi.py`. This runs the backend api that is build in python using flask;

### Run Frontend

In the project directory, you can run: `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

#### Go to /src/services/backendService.js in the variable ipAddress put the ip of your device. Get your ip by the ipconfig command in cmd.

## Deployment

`npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)
