utag.link({
category : "Website - Homepage",
action : "Click",
label : "Game",
name : this.game.name,
section : this.section.name,
position : this.position_id,
secondary_name: "-"
});

utag.link({
category : "Poker - Game Flow",
action : "Click",
label : "Register",
name : this.model.getTournamentName(),
section: "-",
position: "-",
secondary_name: "-",
value : (this.model.getBuyIn() * 100).toFixed(0)
});