import { describe, expect, test } from 'vitest';
import {
    barRatio,
    formatNumber,
    formatWeek,
    plural,
    reportQuery,
} from './reports';

describe('RF-28 candidato: utilidades del módulo de reportes', () => {
    test('las cifras sin datos se muestran como guion y no como cero', () => {
        expect(formatNumber(null)).toBe('—');
        expect(formatNumber(null, ' %')).toBe('—');
        expect(formatNumber(0)).toBe('0');
    });

    test('las cifras usan formato es-PE con un decimal como máximo', () => {
        expect(formatNumber(2.5)).toBe('2.5');
        expect(formatNumber(66.66, ' %')).toBe('66.7 %');
        expect(formatNumber(1284)).toBe('1,284');
    });

    test('el plural concuerda con la cantidad', () => {
        expect(plural(1, 'postulación', 'postulaciones')).toBe('1 postulación');
        expect(plural(0, 'postulación', 'postulaciones')).toBe(
            '0 postulaciones',
        );
        expect(plural(3, 'vacante', 'vacantes')).toBe('3 vacantes');
    });

    test('la semana se formatea sin desplazarse por la zona horaria', () => {
        expect(formatWeek('2026-11-09')).toMatch(/^09/);
    });

    test('la escala de barras empieza en cero y no excede el máximo', () => {
        expect(barRatio(0, 10)).toBe(0);
        expect(barRatio(5, 0)).toBe(0);
        expect(barRatio(5, 10)).toBe(0.5);
        expect(barRatio(12, 10)).toBe(1);
    });

    test('la consulta solo envía los filtros con valor', () => {
        expect(
            reportQuery({
                desde: '2026-08-12',
                hasta: '2026-11-09',
                vacante: '',
                estado: 'preseleccionado',
            }),
        ).toEqual({
            desde: '2026-08-12',
            hasta: '2026-11-09',
            estado: 'preseleccionado',
        });
        expect(
            reportQuery({ desde: ' ', hasta: '', vacante: '', estado: '' }),
        ).toEqual({});
    });
});
