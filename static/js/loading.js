/*
 * Career Compass — shared loading overlay controller.
 *
 * Wraps the #loadingOverlay markup (templates/_loading_overlay.html,
 * included globally in base.html) so ANY page's script can drive the same
 * "premium navy/gold editorial" loading screen with one small API, instead
 * of each page re-implementing its own percent-counter/message logic (or,
 * worse, using a plain text spinner instead of the real loading screen).
 *
 * Usage:
 *   CareerCompassLoader.show({
 *     tagline: "Building your roadmap",
 *     messages: ["Analyzing your responses...", "Matching real occupational data..."]
 *   });
 *   ...
 *   CareerCompassLoader.hide();   // or .finish() to snap to 100% first, then hide()
 */
const CareerCompassLoader = (function () {
  let msgInterval = null;
  let progressInterval = null;
  let percent = 4;

  function els() {
    return {
      overlay: document.getElementById("loadingOverlay"),
      tagline: document.getElementById("loadingTitle"),
      msg: document.getElementById("loadingMessage"),
      percentEl: document.getElementById("loadingPercent"),
      bar: document.getElementById("loadingProgressBar"),
    };
  }

  function show(opts) {
    opts = opts || {};
    const { overlay, tagline, msg, percentEl, bar } = els();
    if (!overlay) return; // overlay markup not present on this page for some reason

    const messages = opts.messages && opts.messages.length ? opts.messages : ["One moment..."];
    let msgIndex = 0;

    if (tagline) tagline.textContent = opts.tagline || "Navigating what comes next";
    if (msg) msg.textContent = messages[0];

    percent = 4;
    if (percentEl) percentEl.textContent = percent + "%";
    if (bar) bar.style.width = percent + "%";

    overlay.classList.remove("hidden");
    overlay.classList.add("flex");

    clearInterval(msgInterval);
    clearInterval(progressInterval);

    if (messages.length > 1) {
      msgInterval = setInterval(() => {
        msgIndex = (msgIndex + 1) % messages.length;
        if (!msg) return;
        msg.classList.add("opacity-0");
        setTimeout(() => {
          msg.textContent = messages[msgIndex];
          msg.classList.remove("opacity-0");
        }, 250);
      }, 1600);
    }

    // Fake-but-honest progress: creeps toward 95% and holds there until
    // finish()/hide() is called — never claims 100% until we actually know
    // the operation is done.
    progressInterval = setInterval(() => {
      if (percent >= 95) return;
      percent += Math.floor(Math.random() * 6) + 2;
      if (percent > 95) percent = 95;
      if (percentEl) percentEl.textContent = percent + "%";
      if (bar) bar.style.width = percent + "%";
    }, 900);
  }

  function finish() {
    clearInterval(progressInterval);
    const { percentEl, bar } = els();
    if (percentEl) percentEl.textContent = "100%";
    if (bar) bar.style.width = "100%";
  }

  function hide() {
    clearInterval(msgInterval);
    clearInterval(progressInterval);
    const { overlay } = els();
    if (!overlay) return;
    overlay.classList.remove("flex");
    overlay.classList.add("hidden");
  }

  return { show, hide, finish };
})();
