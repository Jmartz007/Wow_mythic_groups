import React, { createContext, useContext, useState, useCallback } from "react";

interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: { id: string; battletag: string } | null;
  characters: Array<{
    characterId: string;
    characterName: string;
    name: string;
    raceName: string;
    specializationName: string;
    level: number;
  }[]> | null;
  blizzardAccessToken: string | null;
  checkAuthStatus: () => void;
  logout: () => Promise<void>;
}

interface AuthProviderProps {
  children: React.ReactNode;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [user, setUser] = useState<{ id: string; battletag: string } | null>(null);
  const [characters, setCharacters] = useState<
    Array<{
      characterId: string;
      characterName: string;
      name: string;
      raceName: string;
      specializationName: string;
      level: number;
    }[]>
  >(null);
  const [blizzardAccessToken, setBlizzardAccessToken] = useState<string | null>(null);

  const checkAuthStatus = useCallback(() => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem("token");
      const blizzardToken = localStorage.getItem("blizzard_access_token");
      const storedUser = localStorage.getItem("user");
      const storedCharacters = localStorage.getItem("characters");

      // If there's a token, consider the user authenticated
      // In a production app, you might want to also verify the token hasn't expired
      if (token) {
        setIsAuthenticated(true);
        // Set user and characters if available
        if (blizzardToken && storedUser && storedCharacters) {
          setUser(JSON.parse(storedUser));
          setCharacters(JSON.parse(storedCharacters));
          setBlizzardAccessToken(blizzardToken);
          console.log("Authenticated user:", JSON.parse(storedUser));
          console.log("Characters available:", storedCharacters);
        }
      }
    } catch (error) {
      console.error("Error checking authentication status:", error);
      setIsAuthenticated(false);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    localStorage.removeItem("token");
    localStorage.removeItem("blizzard_access_token");
    localStorage.removeItem("user");
    localStorage.removeItem("characters");
    setUser(null);
    setCharacters(null);
    setBlizzardAccessToken(null);
    setIsAuthenticated(false);
  }, []);

  // Check auth status when the component mounts
  React.useEffect(() => {
    checkAuthStatus();
  }, [checkAuthStatus]);

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        isLoading,
        user,
        characters,
        blizzardAccessToken,
        checkAuthStatus,
        logout,
      }}
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
