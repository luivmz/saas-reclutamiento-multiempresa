import type { SVGAttributes } from 'react';

/**
 * Marca de la plataforma.
 *
 * Tres renglones de un expediente y, al costado, la marca que deja una
 * persona al decidir sobre él. Es la idea que sostiene todo el producto: el
 * sistema lleva el registro; la decisión la firma alguien.
 */
export default function AppLogoIcon(props: SVGAttributes<SVGElement>) {
    return (
        <svg
            {...props}
            viewBox="0 0 24 24"
            xmlns="http://www.w3.org/2000/svg"
            aria-hidden="true"
            focusable="false"
        >
            <rect x="2" y="4" width="15" height="3" rx="1.5" />
            <rect x="2" y="10" width="10" height="3" rx="1.5" />
            <rect x="2" y="16" width="13" height="3" rx="1.5" />
            <circle cx="20" cy="11.5" r="2.5" />
        </svg>
    );
}
