import express from "express";
import session from "express-session";
import fhirClient from "fhirclient";

const app = express();
const port = 5000;

// OAuth2 Client Configuration
const client_id = "d81ed990-b75a-4fb8-94b5-a9df0e809631"; // Replace with your client ID
const scope = "patient/*.read openid fhirUser"; // Adjust the scope as needed
const redirect_uri = "http://127.0.0.1:5000/callback"; // Ensure this matches the one registered with the EHR
const iss = "https://fhir.epic.com/interconnect-fhir-oauth/api/FHIR/R4"; // Replace with your FHIR server base URL
// Set up session middleware
app.use(
  session({
    secret: "fhirclient-secret", // Replace with a strong secret in production
    resave: false,
    saveUninitialized: true,
    cookie: { secure: false }, // Set secure to true if using HTTPS
  })
);

// Launch Endpoint: Initiates the OAuth2 authorization flow
app.get("/launch", (req, res) => {
  fhirClient(req, res).authorize({
    'client_id':client_id,
    'scope':scope,
    'redirect_uri':redirect_uri,
    iss,
  });
});

// Root Endpoint: Handles the redirect and fetches data
// Root Endpoint: Handles the redirect and fetches data
app.get("/callback", async (req, res) => {
  try {
    // Complete the OAuth2 process and obtain a SMART client
    const client = await fhirClient(req, res).ready();

    // Access the token response
    const tokenResponse = client.state.tokenResponse;
    console.log("Access Token:", tokenResponse.access_token);
    console.log("Patient ID:", tokenResponse.patient);
    console.log("Expires in:", tokenResponse.expires_in);

    // Fetch patient data 
    const patient = await client.request("Patient");
    res.json({ success: true, token: tokenResponse.access_token, patient });
  } catch (error) {
    console.error("Error during authorization or data retrieval:", error);
    res.status(500).json({ success: false, error: error.message });
  }
});


// Start the Express server
app.listen(port, () => {
  console.log(`FHIR app is running at http://127.0.0.1:${port}`);
});
