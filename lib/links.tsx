// Link annotations — `Phrase (/path/)` — (LINKFIX 2026-11-13).
//
// The doc carries NO hyperlink objects. Every internal link is a
// parenthetical path annotation: the phrase immediately before the paren
// is the anchor, the path is the href. The ` (/path/)` text is LINK
// METADATA and must NEVER render as visible text.
//
// Rule (qa/parse_tabs.py — the same doc convention):
//   href = path with trailing slash stripped ("/" stays "/").
//   anchor = the phrase immediately before the paren:
//     1. text after the last "see " / "learn more about " marker, but
//        ONLY when that marker sits after the last clause boundary —
//        "see" also occurs as an ordinary verb ("or see dark spots").
//     2. else text after the LAST clause boundary in
//        {". ", "! ", "? ", ": ", ", "} (the trailing service-name
//        pattern: "...dry the cavity. Burst Pipe Water Damage (/.../)").
//     3. else the whole segment (after "including " if present),
//        stripping leading ", " / "and " / verb prefixes
//        ("covers ", "we cover ", ...).
//   DEDUPE: 1 link per target per page in body copy (header/footer
//   exempt); first occurrence wins, later ones render as plain phrase
//   text. SELF-LINK renders as plain text. NO truncation: the anchor is
//   the FULL phrase he wrote — a link anchored on only part of his
//   phrase counts as missing (his standing rule). That overrides
//   a 5-word truncation.
//   Visible words drop by exactly one token per annotation (the paren
//   itself); the anchor words stay visible. Verbatim accounting:
//   expected visible = doc words - annotation tokens - heading-label
//   tokens - structural tokens.
//
// This module is pure (no data-file mutation): the data keeps the
// annotations verbatim; the renderer interprets them via splitAnnotated.
// Server-component safe.
import Link from "next/link";
import type { ReactNode } from "react";

export type LinkPart = { text: string; href?: string };

const LINK_RE_SRC = "\\((/[^)]*)\\)";

export function normSlug(url: string): string {
  return url === "/" ? "/" : url.replace(/\/+$/, "");
}

const VERB_PREFIXES = [
  "the same 24/7 crew covers ",
  "the same crew also covers ",
  "the same crew covers ",
  "the crew also covers ",
  "we cover ",
  "covers ",
  "also covers ",
];

export function extractAnchor(segment: string): string {
  // 1. Last clause boundary among ". " "! " "? " ": " ", " (trailing
  //    service-name pattern and "Full list: X" both resolve here).
  let cut = -1;
  for (const b of [". ", "! ", "? ", ": ", ", "]) {
    const idx = segment.lastIndexOf(b);
    if (idx > cut) cut = idx + b.length;
  }
  const tail = cut >= 0 ? segment.slice(cut) : segment;
  // 2. "see " / "learn more about " marker AFTER that boundary only.
  const low = tail.toLowerCase();
  let last = -1;
  for (const pat of ["see ", "learn more about "]) {
    const idx = low.lastIndexOf(pat);
    if (idx > last) last = idx + pat.length;
  }
  let cand = last >= 0 ? tail.slice(last) : tail;
  // 3. Strip leading list separators / verb phrases, repeatedly.
  //    (Only when no boundary was found above is "including " relevant;
  //    when a boundary WAS found, cand already starts after it.)
  if (cut < 0 && cand.includes("including ")) {
    cand = cand.split("including ").pop() as string;
  }
  let changed = true;
  while (changed) {
    changed = false;
    const s = cand.replace(/^\s+/, "");
    if (s.startsWith(",")) {
      cand = s.slice(1);
      changed = true;
      continue;
    }
    if (s.toLowerCase().startsWith("and ")) {
      cand = s.slice(4);
      changed = true;
      continue;
    }
    const l = s.toLowerCase();
    for (const vp of VERB_PREFIXES) {
      if (l.startsWith(vp)) {
        cand = s.slice(vp.length);
        changed = true;
        break;
      }
    }
  }
  cand = cand.trim().replace(/[.,;:]+$/, "");
  return cand.replace(/\s+/g, " ").trim();
}

type LinkRecord = {
  anchor: string;
  href: string;
  /** 0-based char offset of the anchor start in the STRIPPED text. */
  pos: number;
  status: "kept" | "dup-dropped" | "self-dropped";
};

function extractLinks(
  rawText: string,
  ownSlug: string,
  seen: Set<string>,
): { stripped: string; links: LinkRecord[] } {
  const re = new RegExp(LINK_RE_SRC, "g");
  const links: LinkRecord[] = [];
  const outParts: string[] = [];
  let removedBefore = 0;
  let prevEnd = 0;
  let cursor = 0;
  let m: RegExpExecArray | null;
  while ((m = re.exec(rawText)) !== null) {
    const href = normSlug(m[1]);
    const segment = rawText.slice(prevEnd, m.index);
    const anchorFull = extractAnchor(segment);
    const idxInSeg = anchorFull ? segment.lastIndexOf(anchorFull) : -1;
    if (anchorFull && idxInSeg >= 0) {
      const anchorStartRaw = prevEnd + idxInSeg;
      const pos = anchorStartRaw - removedBefore;
      let status: LinkRecord["status"];
      if (href === ownSlug) status = "self-dropped";
      else if (seen.has(href)) status = "dup-dropped";
      else {
        status = "kept";
        seen.add(href);
      }
      links.push({ anchor: anchorFull, href, pos, status });
    }
    // Strip the paren (and the single space before it) from visible text.
    let chunk = rawText.slice(cursor, m.index);
    if (chunk.endsWith(" ")) {
      chunk = chunk.slice(0, -1);
      removedBefore += 1;
    }
    outParts.push(chunk);
    removedBefore += m[0].length;
    cursor = m.index + m[0].length;
    prevEnd = cursor;
  }
  outParts.push(rawText.slice(cursor));
  const stripped = outParts
    .join("")
    .replace(/\u2028/g, "-")
    .replace(/—/g, "-");
  return { stripped, links };
}

/** Split a text unit into plain runs + link runs (kept links only).
 *  Parts concatenate EXACTLY to the annotation-stripped text.
 *  `seen` is the per-page first-occurrence set (mutated). */
export function splitAnnotated(
  text: string,
  ownSlug: string,
  seen: Set<string>,
): LinkPart[] {
  const { stripped, links } = extractLinks(text, ownSlug, seen);
  if (links.length === 0) return stripped ? [{ text: stripped }] : [];
  const parts: LinkPart[] = [];
  let cursor = 0;
  for (const L of links) {
    const start = L.pos;
    const end = L.pos + L.anchor.length;
    if (start > cursor) parts.push({ text: stripped.slice(cursor, start) });
    parts.push(
      L.status === "kept"
        ? { text: L.anchor, href: L.href }
        : { text: L.anchor },
    );
    cursor = end;
  }
  if (cursor < stripped.length) parts.push({ text: stripped.slice(cursor) });
  return parts;
}

/** Plain stripped text (no links) — e.g. FAQPage schema answers, which
 *  must equal the visible answer text exactly. */
export function stripAnnotations(text: string): string {
  return extractLinks(text, "", new Set()).stripped;
}

/** Render link parts as React nodes. Kept links render as body links
 *  (no underline, per his rule); dup/self-dropped anchors are plain. */
export function LinkParts({
  parts,
  prefix,
}: {
  parts: LinkPart[];
  prefix: string;
}): ReactNode[] {
  return parts.map((p, i) =>
    p.href ? (
      <Link key={`${prefix}-${i}`} href={p.href} className="body-link">
        {p.text}
      </Link>
    ) : (
      <span key={`${prefix}-${i}`}>{p.text}</span>
    ),
  );
}
