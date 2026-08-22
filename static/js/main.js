/*
 * Career Compass — Questionnaire engine (Tailwind/Stitch styled version)
 * Renders one question at a time from QUESTIONS (questions.js),
 * stores answers, and handles Back/Next navigation.
 */

let currentStep = 0;
const answers = {};

const form = document.getElementById("quizForm");
const nextBtn = document.getElementById("nextBtn");
const nextBtnLabel = document.getElementById("nextBtnLabel");
const backBtn = document.getElementById("backBtn");
const progressBar = document.getElementById("progress-bar");
const stepNumEl = document.getElementById("stepNum");
const stepTotalEl = document.getElementById("stepTotal");
const phaseLabelEl = document.getElementById("phaseLabel");

stepTotalEl.textContent = QUESTIONS.length;

// Fallback icon per category, used only if an option isn't in OPTION_META below
const CATEGORY_ICONS = {
  Interests: "explore", Background: "school", "Work Style": "work",
  Strengths: "star", Priorities: "trending_up", Constraints: "tune", Preferences: "bookmark"
};

// Per-option icon + one-line subtitle, matching the reference card design
// (icon tile + title + short description). Keyed by the exact option string
// from questions.js. Anything not listed here falls back to the category
// icon and no subtitle, so new/edited options never break rendering.
const OPTION_META = {
  // interests
  "Math & Numbers": { icon: "calculate", subtitle: "Numbers, logic, patterns" },
  "Science": { icon: "science", subtitle: "Experiments, discovery, research" },
  "Computers & Technology": { icon: "computer", subtitle: "Coding, software, systems" },
  "Arts & Design": { icon: "palette", subtitle: "Visual arts, design, creativity" },
  "Business & Finance": { icon: "payments", subtitle: "Markets, money, strategy" },
  "Writing & Communication": { icon: "edit_note", subtitle: "Storytelling, language, media" },
  "Social Sciences": { icon: "groups", subtitle: "Society, behavior, culture" },
  "Healthcare & Biology": { icon: "medical_services", subtitle: "Health, biology, care" },
  "Engineering & Mechanics": { icon: "precision_manufacturing", subtitle: "Building, machines, systems" },
  "Teaching & Mentoring": { icon: "school", subtitle: "Guiding, coaching, education" },
  // education_level
  "Matric": { icon: "looks_one", subtitle: "Currently in or completed Matric" },
  "Intermediate / FSc": { icon: "looks_two", subtitle: "Currently in or completed FSc" },
  "Bachelor's (in progress)": { icon: "menu_book", subtitle: "Working toward your degree" },
  "Bachelor's (completed)": { icon: "workspace_premium", subtitle: "Degree already in hand" },
  "Other": { icon: "more_horiz", subtitle: "Something else entirely" },
  // work_environment
  "Office / Corporate": { icon: "business_center", subtitle: "Structured, team-based, indoors" },
  "Outdoors / Fieldwork": { icon: "landscape", subtitle: "Hands-on, on-site, active" },
  "Remote / Freelance": { icon: "laptop_mac", subtitle: "Independent, flexible, self-paced" },
  "Lab / Research": { icon: "biotech", subtitle: "Focused, analytical, experimental" },
  "Creative Studio": { icon: "brush", subtitle: "Expressive, collaborative, visual" },
  "Hospital / Clinical": { icon: "local_hospital", subtitle: "Patient-facing, hands-on care" },
  // strengths
  "Math": { icon: "calculate", subtitle: "Numbers and quantitative thinking" },
  "Communication": { icon: "forum", subtitle: "Speaking, writing, listening" },
  "Leadership": { icon: "flag", subtitle: "Guiding and motivating others" },
  "Creativity": { icon: "auto_awesome", subtitle: "Original ideas, imagination" },
  "Problem-solving": { icon: "extension", subtitle: "Untangling tricky challenges" },
  "Organization": { icon: "checklist", subtitle: "Planning and structure" },
  "Technical / Coding": { icon: "terminal", subtitle: "Building with code and tools" },
  "Empathy & Helping Others": { icon: "volunteer_activism", subtitle: "Understanding and supporting people" },
};

function optionCard(q, opt, isSelected) {
  const meta = OPTION_META[opt];
  const icon = meta ? meta.icon : (CATEGORY_ICONS[q.eyebrow] || "check_circle");
  const subtitle = meta ? meta.subtitle : "";
  const btn = document.createElement("button");
  btn.type = "button";
  btn.dataset.value = opt;
  btn.className = `option-card group flex items-start gap-unit-md p-unit-md border rounded-lg text-left transition-all duration-300 w-full
    ${isSelected ? "bg-secondary border-secondary" : "bg-surface-container-high border-outline-variant/30 hover:border-secondary"}`;

  btn.innerHTML = `
    <div class="w-14 h-14 flex items-center justify-center rounded-lg shrink-0 transition-colors
      ${isSelected ? "bg-on-secondary text-secondary" : "bg-surface-variant text-secondary group-hover:bg-secondary group-hover:text-on-secondary"}">
      <span class="material-symbols-outlined text-[32px]">${icon}</span>
    </div>
    <div>
      <h3 class="font-headline-sm mb-1 ${isSelected ? "text-on-secondary" : "text-on-surface"}">${opt}</h3>
      ${subtitle ? `<p class="font-body-sm ${isSelected ? "text-on-secondary/80" : "text-on-surface-variant"}">${subtitle}</p>` : ""}
    </div>
  `;
  return btn;
}

function renderStep(index) {
  const q = QUESTIONS[index];
  form.innerHTML = "";

  const header = document.createElement("div");
  header.className = "mb-unit-xl";
  header.innerHTML = `
    <div class="flex items-center gap-unit-sm mb-unit-md">
      <span class="w-12 h-0.5 bg-secondary"></span>
      <span class="font-label-lg text-secondary uppercase">${q.eyebrow}</span>
    </div>
    <h1 class="font-headline-xl text-headline-xl-mobile lg:text-headline-xl text-on-surface max-w-2xl">${q.title}</h1>
    ${q.hint ? `<p class="font-body-lg text-on-surface-variant mt-unit-md">${q.hint}</p>` : ""}
  `;
  form.appendChild(header);

  if (q.type === "multi" || q.type === "single") {
    const grid = document.createElement("div");
    grid.className = "grid grid-cols-1 md:grid-cols-2 gap-gutter";

    q.options.forEach(opt => {
      const current = answers[q.id];
      const isSelected = q.type === "multi"
        ? Array.isArray(current) && current.includes(opt)
        : current === opt;

      const card = optionCard(q, opt, isSelected);
      card.addEventListener("click", () => {
        if (q.type === "single") {
          answers[q.id] = opt;
        } else {
          if (!Array.isArray(answers[q.id])) answers[q.id] = [];
          const arr = answers[q.id];
          const pos = arr.indexOf(opt);
          if (pos >= 0) arr.splice(pos, 1); else arr.push(opt);
        }
        renderStep(currentStep); // re-render to reflect selection state
      });
      grid.appendChild(card);
    });
    form.appendChild(grid);
  }

  if (q.type === "text") {
    const input = document.createElement("input");
    input.type = "text";
    input.placeholder = q.placeholder || "";
    input.value = answers[q.id] || "";
    input.className = "w-full bg-surface-container-high border border-outline-variant/30 focus:border-secondary rounded-lg px-unit-md py-unit-md text-on-surface font-body-md outline-none transition-colors";
    input.addEventListener("input", () => { answers[q.id] = input.value; });
    form.appendChild(input);
  }

  if (q.type === "select") {
    const select = document.createElement("select");
    select.className = "w-full bg-surface-container-high border border-outline-variant/30 focus:border-secondary rounded-lg px-unit-md py-unit-md text-on-surface font-body-md outline-none transition-colors";
    const blank = document.createElement("option");
    blank.textContent = "Select an option...";
    blank.value = "";
    select.appendChild(blank);
    q.options.forEach(opt => {
      const o = document.createElement("option");
      o.value = opt;
      o.textContent = opt;
      if (answers[q.id] === opt) o.selected = true;
      select.appendChild(o);
    });
    select.addEventListener("change", () => { answers[q.id] = select.value; });
    form.appendChild(select);
  }

  if (q.type === "rank") {
    if (!Array.isArray(answers[q.id])) answers[q.id] = [...q.options];
    const list = document.createElement("ul");
    list.className = "flex flex-col gap-unit-sm";

    function renderRankItems() {
      list.innerHTML = "";
      answers[q.id].forEach((opt, i) => {
        const li = document.createElement("li");
        li.draggable = true;
        li.dataset.index = i;
        li.className = "flex items-center gap-unit-md bg-surface-container-high border border-outline-variant/30 rounded-lg px-unit-md py-unit-md cursor-grab";
        li.innerHTML = `<span class="font-headline-sm text-secondary w-6">${i + 1}</span><span class="font-body-md text-on-surface">${opt}</span>`;
        list.appendChild(li);
      });
    }
    renderRankItems();

    let dragSrc = null;
    list.addEventListener("dragstart", e => {
      if (e.target.tagName === "LI") dragSrc = e.target.dataset.index;
    });
    list.addEventListener("dragover", e => e.preventDefault());
    list.addEventListener("drop", e => {
      e.preventDefault();
      const target = e.target.closest("li");
      if (!target || dragSrc === null) return;
      const from = parseInt(dragSrc);
      const to = parseInt(target.dataset.index);
      const arr = answers[q.id];
      const [moved] = arr.splice(from, 1);
      arr.splice(to, 0, moved);
      renderRankItems();
    });

    form.appendChild(list);
  }

  // Progress + labels
  stepNumEl.textContent = index + 1;
  progressBar.style.width = `${((index + 1) / QUESTIONS.length) * 100}%`;
  phaseLabelEl.textContent = `Phase: ${q.eyebrow}`;
  backBtn.disabled = index === 0;
  nextBtnLabel.textContent = index === QUESTIONS.length - 1 ? "Finish" : "Continue";
}

nextBtn.addEventListener("click", () => {
  if (currentStep < QUESTIONS.length - 1) {
    currentStep++;
    renderStep(currentStep);
    window.scrollTo({ top: 0, behavior: "smooth" });
  } else {
    submitAnswers();
  }
});

backBtn.addEventListener("click", () => {
  if (currentStep > 0) {
    currentStep--;
    renderStep(currentStep);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }
});

const LOADING_MESSAGES = [
  "Analyzing your responses...",
  "Matching real occupational data...",
  "Cross-referencing Pakistani job market outlook...",
  "Checking universities in your preferred city...",
  "Building your personalized roadmap...",
  "Still working — this can take up to a minute...",
  "Almost ready..."
];

function submitAnswers() {
  console.log("Final answers:", answers);

  const overlay = document.getElementById("loadingOverlay");
  const msgEl = document.getElementById("loadingMessage");
  const percentEl = document.getElementById("loadingPercent");
  const barEl = document.getElementById("loadingProgressBar");
  overlay.classList.remove("hidden");
  overlay.classList.add("flex");

  let msgIndex = 0;
  const msgInterval = setInterval(() => {
    msgIndex = (msgIndex + 1) % LOADING_MESSAGES.length;
    msgEl.classList.add("opacity-0");
    setTimeout(() => {
      msgEl.textContent = LOADING_MESSAGES[msgIndex];
      msgEl.classList.remove("opacity-0");
    }, 250);
  }, 1600);

  // Fake-but-honest progress readout: never claims 100% until the real
  // response comes back, since we don't know how long O*NET/Gemini will
  // actually take. Creeps toward 95% and holds, then jumps to 100% on success.
  let percent = 4;
  const progressInterval = setInterval(() => {
    if (percent < 95) {
      percent += Math.floor(Math.random() * 6) + 2;
      if (percent > 95) percent = 95;
      percentEl.textContent = percent + "%";
      barEl.style.width = percent + "%";
    }
  }, 900);

  function finishProgress() {
    clearInterval(progressInterval);
    percentEl.textContent = "100%";
    barEl.style.width = "100%";
  }

  fetch("/generate-report", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(answers)
  })
    .then(res => res.json().then(data => ({ status: res.status, data })))
    .then(({ status, data }) => {
      clearInterval(msgInterval);
      finishProgress();
      if (status !== 200) {
        console.error("Report generation failed:", data.error);
        alert("Something went wrong generating your report: " + data.error +
              "\n\n(Falling back to the sample roadmap for now.)");
        window.location.href = "/sample-roadmap";
        return;
      }
      // Stash the real report so the results page can read and render it
      sessionStorage.setItem("careerCompassReport", JSON.stringify(data));
      window.location.href = "/sample-roadmap";
    })
    .catch(err => {
      clearInterval(msgInterval);
      finishProgress();
      console.error("Network error:", err);
      alert("Couldn't reach the server. Check that the Flask app is running.\n\n(Falling back to the sample roadmap for now.)");
      window.location.href = "/sample-roadmap";
    });
}

renderStep(currentStep);
