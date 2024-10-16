const CACHE_NAME = 'media-cache-v1';

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
    );
});

self.addEventListener('fetch', (event) => {
    if (event.request.url.match(/\.(jpg|jpeg|png|gif|bmp|mp4)$/i)) {
        event.respondWith(
            caches.open(CACHE_NAME).then((cache) => {
                return cache.match(event.request).then((cachedResponse) => {
                    if (cachedResponse) {
                        console.log('Serving from cache:', event.request.url);
                        return cachedResponse;
                    }

                    return fetch(event.request).then((fetchedResponse) => {
                        console.log('Fetching and caching:', event.request.url);
                        cache.put(event.request, fetchedResponse.clone());
                        return fetchedResponse;
                    });
                });
            })
        );
    }
});

