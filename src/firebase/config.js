import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyA1ERJqkk563YgymE3HGoESihAM4-jMWn0",
  authDomain: "salonapp-cf165.firebaseapp.com",
  projectId: "salonapp-cf165",
  storageBucket: "salonapp-cf165.firebasestorage.app",
  messagingSenderId: "73712229371",
  appId: "1:73712229371:web:93eadf2d1bede8224ec95e",
  measurementId: "G-ZR6EB8ZS3B"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Auth
export const auth = getAuth(app);

export default app;