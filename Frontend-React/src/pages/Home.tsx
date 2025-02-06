import { FormEvent } from "react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const navigate = useNavigate();

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
    <div className="rounded border border-1 shadow bg-primary-subtle p-4">
      <h1> Home Page</h1>
      <form onSubmit={handleSubmit}>
        <input type="text" name="username" placeholder="User Name" />
        <input type="password" name="password" placeholder="Password" />
        <button type="submit">Log In</button>
      </form>
    </div>
  );
}
