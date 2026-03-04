export const msalConfig = {
  auth: {
    clientId: "e6fe47ce-a9bd-4650-9f60-587d5010bb21",
    authority: "https://login.microsoftonline.com/common",
    redirectUri: "http://localhost:5173"
  },
  cache: {
    cacheLocation: "localStorage",
    storeAuthStateInCookie: false,
  }
};

export const loginRequest = {
  scopes: ["api://fdee396e-0f4c-4066-a4f8-0ad96d7737be/access_as_user"]
};