/*
 * Career Compass — Question definitions
 *
 * Each question has a `type` that tells main.js how to render it, and an
 * `id` that becomes the key in the final answers object sent to the backend.
 *
 * Types used:
 *  - "multi"   : select multiple option cards
 *  - "single"  : select one option card
 *  - "text"    : free text input
 *  - "select"  : dropdown
 *  - "rank"    : drag-to-reorder priority list
 *
 * Trimmed to 8 questions (from 15) to fit a ~3-4 min presentation demo.
 * Kept: the two that directly drive the O*NET occupation match
 * (interests, dream_field), plus the ones with the highest personalization
 * value for the AI-written report (education level, work environment,
 * strengths, priorities, budget, preferred city).
 * Cut: work_with, problem_solving, risk_tolerance, study_location,
 * years_willing, avoid_field, dream_university — still useful signals, but
 * lower-value per second of demo time. Restore any of these later by
 * copying their block back in from git history if you want the fuller
 * assessment for a non-timed context.
 */

const QUESTIONS = [
  {
    id: "interests",
    type: "multi",
    eyebrow: "Interests",
    title: "Which subjects or activities do you enjoy most?",
    hint: "Pick as many as apply.",
    options: [
      "Math & Numbers", "Science", "Computers & Technology", "Arts & Design",
      "Business & Finance", "Writing & Communication", "Social Sciences",
      "Healthcare & Biology", "Engineering & Mechanics", "Teaching & Mentoring"
    ]
  },
  {
    id: "dream_field",
    type: "text",
    eyebrow: "Interests",
    title: "Do you have a career field in mind — one you're aiming for, or one you're already in?",
    hint: "Optional — write \"not sure\" if you don't.",
    placeholder: "e.g. Software Engineering, Medicine, Graphic Design..."
  },
  {
    id: "education_level",
    type: "single",
    eyebrow: "Background",
    title: "What's your current education level?",
    options: ["Matric", "Intermediate / FSc", "Bachelor's (in progress)", "Bachelor's (completed)", "Other"]
  },
  {
    id: "work_environment",
    type: "single",
    eyebrow: "Work Style",
    title: "What kind of work environment appeals to you most?",
    options: ["Office / Corporate", "Outdoors / Fieldwork", "Remote / Freelance", "Lab / Research", "Creative Studio", "Hospital / Clinical"]
  },
  {
    id: "strengths",
    type: "multi",
    eyebrow: "Strengths",
    title: "What are you naturally good at?",
    hint: "Pick as many as apply.",
    options: [
      "Math", "Communication", "Leadership", "Creativity",
      "Problem-solving", "Organization", "Technical / Coding", "Empathy & Helping Others"
    ]
  },
  {
    id: "priorities",
    type: "rank",
    eyebrow: "Priorities",
    title: "Rank what matters most to you in a career.",
    hint: "Drag to reorder — most important at the top.",
    options: ["High Salary", "Job Security", "Work-Life Balance", "Passion / Interest", "Social Impact", "Growth Opportunities"]
  },
  {
    id: "budget",
    type: "select",
    eyebrow: "Constraints",
    title: "What's your realistic budget range for further education?",
    options: ["Under 5 Lakh PKR", "5–15 Lakh PKR", "15–30 Lakh PKR", "30+ Lakh PKR", "Scholarship / Not sure yet"]
  },
  {
    id: "preferred_city",
    type: "select",
    eyebrow: "Constraints",
    title: "Which city/region would you prefer to study or work in?",
    options: ["Karachi", "Lahore", "Islamabad", "Rawalpindi", "Faisalabad", "Peshawar", "Multan", "No strong preference"]
  },
];
