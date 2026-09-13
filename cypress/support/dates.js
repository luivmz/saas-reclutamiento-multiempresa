// Calendar dates for form inputs, computed in the application timezone (APP_TIMEZONE), not in the runner's UTC clock.
// Between 19:00 and 24:00 in Lima the UTC date is already the next day (DEF-12).
const DAY_MS = 24 * 60 * 60 * 1000;

export function appDate(offsetDays = 0, now = Date.now(), timeZone = Cypress.env('APP_TIMEZONE') || 'America/Lima') {
    return new Intl.DateTimeFormat('en-CA', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).format(
        new Date(now + offsetDays * DAY_MS),
    );
}
