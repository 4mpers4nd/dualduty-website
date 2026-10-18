// Pure planner logic. No network, browser storage, or personal information.
export const STORAGE_KEY = 'dualDuty.plan.v1';
const finite = (x, min, max, fallback) => typeof x === 'number' && Number.isFinite(x) ? Math.min(max, Math.max(min, x)) : fallback;
export function normalize(raw, config) {
  const r = raw && typeof raw === 'object' ? raw : {};
  const available = new Map(config.items.map(i => [i.id, i]));
  const found = new Set();
  const items = Array.isArray(r.items) ? r.items.slice(0, 100).flatMap(i => {
    if (!i || !available.has(i.id) || found.has(i.id)) return [];
    found.add(i.id);
    const def = available.get(i.id);
    return [{id:i.id, quantity:Math.round(finite(i.quantity,1,99,1)), volume:finite(i.volume,0.01,100,def.volume)}];
  }) : [];
  const city = config.areas.some(a => a.name === r.city) || r.city === 'Rural Sanpete / other' ? r.city : config.areas[0].name;
  return {items, difficulty:['easy','moderate','difficult'].includes(r.difficulty) ? r.difficulty : 'easy', stairs:Math.round(finite(r.stairs,0,10,0)), city, special:r.special === true, useVolume:r.useVolume === true, manualVolume:finite(r.manualVolume,0,100,0)};
}
const rate = x => typeof x === 'number' && Number.isFinite(x) && x >= 0;
export function calculate(raw, config) {
  const state = normalize(raw, config);
  const lines = state.items.map(i => ({...config.items.find(x=>x.id===i.id), ...i}));
  const itemVolume = lines.reduce((n,i)=>n+i.volume*i.quantity,0);
  const volume = state.useVolume ? state.manualVolume : itemVolume;
  const heavyCount = lines.reduce((n,i)=>n+(i.heavy ? i.quantity : 0),0);
  const special = state.special || lines.some(i=>i.special);
  const capacity = config.trailer.usableCubicYards;
  let load = volume === 0 ? 'Add items or enter occupied volume to begin.' : volume < 1 ? 'Compact pile — less than 1 cubic yard.' : volume < 3 ? 'Small load — approximately 1–3 cubic yards.' : volume < 6 ? 'Medium load — approximately 3–6 cubic yards.' : 'Large load — 6 or more cubic yards.';
  let fill = Math.min(100,volume / 10 * 100);
  if (rate(capacity) && capacity > 0) {
    load = `${(volume / capacity * 100).toFixed(0)}% of configured trailer volume (${capacity} yd³). ${volume > capacity ? 'Multiple volume loads may be needed. ' : ''}Weight limits still apply.`;
    fill = Math.min(100, volume / capacity * 100);
  } else load += ' Trailer capacity unconfirmed; bar uses a 10 yd³ planning scale.';
  const factors = [`${{easy:'Curb / driveway access',moderate:'Indoor carry',difficult:'Tight or long carry'}[state.difficulty]}`, `${state.stairs} flight${state.stairs===1?'':'s'} of stairs`];
  if (heavyCount) factors.push(`${heavyCount} potentially heavy item${heavyCount===1?'':'s'} — safe handling review required`);
  if (special) factors.push('Special disposal review required');
  if (state.useVolume) factors.push('Manual volume replaces calculated item total');
  if (state.city === 'Rural Sanpete / other') factors.push('Rural location — coverage and travel need review');
  const p=config.pricing;
  const required=[p.baseCharge,p.volumeRatePerYard,p.laborRatePerHour,p.disposalAllowance,p.heavyItemAdjustment,p.minimumCharge,p.travelCharges[state.city],p.laborHours[state.difficulty],p.stairsHoursPerFlight,p.specialHandlingCharge];
  let price=null, breakdown=[];
  if(config.features.pricingEstimates && volume>0 && required.every(rate)) {
    breakdown=[['Base service',p.baseCharge],['Occupied volume',volume*p.volumeRatePerYard],['Estimated labor',(p.laborHours[state.difficulty]+state.stairs*p.stairsHoursPerFlight)*p.laborRatePerHour],['Travel',p.travelCharges[state.city]],['Disposal allowance',p.disposalAllowance],['Heavy item adjustment',heavyCount*p.heavyItemAdjustment],['Special handling',special?p.specialHandlingCharge:0]];
    const sum=breakdown.reduce((a,x)=>a+x[1],0);
    if(sum<p.minimumCharge)breakdown.push(['Minimum charge adjustment',p.minimumCharge-sum]);
    price=Math.round(Math.max(p.minimumCharge,sum)*100)/100;
  }
  return {state,lines,itemVolume,volume,heavyCount,special,load,fill,factors,price,breakdown};
}
export function summary(result, config) {
  return [config.business.name+' — Load plan', 'Planning only. Not a booking or confirmed quote.', '', ...result.lines.map(i=>`${i.quantity} × ${i.name} @ ${i.volume.toFixed(2)} yd³ each = ${(i.quantity*i.volume).toFixed(2)} yd³`), `Estimated occupied volume: ${result.volume.toFixed(2)} yd³`, result.load, `Community: ${result.state.city}`, ...result.factors, '', result.price===null?'No dollar estimate: pricing is unconfigured or incomplete.':`Preliminary estimate: $${result.price.toFixed(2)} USD`, ...result.breakdown.map(([k,v])=>`${k}: $${v.toFixed(2)}`), '', 'Actual volume, packing, safe payload, item acceptance, disposal arrangements and final price require business confirmation. No personal information is included.'].join('\n');
}
