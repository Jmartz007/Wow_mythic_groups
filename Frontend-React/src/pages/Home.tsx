import Table from "../components/Table";

export default function Home() {
  let url = "http://localhost:5000/groups/api/current-players";

  return (
    <>
      <div>
        <h1> Home</h1>
      </div>
      <Table url={url} />
    </>
  );
}
