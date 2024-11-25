import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <div className="container bg-danger-subtle p-4">
      404 | Page Not Found<br></br>
      <Link to="/">Home</Link>
    </div>
  );
}
