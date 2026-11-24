// Shared by index.html (dashboard) and graph.html (logic graph): escaping, status names, board and stone pictures.
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const STATUS = { proved: "Proved", empirical: "Holds in tests", open: "Open", disproved: "Ruled out", idea: "Idea to try" };
const PAL = ["#3b6fd8","#f08a24","#3aa655","#d93f4c","#9457c9","#e0b616","#17a2b8","#ef7fb0","#8d6142","#2f3e57"];
// ---------- pictures: boards and stones ----------
function boardSVG(b) {
  const r0 = Math.min(...b.rows), r1 = Math.max(...b.rows), c0 = Math.min(...b.cols), c1 = Math.max(...b.cols);
  const nr = r1 - r0 + 1, nc = c1 - c0 + 1, S = nc > 7 ? 24 : 28, L = b.par ? 34 : 22, T = 18;
  const W = L + nc * S + 2, Hh = T + nr * S + 2, rank = d => b.D.indexOf(d);
  const pts = new Set((b.pts || []).map(p => p.join())), w = Object.fromEntries((b.w || []).map(([r, c, v]) => [r + "," + c, v]));
  const cand = new Set((b.cand || []).map(p => p.join()));
  let s = `<svg viewBox="0 0 ${W} ${Hh}" width="${W}" height="${Hh}" role="img" aria-label="${esc(b.cap || "board")}"><defs><pattern id="hx" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" style="stroke:var(--line)" stroke-width="2"/></pattern></defs>`;
  for (let c = c0; c <= c1; c++) s += `<text x="${L + (c - c0 + .5) * S}" y="12" text-anchor="middle" font-size="10" style="fill:var(--ink2)">${c}</text>`;
  for (let r = r0; r <= r1; r++) {
    const y = T + (r - r0) * S, has = b.rows.includes(r);
    s += `<text x="${b.par ? 12 : L - 6}" y="${y + S / 2 + 4}" text-anchor="${b.par ? "middle" : "end"}" font-size="10" style="fill:var(--ink2)">${r}</text>`;
    if (b.par && has) s += r % 2 ? `<circle cx="27" cy="${y + S / 2}" r="4" style="fill:var(--ink)"/>` : `<circle cx="27" cy="${y + S / 2}" r="3.5" style="fill:none;stroke:var(--ink)" stroke-width="1.4"/>`;
    for (let c = c0; c <= c1; c++) {
      const x = L + (c - c0) * S, key = r + "," + c, d = c - r, live = has && b.cols.includes(c), k = rank(d);
      s += `<rect x="${x}" y="${y}" width="${S}" height="${S}" style="fill:${!live ? "url(#hx)" : k >= 0 ? PAL[k % 10] : "var(--card)"};fill-opacity:${!live ? 1 : k >= 0 ? .26 : 1};stroke:var(--line)"/>`;
      if (!live) continue;
      if (pts.has(key)) s += `<circle cx="${x + S / 2}" cy="${y + S / 2}" r="${S * .3}" style="fill:${k >= 0 ? PAL[k % 10] : "var(--ink)"};stroke:var(--ink)" stroke-width="1.2"/>`;
      else if (w[key]) s += `<text x="${x + S / 2}" y="${y + S / 2 + 5}" text-anchor="middle" font-size="14" font-weight="700" style="fill:var(--ink)">${esc(w[key])}</text>`;
      else if (k >= 0) s += `<text x="${x + S / 2}" y="${y + S / 2 + 3.5}" text-anchor="middle" font-size="9.5" style="fill:var(--ink2)">${d > 0 ? "+" + d : d}</text>`;
      if (cand.has(key)) s += `<circle cx="${x + S / 2}" cy="${y + S / 2}" r="${S * .42}" style="fill:none;stroke:var(--no)" stroke-width="2" stroke-dasharray="3 2"/>`;
    }
  }
  (b.blocks || []).forEach(([ra, rb, ca, cb]) => s += `<rect x="${L + (ca - c0) * S}" y="${T + (ra - r0) * S}" width="${(cb - ca + 1) * S}" height="${(rb - ra + 1) * S}" style="fill:none;stroke:var(--ink)" stroke-width="2.2" stroke-dasharray="5 3" rx="3"/>`);
  return s + "</svg>";
}
function stonesSVG(st) {
  const U = 22, n = st.hi - st.lo + 1, W = n * U + 10, Hh = 58, hl = new Set(st.hl || []);
  let s = `<svg viewBox="0 0 ${W} ${Hh}" width="${W}" height="${Hh}" role="img" aria-label="${esc(st.cap || "stones")}">`;
  s += `<rect x="2" y="30" width="${W - 4}" height="7" rx="2" style="fill:var(--wood)"/>`;
  for (let m = st.lo; m <= st.hi; m++) { const x = 5 + (m - st.lo + .5) * U;
    s += `<line x1="${x}" y1="37" x2="${x}" y2="41" style="stroke:var(--ink2)"/><text x="${x}" y="53" text-anchor="middle" font-size="9.5" style="fill:var(--ink2)">${m > 0 ? "+" + m : m}</text>`;
    if (st.D.includes(m)) s += `<circle cx="${x}" cy="21" r="8" style="fill:var(--ink2)"/>` + (hl.has(m) ? `<circle cx="${x}" cy="21" r="11" style="fill:none;stroke:#e0743a" stroke-width="2"/>` : ""); }
  return s + "</svg>";
}
function labPerm(b) {
  const n = b.rows.length, pts = b.pts || [];
  if (n > 10 || pts.length !== n || b.cols.length !== n) return null;
  for (let k = 0; k < n; k++) if (b.rows[k] !== k + 1 || b.cols[k] !== k + 1) return null;
  const p = Array(n).fill(0); pts.forEach(([r, c]) => p[r - 1] = c);
  const d = p.map((c, i) => c - i - 1);
  if (p.includes(0) || new Set(p).size !== n || new Set(d).size !== n || d.some(x => !b.D.includes(x))) return null;
  return p.join(",");
}
const one = p => { if (p.t === "board") { const L = labPerm(p); return L ? `<div class="labable" data-lab="${L}" title="Open in the lab">${boardSVG(p)}<span class="labhint">lab ↗</span></div>` : boardSVG(p); }
  return p.t === "stones" ? stonesSVG(p) : ""; };
function picHTML(p) {
  if (p.t === "pair") return `<figure><div class="pics"><div>${one(p.a)}${p.a.cap ? `<figcaption>${esc(p.a.cap)}</figcaption>` : ""}</div><span class="mid">${esc(p.mid || "→")}</span><div>${one(p.b)}${p.b.cap ? `<figcaption>${esc(p.b.cap)}</figcaption>` : ""}</div></div>${p.cap ? `<figcaption>${esc(p.cap)}</figcaption>` : ""}</figure>`;
  return `<figure><div class="pics">${one(p)}</div>${p.cap ? `<figcaption>${esc(p.cap)}</figcaption>` : ""}</figure>`;
}
// ---------- labs ----------
// A lab is a file under labs/ when the page is served or opened from disk. In the single-file bundle
// (bundle.py) the lab pages are inlined as text in window.LABS and shown with srcdoc.
function labFrame(file, title, hash) {
  const inl = window.LABS && window.LABS[file];
  if (!inl) return `<iframe title="${esc(title)}" src="${esc(file)}${hash ? "#" + hash : ""}"></iframe>`;
  const doc = hash ? inl.replace("<head>", () => `<head><script>window.LAB_HASH=${JSON.stringify("#" + hash)}<\/script>`) : inl;
  return `<iframe title="${esc(title)}" srcdoc="${esc(doc)}"></iframe>`;
}
