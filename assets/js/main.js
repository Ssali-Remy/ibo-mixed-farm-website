/* ==========================================================================
   IBO Mixed Farm Ltd — site behaviour
   No dependencies, no build step.
   ========================================================================== */

/* --------------------------------------------------------------------------
   CONTACT DETAILS — single source of truth.
   Update these three values and every button, link and prefilled message
   across the whole site updates with them.

   NOTE: the phone number below is a PLACEHOLDER. The number printed on the
   farm's exhibition banner was not legible in the supplied photos. Replace
   both WHATSAPP (digits only, international format, no "+") and PHONE_DISPLAY
   with the real line before launch.
   -------------------------------------------------------------------------- */
const IBO = {
  WHATSAPP: "256700000000",              // TODO: real WhatsApp number, digits only
  PHONE_DISPLAY: "+256 700 000 000",     // TODO: real number as it should read on screen
  EMAIL: "ibomixedfarm@gmail.com",
  LOCATION: "Bwizibwera, Rwanyamahembe Sub-county, Mbarara, Uganda",
};

/* --------------------------------------------------------------------------
   Inject contact details into any element marked up for them
   -------------------------------------------------------------------------- */
function applyContactDetails() {
  document.querySelectorAll("[data-phone-text]").forEach((el) => {
    el.textContent = IBO.PHONE_DISPLAY;
  });

  document.querySelectorAll("[data-phone-link]").forEach((el) => {
    el.setAttribute("href", "tel:" + IBO.PHONE_DISPLAY.replace(/[^\d+]/g, ""));
  });

  document.querySelectorAll("[data-email-text]").forEach((el) => {
    el.textContent = IBO.EMAIL;
  });

  document.querySelectorAll("[data-email-link]").forEach((el) => {
    el.setAttribute("href", "mailto:" + IBO.EMAIL);
  });

  document.querySelectorAll("[data-whatsapp]").forEach((el) => {
    const preset = el.getAttribute("data-whatsapp");
    const text = preset
      ? preset
      : "Hello IBO Mixed Farm, I found you on your website and I would like to make an enquiry.";
    el.setAttribute(
      "href",
      "https://wa.me/" + IBO.WHATSAPP + "?text=" + encodeURIComponent(text)
    );
    el.setAttribute("target", "_blank");
    el.setAttribute("rel", "noopener");
  });
}

/* --------------------------------------------------------------------------
   Mobile navigation
   -------------------------------------------------------------------------- */
function initNav() {
  const toggle = document.querySelector(".nav-toggle");
  const drawer = document.getElementById("mobile-nav");
  if (!toggle || !drawer) return;

  const close = () => {
    drawer.classList.remove("is-open");
    toggle.setAttribute("aria-expanded", "false");
  };

  toggle.addEventListener("click", () => {
    const open = toggle.getAttribute("aria-expanded") === "true";
    drawer.classList.toggle("is-open", !open);
    toggle.setAttribute("aria-expanded", String(!open));
  });

  drawer.addEventListener("click", (e) => {
    if (e.target.closest("a")) close();
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") close();
  });

  // Reset the drawer if the viewport grows past the desktop breakpoint
  window.matchMedia("(min-width: 1024px)").addEventListener("change", (e) => {
    if (e.matches) close();
  });
}

/* --------------------------------------------------------------------------
   Sticky header shadow
   -------------------------------------------------------------------------- */
function initStickyHeader() {
  const header = document.querySelector(".site-header");
  if (!header) return;

  const update = () => {
    header.classList.toggle("is-stuck", window.scrollY > 8);
  };

  update();
  window.addEventListener("scroll", update, { passive: true });
}

/* --------------------------------------------------------------------------
   Scroll reveal
   -------------------------------------------------------------------------- */
function initReveal() {
  const items = document.querySelectorAll(".reveal");
  if (!items.length) return;

  if (
    !("IntersectionObserver" in window) ||
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  ) {
    items.forEach((el) => el.classList.add("is-visible"));
    return;
  }

  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "0px 0px -8% 0px", threshold: 0.08 }
  );

  items.forEach((el) => io.observe(el));
}

/* --------------------------------------------------------------------------
   Gallery filtering
   -------------------------------------------------------------------------- */
function initGalleryFilter() {
  const buttons = document.querySelectorAll(".filter-btn");
  const items = document.querySelectorAll(".gallery-item");
  if (!buttons.length || !items.length) return;

  buttons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const filter = btn.dataset.filter;

      buttons.forEach((b) =>
        b.setAttribute("aria-pressed", String(b === btn))
      );

      items.forEach((item) => {
        const show = filter === "all" || item.dataset.category === filter;
        item.hidden = !show;
      });
    });
  });
}

/* --------------------------------------------------------------------------
   Enquiry / booking forms

   There is no server behind this build (the brief is "start with enquiries",
   so nothing is stored or charged here). On submit we assemble the answers
   into a single readable message and hand it to whichever channel the visitor
   picked — WhatsApp or email. Both open prefilled, so the Director receives a
   complete, structured enquiry either way.

   To switch to a hosted form service later, point FORM_ENDPOINT at it and
   this handler will POST instead.
   -------------------------------------------------------------------------- */
const FORM_ENDPOINT = null; // e.g. "https://formspree.io/f/xxxxxxx"

function buildMessage(form) {
  const title = form.dataset.formTitle || "Website enquiry";
  const lines = [title, "".padEnd(title.length, "-")];

  form.querySelectorAll("input, select, textarea").forEach((el) => {
    if (!el.name || el.type === "submit" || el.closest(".honeypot")) return;
    // "channel" only decides how we deliver the message — it is not content.
    if (el.name === "channel") return;
    if ((el.type === "radio" || el.type === "checkbox") && !el.checked) return;
    const label =
      form.querySelector('label[for="' + el.id + '"]')?.childNodes[0]
        ?.textContent?.trim() || el.name;
    const value = (el.value || "").trim();
    if (value) lines.push(label.replace(/\*$/, "").trim() + ": " + value);
  });

  return lines.join("\n");
}

function initForms() {
  const forms = document.querySelectorAll("form[data-enquiry]");

  forms.forEach((form) => {
    const status = form.querySelector(".form-status");

    form.addEventListener("submit", async (e) => {
      e.preventDefault();

      // Bot trap — a real visitor never fills this in
      const trap = form.querySelector('input[name="company_website"]');
      if (trap && trap.value) return;

      if (!form.reportValidity()) return;

      const message = buildMessage(form);
      const channel =
        form.querySelector('input[name="channel"]:checked')?.value || "whatsapp";

      if (FORM_ENDPOINT) {
        try {
          const res = await fetch(FORM_ENDPOINT, {
            method: "POST",
            headers: { Accept: "application/json" },
            body: new FormData(form),
          });
          if (!res.ok) throw new Error("Request failed");
          showStatus(
            status,
            "Thank you — your enquiry has been sent. We reply to most enquiries within two working days."
          );
          form.reset();
          return;
        } catch (err) {
          showStatus(
            status,
            "We could not send that automatically. Please use the WhatsApp or email buttons below and your details will be carried across."
          );
        }
      }

      if (channel === "email") {
        const subject = encodeURIComponent(
          (form.dataset.formTitle || "Website enquiry") + " — IBO Mixed Farm"
        );
        window.location.href =
          "mailto:" +
          IBO.EMAIL +
          "?subject=" +
          subject +
          "&body=" +
          encodeURIComponent(message);
        showStatus(
          status,
          "Your email app is opening with the enquiry filled in. Press send and we will get back to you."
        );
      } else {
        window.open(
          "https://wa.me/" + IBO.WHATSAPP + "?text=" + encodeURIComponent(message),
          "_blank",
          "noopener"
        );
        showStatus(
          status,
          "WhatsApp is opening with your enquiry filled in. Press send and we will get back to you."
        );
      }
    });
  });
}

function showStatus(el, text) {
  if (!el) return;
  el.textContent = text;
  el.hidden = false;
  el.scrollIntoView({ behavior: "smooth", block: "center" });
}

/* --------------------------------------------------------------------------
   Footer year
   -------------------------------------------------------------------------- */
function initYear() {
  document.querySelectorAll("[data-year]").forEach((el) => {
    el.textContent = String(new Date().getFullYear());
  });
}

/* --------------------------------------------------------------------------
   Boot
   -------------------------------------------------------------------------- */
document.addEventListener("DOMContentLoaded", () => {
  applyContactDetails();
  initNav();
  initStickyHeader();
  initReveal();
  initGalleryFilter();
  initForms();
  initYear();
});
