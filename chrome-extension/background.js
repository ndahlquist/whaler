
/**
 * The default content security policy for github.com only allows AJAX posts to white-listed domains.
 * In order to allow us to post to our server, we intercept the content-security-policy header and whitelist our domain.
 */

chrome.webRequest.onHeadersReceived.addListener(function(details) {
    for(var i = 0; i < details.responseHeaders.length; ++i) {
        if (details.responseHeaders[i].name.toLowerCase() == 'content-security-policy') {
            console.log("Amending content-security-policy for " + details.url)
            details.responseHeaders[i].value += " dev-dot-whaler-on-fleek.appspot.com"
        }
    }
    return {responseHeaders:details.responseHeaders};
}, {
    urls: [
        '*://github.com/*/pull/*'
    ]
}, [
    'blocking',
    'responseHeaders'
]);

