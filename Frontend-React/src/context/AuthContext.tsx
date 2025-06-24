import React, {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  checkAuthStatus: () => void;
}

interface AuthProviderProps {
  children: React.ReactNode;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  const checkAuthStatus = useCallback(async () => {
    setIsLoading(true);
    try {
      const response = await fetch("/groups/auth/status", {
        method: "GET",
        credentials: "include",
      });
      const data = await response.json();
      setIsAuthenticated(data.authenticated);
    } catch (error) {
      console.error("Error checking authentication status:", error);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  return (
    <AuthContext.Provider
      value={{ isAuthenticated, isLoading, checkAuthStatus }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
