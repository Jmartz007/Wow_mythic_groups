import Table from "../components/Table";

export default function EditDungeons() {
  let url = "http://localhost:5000/groups/api/dungeons";

  return (
    <>
      <h3>Edit Dungeons</h3>

      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <form method="POST">
          <h1 className="title">Current Dungeons</h1>
          <div id="Dungeons List" className="container grid gap-3">
            <div>
              <label htmlFor="newdungeon" className="col">
                Enter New Dungeon
              </label>
              <input
                className="col"
                type="text"
                id="newdungeon"
                name="newdungeon"
                pattern="[a-z ':A-Z]+"
              />
              <button className="col" type="submit">
                Add
              </button>
            </div>
          </div>
        </form>
        <Table url={url}></Table>
      </div>
    </>
  );
}
