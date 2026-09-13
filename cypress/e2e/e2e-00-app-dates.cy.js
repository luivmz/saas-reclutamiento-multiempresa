import { appDate } from '../support/dates';

// Support check for DEF-12: the dates used by the specs follow America/Lima, whatever the runner's clock zone.
describe('Soporte · fechas en la zona horaria de la aplicación', () => {
    const lateEveningInLima = Date.parse('2026-09-14T02:30:00Z'); // 13/09/2026 21:30 in Lima, already 14/09 in UTC

    it('usa la fecha de Lima aunque en UTC ya sea el día siguiente', () => {
        expect(new Date(lateEveningInLima).toISOString().slice(0, 10)).to.equal('2026-09-14');
        expect(appDate(0, lateEveningInLima, 'America/Lima')).to.equal('2026-09-13');
        expect(appDate(30, lateEveningInLima, 'America/Lima')).to.equal('2026-10-13');
    });

    it('coincide con UTC durante el día en Lima', () => {
        const middayInLima = Date.parse('2026-09-13T17:00:00Z'); // 12:00 in Lima

        expect(appDate(0, middayInLima, 'America/Lima')).to.equal('2026-09-13');
        expect(appDate(2, middayInLima, 'America/Lima')).to.equal('2026-09-15');
    });

    it('usa America/Lima por defecto', () => {
        expect(appDate(0, lateEveningInLima)).to.equal('2026-09-13');
    });
});
