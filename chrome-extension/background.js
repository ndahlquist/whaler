
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

/**
 * Randomly generates a 24 character string.
 */
function getRandomToken() {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

    for( var i=0; i < 24; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}

/**
 * Responds to messages posted by the content script.
 */
chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.message != "get_session_token") return false;

    chrome.cookies.get({"url": "https://whaler-on-fleek.appspot.com", "name": "session"}, function(cookie) {
      if (cookie == null) {
        session_id = getRandomToken();
        chrome.cookies.set({"url": "https://whaler-on-fleek.appspot.com",
                            "name": "session",
                            "value": session_id,
                            "secure": true})
      } else {
        session_id = cookie.value
      }

      sendResponse({session_token: session_id});
    });
    return true; // We will respond asynchronously.
  });
