import React, { createContext, useContext, useEffect, useState } from 'react';
import { 
  signInWithEmailAndPassword, 
  createUserWithEmailAndPassword, 
  signOut, 
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth';
import { auth } from '../firebase/config';
import axios from 'axios';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);

  const api = axios.create({
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  });

  api.interceptors.request.use((config) => {
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  });

  
  const register = async (email, password, name) => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      
      await updateProfile(userCredential.user, {
        displayName: name
      });
      
      const firebaseToken = await userCredential.user.getIdToken();
      setToken(firebaseToken);
      
      try {
        const response = await api.post('/api/auth/verify', {}, {
          headers: { Authorization: `Bearer ${firebaseToken}` }
        });
        setUser(response.data.user);
      } catch (backendError) {
        console.warn('Backend not available:', backendError.message);
        setUser({
          uid: userCredential.user.uid,
          email: userCredential.user.email,
          name: name,
          role: 'customer'
        });
      }
      
      return { success: true };
    } catch (error) {
      console.error('Register error:', error);
      let errorMessage = 'Registration failed';
      if (error.code === 'auth/email-already-in-use') {
        errorMessage = 'Email already in use.';
      } else if (error.code === 'auth/weak-password') {
        errorMessage = 'Password should be at least 6 characters.';
      }
      return { success: false, error: errorMessage };
    }
  };


  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (firebaseUser) => {
      if (firebaseUser) {
        try {
          const firebaseToken = await firebaseUser.getIdToken();
          setToken(firebaseToken);
          
          try {
            const response = await api.post('/api/auth/verify', {}, {
              headers: { Authorization: `Bearer ${firebaseToken}` }
            });
            setUser(response.data.user);
          } catch (backendError) {
            console.warn('Backend not available:', backendError.message);
            setUser({
              uid: firebaseUser.uid,
              email: firebaseUser.email,
              name: firebaseUser.displayName || firebaseUser.email.split('@')[0],
              role: 'customer'
            });
          }
        } catch (error) {
          console.error('Error getting user:', error);
          setUser(null);
        }
      } else {
        setUser(null);
        setToken(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  const value = {
    user,
    
    register,
    loading,
    token,
    api
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};