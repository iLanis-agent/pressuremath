// Pressure math - pressure washer honesty.
// Cleaning units = PSI x GPM. Bands and notes judge the unrounded figure;
// rounding is for display only.
var PressureMath = (function () {
  function pos(x) { return typeof x === "number" && isFinite(x) && x > 0; }
  function round2(x) { return Math.round(x * 100) / 100; }

  function band(cu) {
    if (cu < 1000) return "a rinser";
    if (cu < 2000) return "light duty - cars and patio furniture";
    if (cu < 4000) return "medium duty - decks and fences";
    if (cu < 7000) return "heavy duty - driveways and siding";
    return "industrial territory";
  }

  function cleanPlan(psi, gpm) {
    if (!pos(psi) || !pos(gpm)) return { error: "pressure and flow must both be above zero" };
    var cu = psi * gpm;
    var hype = psi >= 2000 && gpm < 1.3;
    return { units: Math.round(cu), band: band(cu), hype: hype };
  }

  function renderClean(r, psi, gpm) {
    var s = "Your " + psi + " PSI at " + gpm + " GPM makes " + r.units + " cleaning units - " + r.band;
    if (r.hype) s += ", and the box is selling pressure more than cleaning";
    return s + ".";
  }

  function nozzlePlan(gpm, psi) {
    if (!pos(psi) || !pos(gpm)) return { error: "pressure and flow must both be above zero" };
    var raw = gpm * Math.sqrt(4000 / psi);
    var half = Math.round(raw * 2) / 2;
    return { orifice: half, raw: round2(raw) };
  }

  function renderNozzle(r, gpm, psi) {
    return "Your " + gpm + " GPM at " + psi + " PSI calls for a #" + r.orifice + " orifice ("
      + r.raw + " rounded to the nearest half size) - the orifice sets the working pressure; the fan angle only spreads it.";
  }

  function timePlan(units, sqft) {
    if (!pos(units) || !pos(sqft)) return { error: "area and cleaning units must both be above zero" };
    // Labeled norm: a surface cleaner covers about units/10 sq ft per hour, a wand about half that.
    var cleaner = Math.round(sqft / (units / 10) * 60);
    var wand = Math.round(sqft / (units / 20) * 60);
    return { cleanerMin: cleaner, wandMin: wand };
  }

  function renderTime(r, units, sqft) {
    return "Your " + sqft + " sq ft at " + units + " cleaning units figures about " + r.cleanerMin
      + " minutes with a surface cleaner and " + r.wandMin + " with a wand - a labeled norm, not a promise.";
  }

  return {
    cleanPlan: cleanPlan, renderClean: renderClean,
    nozzlePlan: nozzlePlan, renderNozzle: renderNozzle,
    timePlan: timePlan, renderTime: renderTime
  };
})();
if (typeof module !== "undefined") module.exports = PressureMath;
