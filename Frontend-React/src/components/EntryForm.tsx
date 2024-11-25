import React from "react";

export default function EntryForm() {
  function toggleRadioButtons(event: React.ChangeEvent<HTMLInputElement>) {
    // Get the checkbox
    const checkbox = event.target as HTMLInputElement;
    const roleButton = checkbox!.id;
    const newName = `combat_role_${roleButton}`;
    const skillname = `${roleButton}-skill`;

    // Get all radio buttons
    const radioButtons = document.querySelectorAll<HTMLInputElement>(
      `input[type="radio"][name="${newName}"]`
    );
    const skillslider = document.querySelectorAll<HTMLInputElement>(
      `input[type="range"][name="${skillname}"]`
    );
    console.log(radioButtons);
    console.log(skillslider);

    // Enable or disable radio buttons based on checkbox state
    radioButtons.forEach(function (radio) {
      radio.disabled = !checkbox.checked;
      radio.required = checkbox.checked;
    });
    // Enable or disable skill slider based on checkbox state
    skillslider.forEach(function (slider) {
      slider.disabled = !checkbox.checked;
    });
  }

  return (
    <>
      <div className="rounded border border-1 shadow bg-primary-subtle p-4">
        <form method="POST">
          <h1 className="title">Player Entry Form</h1>
          <br />
          <div id="names">
            <label htmlFor="player">Player Name</label>
            <input
              type="text"
              id="player"
              name="playerName"
              placeholder="Your Main's Name(Jmartz)"
              required
              size={30}
              pattern="[a-zA-Z]+"
            />
            <br />
            <label htmlFor="charName">Character's Name</label>
            <input
              type="text"
              id="charName"
              name="characterName"
              placeholder="Character Name(Calioma)"
              required
              size={25}
              pattern="[a-zA-Z]+"
            />
          </div>
          <br />
          <br />

          <div id="keyInfo" className="container grid row gap-3">
            <div className="col">
              <label htmlFor="dungeon" className="row">
                Dungeon
              </label>
              <select
                className="form-select row p-1"
                aria-label="Default select example"
                name="dungeon"
                id="dungeon"
                defaultValue={"Unknown"}
              >
                <option value="Unknown">Select Dungeon</option>
                {/* insert function to fetch dungeon names from backend 
                <option value="{{dungeon}}">{{dungeon}}</option>*/}
                <option value="City of Threads">City of Threads</option>
              </select>
            </div>

            <div className="col">
              <label htmlFor="keylevel" className="row">
                Key Level
              </label>
              <input
                className="row"
                type="text"
                id="keylevel"
                name="keylevel"
                defaultValue="0"
                pattern="[0-9]+"
              />
            </div>
          </div>

          <br />
          <label htmlFor="class">Select your class:</label>
          <div id="class" className="container grid gap-0 row-gap-5">
            <div>
              <input
                type="radio"
                id="warrior"
                name="class"
                value="Warrior"
              ></input>
              <label htmlFor="warrior" className="pe-4 g-col-6">
                Warrior
              </label>
              <input
                type="radio"
                id="paladin"
                name="class"
                value="Paladin"
              ></input>
              <label htmlFor="paladin" className="pe-4 g-col-6">
                Paladin
              </label>
              <input
                type="radio"
                id="hunter"
                name="class"
                value="Hunter"
              ></input>
              <label htmlFor="hunter" className="pe-4 g-col-6">
                Hunter
              </label>

              <input type="radio" id="rogue" name="class" value="Rogue"></input>
              <label htmlFor="rogue" className="pe-4 g-col-6">
                Rogue
              </label>

              <input
                type="radio"
                id="priest"
                name="class"
                value="Priest"
              ></input>
              <label htmlFor="priest" className="pe-4 g-col-6">
                Priest
              </label>

              <input
                type="radio"
                id="shaman"
                name="class"
                value="Shaman"
              ></input>
              <label htmlFor="shaman" className="pe-4 g-col-6">
                Shaman
              </label>
            </div>
            <div className="pe-4 g-col-6">
              <input type="radio" id="mage" name="class" value="Mage"></input>
              <label htmlFor="mage" className="pe-4 g-col-6">
                Mage
              </label>

              <input
                type="radio"
                id="warlock"
                name="class"
                value="Warlock"
              ></input>
              <label htmlFor="warlock" className="pe-4 g-col-6">
                Warlock
              </label>

              <input type="radio" id="monk" name="class" value="Monk"></input>
              <label htmlFor="monk" className="pe-4 g-col-6">
                Monk
              </label>

              <input type="radio" id="druid" name="class" value="Druid"></input>
              <label htmlFor="druid" className="pe-4 g-col-6">
                Druid
              </label>

              <input
                type="radio"
                id="demonHunter"
                name="class"
                value="Demon Hunter"
              ></input>
              <label htmlFor="demonHunter" className="pe-4 g-col-6">
                Demon Hunter
              </label>

              <input
                type="radio"
                id="deathKnight"
                name="class"
                value="Death Knight"
              ></input>
              <label htmlFor="deathKnight" className="pe-4 g-col-6">
                Death Knight
              </label>

              <input
                type="radio"
                id="evoker"
                name="class"
                value="Evoker"
              ></input>
              <label htmlFor="evoker" className="pe-4 g-col-6">
                Evoker
              </label>
            </div>
          </div>
          <br />
          <label htmlFor="role">
            Select the roles you play with this character
          </label>
          <div id="role" className="row g-12" />
          <div className="col">
            <input
              type="checkbox"
              id="tank"
              value="Tank"
              name="role"
              className="col ms-3 rolebutton"
              onChange={toggleRadioButtons}
            />
            <label htmlFor="tank" className="col-md-3">
              Tank
            </label>
            <input
              type="range"
              className="form-range row-md-2 me-1"
              min="1"
              max="3"
              id="tank-skill"
              name="tank-skill"
              disabled
            />
            <label htmlFor="tank-skill" className="form-label row-sm-3 mx-4">
              Skill
            </label>
            <div id="combat_role_tank">
              <label htmlFor="combat_role_tank">Select Range:</label>
              <input
                type="radio"
                id="tank-melee"
                name="combat_role_tank"
                value="Melee"
                disabled
                required
              />
              <label htmlFor="tank-melee" className="pe-4 g-col-6">
                Melee
              </label>
              <input
                type="radio"
                id="tank-ranged"
                name="combat_role_tank"
                value="Ranged"
                disabled
              ></input>
              <label htmlFor="tank-ranged" className="pe-4 g-col-6">
                Ranged
              </label>
            </div>
          </div>

          <div className="col">
            <input
              type="checkbox"
              id="healer"
              value="Healer"
              name="role"
              className="col ms-3 rolebutton"
              onChange={toggleRadioButtons}
            />
            <label htmlFor="healer" className="col-md-3">
              Healer
            </label>
            <input
              type="range"
              className="form-range row-md-2"
              min="1"
              max="3"
              id="healer-skill"
              name="healer-skill"
              disabled
            />
            <label htmlFor="healer-skill" className="form-label row-sm-2  mx-4">
              Skill
            </label>
            <div id="combat_role_healer">
              <label htmlFor="combat_role_healer">Select Range:</label>
              <input
                type="radio"
                id="healer-melee"
                name="combat_role_healer"
                value="Melee"
                disabled
                required
              />
              <label htmlFor="healer-melee" className="pe-4 g-col-6">
                Melee
              </label>
              <input
                type="radio"
                id="healer-ranged"
                name="combat_role_healer"
                value="Ranged"
                disabled
              ></input>
              <label htmlFor="healer-ranged" className="pe-4 g-col-6">
                Ranged
              </label>
            </div>
          </div>
          <div className="col">
            <input
              type="checkbox"
              id="dps"
              value="DPS"
              name="role"
              className="col ms-3 rolebutton"
              onChange={toggleRadioButtons}
            />
            <label htmlFor="dps" className="col-md-3">
              DPS
            </label>
            <input
              type="range"
              className="form-range col-md-2"
              min="1"
              max="3"
              id="dps-skill"
              name="dps-skill"
              disabled
            />
            <label htmlFor="dps-skill" className="form-label col-sm-2  mx-4">
              Skill
            </label>
            <div>
              <label htmlFor="combat_role_dps">Select Range:</label>
              <input
                type="radio"
                id="dps-melee"
                name="combat_role_dps"
                value="Melee"
                disabled
                required
              />
              <label htmlFor="dps-melee" className="pe-4 g-col-6">
                Melee
              </label>
              <input
                type="radio"
                id="dps-ranged"
                name="combat_role_dps"
                value="Ranged"
                disabled
              ></input>
              <label htmlFor="dps-ranged" className="pe-4 g-col-6">
                Ranged
              </label>
            </div>
          </div>

          <br />
          <button type="submit">Submit</button>
        </form>
      </div>
    </>
  );
}
