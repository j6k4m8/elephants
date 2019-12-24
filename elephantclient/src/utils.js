

// export const BASE_URL = "http://localhost:5050";
export const BASE_URL = "https://bwmf3n2rre.execute-api.us-east-1.amazonaws.com/production";

export function lerp(a, b, n) {
    return (1 - n) * a + n * b;
}

export function lngToPix(lng) {
    return lerp(0, 240000, (lng + 180) / 360);
}

export const REPORT_FREQUENCY = 16000;
