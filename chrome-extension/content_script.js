/**
 * Our CSS makes the merge buttons blue.
 */
function injectCSS() {
  var link = document.createElement('link');
  link.href = chrome.extension.getURL('css/whaler.css');
  link.rel = 'stylesheet';
  head = document.getElementsByTagName ('head')[0] || document.documentElement;
  head.insertBefore(link, head.lastChild);
}

function updateDocument() {
  if (!/\/pull\//.test(document.URL)) {
    // This is not a pull request URL.
    return false;
  }
  if (supportsWhaler(document.URL)) {
    whalifyDocument();
  } else {
    dewhalifyDocument();
  }
}

function whalifyDocument() {
  mergeButton = document.querySelector('.merge-branch-action');
  if (mergeButton != null) {
    // Add our CSS tag to paint the button blue.
    mergeButton.className = mergeButton.className.replace(/primary/g, 'whaler');
    // Modify the text
    mergeButton.innerHTML = mergeButton.innerHTML.replace(/Merge pull request/g, 'Squash merge')
  }

  form = document.querySelector('.merge-branch-form');
  if (form != null) {
    // Redirect the form to our server so that we can handle the merge.
    form.action = 'https://whaler-on-fleek.appspot.com/queue_merge';

    confirmMergeButton = form.querySelector('.button');
    // Add our CSS tag to paint the button blue.
    confirmMergeButton.className = confirmMergeButton.className.replace(/primary/g, 'whaler');
  }

  merge_description = document.querySelector('.merge-branch-description')
  if (originalMergeDescription != null) merge_description.innerHTML = originalMergeDescription;
}

var originalMergeDescription = null

function dewhalifyDocument() {
  mergeButton = document.querySelector('.merge-branch-action');
  if (mergeButton != null) {
    // Remove our CSS tag to paint the button blue.
    mergeButton.className = mergeButton.className.replace(/whaler/g, 'primary');
    // Remove our text modifications.
    mergeButton.innerHTML = mergeButton.innerHTML.replace(/Squash merge/g, 'Merge pull request')
  }

  form = document.querySelector('.merge-branch-form');
  if (form != null) {
    // Change the form's URL back to its original state.
    form.action = document.URL + '/merge';

    confirmMergeButton = form.querySelector('.button');
    // Add our CSS tag to paint the button blue.
    confirmMergeButton.className = confirmMergeButton.className.replace(/whaler/g, 'primary');
  }

  merge_description = document.querySelector('.merge-branch-description')
  if (originalMergeDescription == null) originalMergeDescription = merge_description.innerHTML;
  merge_description.innerHTML = url_support_cache[document.URL]
}

/**
 * A mapping of URLs to one of the following Strings:
 *  "supported:" We have found that this URL supports whaler.
 *  "optimistic:" A call to the /supports_whaler is pending (we optimistically assume support).
 *  [other]: This is an error message returned by the server.
 */
var url_support_cache = {}

/**
 * Returns false if Whaler does not have collabotar access to this repo.
 * This requires a server request, so this returns true in both the case that we have verified
 * access and the optimistic case.
 */
function supportsWhaler(url) {
  if (url_support_cache[url]) {
    return url_support_cache[url] === 'supported' || url_support_cache[url] === 'optimistic'
  }
  $.get('https://whaler-on-fleek.appspot.com/supports_whaler', function(responseText) {
    url_support_cache[url] = responseText;
    updateDocument();
  });
  url_support_cache[url] = 'optimistic'
  return true
}

function domNodeInsertedCallback() {
    console.log('DomNodeInsertedCallback()');

    // We must remove the event listener before updateDocument() to prevent recursion.
    document.removeEventListener('DOMNodeInserted', domNodeInsertedCallback);
    updateDocument();
    document.addEventListener('DOMNodeInserted', domNodeInsertedCallback);
}

injectCSS();
updateDocument();

// GitHub dynamically modifies the merge form. We need to make sure we apply our modifications when it is updated.
// TODO: This is allegedly terrible for performance. What's a better way of doing this?
document.addEventListener('DOMNodeInserted', domNodeInsertedCallback);

