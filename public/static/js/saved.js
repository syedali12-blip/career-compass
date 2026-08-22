/*
 * Career Compass — Saved Reports storage helper
 *
 * WHY localStorage, not sessionStorage: the existing "careerCompassReport"
 * key (set after /generate-report) uses sessionStorage, which is cleared
 * when the tab closes — fine for "the report currently being viewed," but
 * exactly why "Saved Options" never actually saved anything: there was no
 * persistence layer at all, just a "Coming Soon" placeholder page. This
 * file adds real persistence via localStorage, which survives across tabs/
 * sessions on the same browser (there's no user account/database in this
 * app, so browser storage is the only persistence layer available).
 *
 * Storage shape: a single localStorage key holding a JSON array of
 * { id, savedAt, report } entries — kept as one key (not one key per
 * saved report) so reads/writes are simple and atomic.
 */
const CareerCompassSaved = (function () {
  const STORAGE_KEY = "careerCompassSavedReports";

  function getAll() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      const parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      console.error("Couldn't read saved reports:", e);
      return [];
    }
  }

  function _writeAll(entries) {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(entries));
      return true;
    } catch (e) {
      // Most likely quota exceeded (localStorage is typically ~5-10MB) —
      // surface this instead of silently losing the save.
      console.error("Couldn't write saved reports:", e);
      return false;
    }
  }

  // Reports don't have a stable ID from the backend, so build one from
  // content + time — good enough to dedupe "I clicked Save twice" without
  // needing a real database.
  function _makeId(report) {
    const base = (report.recommended_path || "untitled") + "-" + Date.now();
    return base.replace(/\s+/g, "-").toLowerCase() + "-" + Math.random().toString(36).slice(2, 7);
  }

  function isAlreadySaved(report) {
    const all = getAll();
    // Same recommended_path + same onet_code counts as "the same result" —
    // avoids duplicate saves of the exact same roadmap from re-clicking Save.
    return all.some(entry =>
      entry.report &&
      entry.report.recommended_path === report.recommended_path &&
      entry.report.onet_code === report.onet_code
    );
  }

  function save(report) {
    if (isAlreadySaved(report)) return { ok: false, reason: "duplicate" };
    const all = getAll();
    const entry = { id: _makeId(report), savedAt: new Date().toISOString(), report };
    all.unshift(entry); // newest first
    const ok = _writeAll(all);
    return { ok, entry };
  }

  function remove(id) {
    const all = getAll().filter(e => e.id !== id);
    return _writeAll(all);
  }

  function getById(id) {
    return getAll().find(e => e.id === id) || null;
  }

  return { getAll, save, remove, getById, isAlreadySaved };
})();
