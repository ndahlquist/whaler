
/**
 * The default content security policy for github.com only allows AJAX posts to white-listed domains.
 * In order to allow us to post to our server, we intercept the content-security-policy header and whitelist our domain.
 */

chrome.webRequest.onHeadersReceived.addListener(function(details) {
    for(var i = 0; i < details.responseHeaders.length; ++i) {
        if (details.responseHeaders[i].name.toLowerCase() == 'content-security-policy') {
            console.log("Amending content-security-policy for " + details.url)
            details.responseHeaders[i].value += " whaler-on-fleek.appspot.com"
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

/**
 * Randomly generates a 24 character string.
 */
function getRandomToken() {
    var array = new Uint32Array(10);
    window.crypto.getRandomValues(array);

    var text = "";
    for (var i = 0; i < array.length; i++) {
       text += intToChar(array[i] & 255)
       text += intToChar((array[i] >> 8 ) & 255)
       text += intToChar((array[i] >> 16) & 255)
       text += intToChar((array[i] >> 24) & 255)
    }
    return text;
}

function intToChar(input) {
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    return possible.charAt(input % possible.length)
}

/**
 * Responds to messages posted by the content script.
 */
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.message != "get_session_token") return false;

    chrome.cookies.get({"url": "https://github.com", "name": "whaler_session"}, function(cookie) {
      if (cookie == null) {
        session_id = getRandomToken();
        expirationDate = new Date().getTime() / 1000 + 60 * 60 * 24 * 7 // Expire in 1 week
        chrome.cookies.set({"url": "https://github.com",
                            "name": "whaler_session",
                            "value": session_id,
                            "expirationDate": expirationDate,
                            "secure": true})
      } else {
        session_id = cookie.value
      }

      sendResponse({session_token: session_id});
    });
    return true; // We will respond asynchronously.
  });
