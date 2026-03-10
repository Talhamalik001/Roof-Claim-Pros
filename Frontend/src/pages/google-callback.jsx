// import { useEffect } from "react";
// import { useNavigate } from "react-router-dom";
// import axios from "axios";

// const GoogleCallback = () => {
//   const navigate = useNavigate();

//   useEffect(() => {
//     // Fetch the token from the URL parameters
//     const token = new URLSearchParams(window.location.search).get("token");
//     if (token) {
//       axios
//         .post("http://localhost:9000/google/callback", { token })
//         .then((response) => {
//           console.log("User Info:", response.data); // You can store this in your state or context
//           navigate("/dashboard");  // Redirect to dashboard or other page
//         })
//         .catch((error) => {
//           console.error("Login error:", error);
//           alert("Login failed");
//         });
//     }
//   }, []);

//   return <div>Loading...</div>;  // Display loading message until user info is fetched
// };

// export default GoogleCallback;