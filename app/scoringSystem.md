danger {
	death: 0
	danger 0.5
	safe: 1
}

options {
	3: 1
	2: 0.75
	1: 0.25
}

wall proximity {
	5: 1
	4: 0.8
	3: 0.6
	2: 0.4
	1: 0.2
}

Food {
	True: 
	False: 0.5
}


hunger {
	stuffed: 0.5
	full: 0.75
	none: 1
	peckish: 1.2
	hungry: 1.5
	starving: 2
	ravenous: 5
}

Health_to_hunger {
	50+: none
	40+: peckish
	30+: hungry
	20+: starving
	10+: ravenous

}