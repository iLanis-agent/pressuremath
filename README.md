# Pressure math

The PSI names the poster, the GPM names the work, and the nozzle names the pressure.

Pressure washers are sold on PSI measured at zero flow. The cleaning happens in PSI times GPM - cleaning units - and the machine's working pressure is set by the nozzle orifice, not the motor. Pressure math does the honest arithmetic for all three.

## The three tools

- **Cleaning units** - PSI and GPM become `PSI x GPM`, banded unrounded from a rinser to industrial territory, with a flag when big PSI and small flow mean the box is selling pressure more than cleaning.
- **Nozzle size** - flow and target working pressure become the orifice number: `GPM x sqrt(4000 / PSI)`, rounded to the nearest half size. The orifice sets the working pressure; the fan angle only spreads it.
- **Time plan** - cleaning units and area become honest minutes: a labeled norm of `units / 10` square feet per hour with a surface cleaner, half that with a wand.

## Honesty notes

Illustrative planning arithmetic only. Bands and coverage rates are labeled norms, not promises: surface, nozzle distance and technique move the real time. Never point the jet at people or pets, respect the kickback on ladders, and check what the surface can take - a zero-degree tip writes its name in soft wood, and high pressure can force water under skin, which is a medical emergency, not a scratch.

## Files

- `index.html` - the pitch
- `app.html` - the calculators
- `engine.js` - the arithmetic (browser and node)
- `oracle.py` - the same arithmetic, float-for-float, writing `expected.json`
- `test.js` - runs every case in `expected.json` through `engine.js` and compares results and renders exactly

Run the check:

```
python3 oracle.py && node test.js
```
