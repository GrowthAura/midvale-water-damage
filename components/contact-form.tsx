// Contact request form (P2-3 fix 2026-11-12, his word 21:35 PKT).
// Fields + labels EXACTLY from the Contact tab (Tab 3, "Request Form
// Fields" list); submit button text verbatim "[Send My Request]".
// Template chrome around the verbatim content — the form's own words are
// excluded from the content word-diff (it lives in <section className
// ="contact-form">, stripped by the verifier before counting).
// Pages is static so the form cannot submit: the honest notice says so up
// front, and submit shows the call-first message instead of pretending to
// send. The tab itself says "calling is faster than the form".
"use client";

import { useState } from "react";
import { SITE } from "@/lib/content";
import { TEL_HREF } from "@/components/site";

export default function ContactForm() {
  const [sent, setSent] = useState(false);
  return (
    <section className="contact-form" aria-label="Request form">
      <p className="form-notice">
        Note: this form does not send on this preview site. For the fastest
        help, please call <a href={TEL_HREF}>{SITE.phoneDisplay}</a>, calling
        is faster than the form.
      </p>
      {sent ? (
        <p className="form-sent">
          Thanks, this preview form doesn&apos;t send. Please call{" "}
          <a href={TEL_HREF}>{SITE.phoneDisplay}</a> and a crew will be
          dispatched right away.
        </p>
      ) : (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            setSent(true);
          }}
        >
          <p>
            <label htmlFor="cf-name">Name</label>
            <input id="cf-name" name="name" type="text" autoComplete="name" required />
          </p>
          <p>
            <label htmlFor="cf-phone">Phone number</label>
            <input id="cf-phone" name="phone" type="tel" autoComplete="tel" required />
          </p>
          <p>
            <label htmlFor="cf-address">Address or ZIP code</label>
            <input id="cf-address" name="address" type="text" autoComplete="postal-code" />
          </p>
          <p>
            <label htmlFor="cf-what">What happened (short description)</label>
            <textarea id="cf-what" name="what-happened" rows={3} />
          </p>
          <fieldset>
            <legend>Is the water still running?</legend>
            <span className="radio-row">
              <label>
                <input type="radio" name="water-running" value="Yes" /> Yes
              </label>
              <label>
                <input type="radio" name="water-running" value="No" /> No
              </label>
              <label>
                <input type="radio" name="water-running" value="Not sure" /> Not sure
              </label>
            </span>
          </fieldset>
          <p>
            <label htmlFor="cf-best-time">Best time to call</label>
            <input id="cf-best-time" name="best-time" type="text" />
          </p>
          <button type="submit" className="btn btn-help">
            [Send My Request]
          </button>
        </form>
      )}
    </section>
  );
}
