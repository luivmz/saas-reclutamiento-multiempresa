import { renderToStaticMarkup } from 'react-dom/server';
import { describe, expect, test } from 'vitest';
import {
    ApplicationRequirements,
    formatCvLimit,
    joinList,
} from '@/components/jobs/application-requirements';
import { ReturnNotice } from '@/components/jobs/return-notice';

const requirements = {
    perfil: ['teléfono', 'ciudad', 'nivel educativo'],
    cv: { formato: 'PDF', max_kb: 5120 },
};

/**
 * Lote 2: los requisitos se anuncian con los datos que envía el servidor
 * (las mismas reglas que validan), sin cifras escritas a mano.
 */
describe('Requisitos para postular', () => {
    test('enumera en castellano y expresa el límite del CV', () => {
        expect(joinList(['a'])).toBe('a');
        expect(joinList(['a', 'b', 'c'])).toBe('a, b y c');
        expect(formatCvLimit(5120)).toBe('5 MB');
        expect(formatCvLimit(1500)).toBe('1500 KB');
    });

    test('la versión completa separa el perfil del CV y usa los datos recibidos', () => {
        const markup = renderToStaticMarkup(
            <ApplicationRequirements requirements={requirements} />,
        );

        expect(markup).toContain('teléfono, ciudad y nivel educativo');
        expect(markup).toContain('PDF de hasta 5 MB');
        expect(markup).toContain('Su CV');
    });

    test('la versión compacta es una sola frase', () => {
        const markup = renderToStaticMarkup(
            <ApplicationRequirements
                requirements={{
                    ...requirements,
                    cv: { formato: 'PDF', max_kb: 2048 },
                }}
                compact
            />,
        );

        expect(markup.match(/<p/g)).toHaveLength(1);
        expect(markup).toContain('PDF de hasta 2 MB');
    });

    test('el aviso de retorno no promete postular ni el retorno a otros roles', () => {
        const vacancy = { id: 7, title: 'Docente de Prueba' };
        const acceso = renderToStaticMarkup(
            <ReturnNotice vacancy={vacancy} context="login" />,
        );
        const registro = renderToStaticMarkup(
            <ReturnNotice vacancy={vacancy} context="register" />,
        );

        expect(acceso).toContain('Docente de Prueba');
        expect(acceso).toContain('cuenta de postulante');
        expect(registro).not.toContain('Si entra');
    });
});
