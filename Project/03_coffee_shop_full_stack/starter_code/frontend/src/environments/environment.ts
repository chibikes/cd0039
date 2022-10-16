/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-6fsgzpr4.us', // the auth0 domain prefix
    audience: 'trivia', // the audience set for the auth0 app
    clientId: 'o2SIuKZHFhjFjVYyQFvwqzEFQmQ9Qkae', // the client id generated for the auth0 app
    callbackURL: 'https://localhost:8101', // the base url of the running ionic application. 
  }
};
