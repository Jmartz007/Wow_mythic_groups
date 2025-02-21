import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { FormEvent } from "react";

export default function LoginCard() {
  const navigate = useNavigate();
  const { isAuthenticated, checkAuthStatus } = useAuth();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    try {
      const formData = new FormData(e.currentTarget);
      const jsonData = Object.fromEntries(formData.entries());

      const response = await fetch("/groups/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(jsonData),
      });
      console.log(JSON.stringify(jsonData));

      if (!response.ok) {
        const errorResponse = await response.json();
        console.log(errorResponse);
        const errorMessage = errorResponse.error.message;
        throw new Error(errorMessage);
      }

      const data = await response.json();
      console.log(data);
      await checkAuthStatus();

      navigate("/list");
    } catch (error) {
      console.error("error submitting form: ", error);
      if (error instanceof Error) {
        alert(`Log in error: ${error.message}`);
      } else {
        alert("there was an error submitting form");
      }
    }
  };
  return (
    <div className="container mt-5">
      <div className="row justify-content-center">
        <div className="col-md-6">
          <div className="card">
            <div className="card-body">
              <h1 className="card-title text-center">Log In</h1>
              {isAuthenticated ? (
                <div>
                  <h2>Welcome back!</h2>
                  <p>
                    We're glad to see you again. You can navigate to the Player
                    List page to see your players.
                  </p>
                </div>
              ) : (
                <form onSubmit={handleSubmit}>
                  <div className="mb-3">
                    <label htmlFor="username" className="form-label">
                      User Name
                    </label>
                    <input
                      type="text"
                      className="form-control"
                      id="username"
                      name="username"
                      placeholder="User Name"
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Password
                    </label>
                    <input
                      type="password"
                      className="form-control"
                      id="password"
                      name="password"
                      placeholder="Password"
                    />
                  </div>
                  <button type="submit" className="btn btn-primary w-100">
                    Log In
                  </button>
                </form>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
