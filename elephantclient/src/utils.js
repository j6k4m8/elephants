

// export const BASE_URL = "http://192.168.0.103:5000";
export const BASE_URL = "https://api.elephants.matelsky.com";

export function lerp(a, b, n) {
    return (1 - n) * a + n * b;
}

export function lngToPix(lng) {
    return lerp(0, 240000, (lng + 180) / 360);
}
